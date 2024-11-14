from fastapi import FastAPI
from routers import task, user
import uvicorn

app = FastAPI(swagger_ui_parameters={'tryItOutEnabled': True})

app.include_router(task.router)
app.include_router(user.router)

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7000, log_level='info')