import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    URL_LOAD_TIMEOUT = os.environ.get('URL_LOAD_TIMEOUT') or 10
    THREAD_COUNT = os.environ.get('THREAD_COUNT') or 10