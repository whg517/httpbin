"""app"""
import uvicorn
from fastapi import FastAPI

from httpbin.config import settings

app = FastAPI()


@app.get('/')
def index():
    """index"""
    return {'hello': 'world'}


def main():
    """main"""
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
