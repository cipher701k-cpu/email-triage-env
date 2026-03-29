import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from .environment import EmailTriageEnv, Action
from .grader import grade_easy, grade_medium, grade_hard

app = FastAPI(title="Email Triage Environment")

# In-memory storage for active sessions
envs = {}

class StepRequest(BaseModel):
    session_id: str
    label: str

@app.get("/")
def root():
    return {"message": "Email Triage Environment is running!", "status": "ready"}

@app.post("/reset")
async def reset(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
    
    session_id = body.get("session_id", "default_session")
    task_level = body.get("task_level", "easy")
    
    env = EmailTriageEnv(task_level=task_level)
    obs = env.reset()
    envs[session_id] = env
    
    return {"observation": obs.dict() if hasattr(obs, 'dict') else obs}

@app.post("/step")
def step(req: StepRequest):
    env = envs.get(req.session_id)
    if not env:
        return {"error": "Session not found. Call /reset first."}
    
    action = Action(label=req.label)
    obs, reward, done = env.step(action)
    
    return {
        "observation": obs.dict() if hasattr(obs, 'dict') else obs,
        "reward": reward.dict() if hasattr(reward, 'dict') else reward,
        "done": done
    }

@app.get("/state/{session_id}")
def state(session_id: str):
    env = envs.get(session_id)
    if not env:
        return {"error": "Session not found."}
    return env.state()

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
