from fastapi import FastAPI
from pydantic import BaseModel
from environment import EmailTriageEnv, Action
from grader import grade_easy, grade_medium, grade_hard
import uvicorn

app = FastAPI(title="Email Triage Environment")

envs = {}

class StepRequest(BaseModel):
    session_id: str
    label: str

class ResetRequest(BaseModel):
    session_id: str
    task_level: str = "easy"

@app.get("/")
def root():
    return {"message": "Email Triage Environment is running!"}

@app.post("/reset")
def reset(req: ResetRequest):
    env = EmailTriageEnv(task_level=req.task_level)
    obs = env.reset()
    envs[req.session_id] = env
    return {"observation": obs.dict()}

@app.post("/step")
def step(req: StepRequest):
    env = envs.get(req.session_id)
    if not env:
        return {"error": "Session not found. Call /reset first."}
    action = Action(label=req.label)
    obs, reward, done = env.step(action)
    return {
        "observation": obs.dict() if obs else None,
        "reward": reward.dict(),
        "done": done
    }

@app.get("/state/{session_id}")
def state(session_id: str):
    env = envs.get(session_id)
    if not env:
        return {"error": "Session not found."}
    return env.state()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
