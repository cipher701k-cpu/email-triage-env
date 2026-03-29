from environment import EmailTriageEnv, Action

def run_grader(task_level: str, actions: list) -> float:
    env = EmailTriageEnv(task_level=task_level)
    env.reset()
    total_score = 0.0
    num_emails = len(env.emails)

    for i in range(num_emails):
        if i < len(actions):
            action = Action(label=actions[i])
        else:
            action = Action(label="normal")
        _, reward, done = env.step(action)
        total_score += reward.score
        if done:
            break

    final_score = round(total_score / num_emails, 4)
    return final_score

def grade_easy(actions: list) -> float:
    return run_grader("easy", actions)

def grade_medium(actions: list) -> float:
    return run_grader("medium", actions)

def grade_hard(actions: list) -> float:
    return run_grader("hard", actions)

if __name__ == "__main__":
    easy_answers = ["urgent", "spam", "normal", "urgent", "spam"]
    medium_answers = ["urgent", "normal", "spam", "urgent", "normal"]
    hard_answers = ["urgent", "normal", "spam", "urgent", "normal"]
    print(f"Easy score: {grade_easy(easy_answers)}")
    print(f"Medium score: {grade_medium(medium_answers)}")
    print(f"Hard score: {grade_hard(hard_answers)}")
