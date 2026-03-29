import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# These dots are CRITICAL because the file is now inside the /server folder
from .environment import EmailTriageEnv, Action
from .grader import grade_easy, grade_medium, grade_hard

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
    
    # Initialize the environment
    env = EmailTriageEnv(task_level=task_level)
    obs = env.reset()
    envs[session_id] = env
    
    # The validator requires the key "observation"
    # We ensure it's a dictionary or a string
    return {"observation": obs.dict() if hasattr(obs, 'dict') else obs}

@app.post("/step")
def step(req: StepRequest):
    env = envs.get(req.session_id)
    if not env:
        return {"error": "Session not found. Call /reset first."}
    
    # Convert string label to Action object
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

# --- ENTRY POINT FOR THE VALIDATOR ---
def main():
    """
    Starts the server on port 8000. 
    Using 'server.app:app' tells uvicorn the file is in the /server folder.
    """
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
