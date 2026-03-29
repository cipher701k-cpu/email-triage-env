import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Import your custom environment and grader logic
from environment import EmailTriageEnv, Action
from grader import grade_easy, grade_medium, grade_hard

app = FastAPI(title="Email Triage Environment")

# In-memory storage for active sessions
envs = {}

class StepRequest(BaseModel):
    session_id: str
    label: str

class ResetRequest(BaseModel):
    session_id: str = "default_session"
    task_level: str = "easy"

@app.get("/")
def root():
    return {"message": "Email Triage Environment is running!", "status": "ready"}

@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    # Fallback values if the validator sends an empty body
    session_id = req.session_id if req else "default_session"
    task_level = req.task_level if req else "easy"
    
    env = EmailTriageEnv(task_level=task_level)
    obs = env.reset()
    envs[session_id] = env
    
    # Return observation in the format the validator expects
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

# --- THE CRITICAL FIX FOR MULTI-MODE DEPLOYMENT ---
def main():
    """
    The entry point called by 'uv run server' as defined in pyproject.toml
    """
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
