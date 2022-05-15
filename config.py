import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    URL_LOAD_TIMEOUT = int(os.environ.get("URL_LOAD_TIMEOUT"))
    THREAD_COUNT = int(os.environ.get("THREAD_COUNT"))