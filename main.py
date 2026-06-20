from fastapi import FastAPI
from app.routes import tarefas


app = FastAPI(title="Task Manager API")
app.include_router (tarefas.router)

@app.get("/")

def read_root():
    return {"message": "Task Manager API está no ar!"}