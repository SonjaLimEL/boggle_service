import os


class Settings:
    USE_CELERY = os.environ.get('USE_CELERY', False)
