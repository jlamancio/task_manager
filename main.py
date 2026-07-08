from fastapi import FastAPI
from app.routes import tarefas, auth




app = FastAPI(title="Task Manager API")
app.include_router (tarefas.router)
app.include_router(auth.router)

@app.get("/")

def read_root():
    return {"message": "Task Manager API está no ar!"}