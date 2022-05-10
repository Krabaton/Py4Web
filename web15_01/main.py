from fastapi import FastAPI, Request
from routers import blogs
import time

app = FastAPI()
app.include_router(blogs.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get('/test')
def index():
    return {'message': 'Hello world!'}


