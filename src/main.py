from typing import Annotated, Union

import json
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import service
from request_response_models import (
    GetBoardRequest,
    GetBoardResponse,
    BoggleBoardModel,
    GetBoardTaskResponse
)
from board.boggle_board import BoggleBoard


app = FastAPI()


@app.get("/board")
def get_board(filter_query: Annotated[GetBoardRequest, Query()]) -> Union[GetBoardResponse, GetBoardTaskResponse]:
    result = service.get_board(generation_method=filter_query.generation_method)
    if isinstance(result, BoggleBoard):
        return GetBoardResponse(
            board=BoggleBoardModel(
                letters=result.letters,
                words=result.words,
                max_score=result.maximum_possible_score()
            )
        )
    else:
        return GetBoardTaskResponse(
            task_id=result
        )


@app.get("/board/{task_id}")
def get_async_board(task_id) -> GetBoardResponse:
    try:
        result = service.get_board_from_redis(task_id)
    except service.CeleryTaskException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except service.CeleryTaskUnreadyException as e:
        return JSONResponse(status_code=202, content={"message": "board not ready"})

    board_dict = json.loads(result)
    return GetBoardResponse(
        board=BoggleBoardModel(
            letters=board_dict["letters"],
            words=board_dict["words"],
            max_score=board_dict["max_score"]
        )
    )
