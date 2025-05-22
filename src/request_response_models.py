from typing import Optional

from pydantic import BaseModel, Field, validator
from shared import BoardGenerationOptions


class GetBoardRequest(BaseModel):
    generation_method: Optional[BoardGenerationOptions] = Field(None)
    letters: Optional[str] = Field(None, length=16)

    @validator("letters", always=True)
    def mutually_exclusive(cls, v, values):
        if values["generation_method"] is not None and v:
            raise ValueError("'generation_method' and 'letters' are mutually exclusive.")

        return v


class BoggleBoardModel(BaseModel):
    letters: str = Field(length=16)
    words: list[str]
    max_score: int


class GetBoardResponse(BaseModel):
    board: BoggleBoardModel

class GetBoardTaskResponse(BaseModel):
    task_id: str

class GetBoardNotReadyResponse(BaseModel):
    task_id: str
    ready: bool = False