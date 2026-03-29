import os
from openai import OpenAI
from environment import EmailTriageEnv, Action

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=API_BASE_URL)

def get_ai_label(subject: str, body: str) -> str:
    prompt = f"""You are an email triage assistant.
Classify this email as exactly one of: urgent, normal, spam

Subject: {subject}
Body: {body}

Reply with only one word: urgent, normal, or spam"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0
    )
    label = response.choices[0].message.content.strip().lower()
    if label not in ["urgent", "normal", "spam"]:
        label = "normal"
    return label

def run_task(task_level: str):
    env = EmailTriageEnv(task_level=task_level)
    obs = env.reset()
    total_score = 0.0
    steps = 0
    print(f"\n--- Task: {task_level.upper()} ---")
    while True:
        label = get_ai_label(obs.subject, obs.body)
        print(f"Email: '{obs.subject}' -> AI said: {label}")
        action = Action(label=label)
        obs, reward, done = env.step(action)
        total_score += reward.score
        steps += 1
        if done:
            break
    final = round(total_score / steps, 4)
    print(f"Score: {final}")
    return final

if __name__ == "__main__":
    scores = {}
    for level in ["easy", "medium", "hard"]:
        scores[level] = run_task(level)
    print("\n=== FINAL SCORES ===")
    for level, score in scores.items():
        print(f"{level}: {score}")
