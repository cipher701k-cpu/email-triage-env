import random
from pydantic import BaseModel

class Observation(BaseModel):
    email_id: int
    subject: str
    body: str
    task_level: str

class Action(BaseModel):
    label: str

class Reward(BaseModel):
    score: float
    correct_label: str
    given_label: str

EMAILS = {
    "easy": [
        {"subject": "URGENT: Server is down!", "body": "Production server crashed. Fix immediately!", "label": "urgent"},
        {"subject": "Win a free iPhone!", "body": "Click here to claim your prize now!!!", "label": "spam"},
        {"subject": "Team lunch tomorrow", "body": "Lunch is at 1pm in the cafeteria tomorrow.", "label": "normal"},
        {"subject": "CRITICAL: Database breach", "body": "Unauthorized access detected. Immediate action required.", "label": "urgent"},
        {"subject": "You have won 1000000!", "body": "Send us your bank details to claim your prize.", "label": "spam"},
    ],
    "medium": [
        {"subject": "Follow up on project", "body": "The client called twice today. They seem very frustrated.", "label": "urgent"},
        {"subject": "Newsletter: Top 10 tips", "body": "This week: productivity hacks you never knew!", "label": "normal"},
        {"subject": "Unsubscribe failed", "body": "Your unsubscribe request failed. Buy our products now at 90% off!", "label": "spam"},
        {"subject": "Meeting rescheduled", "body": "The board meeting has been moved to tomorrow 9am due to emergency.", "label": "urgent"},
        {"subject": "Invoice 4521", "body": "Please find attached the invoice for last month services.", "label": "normal"},
    ],
    "hard": [
        {"subject": "Quick question", "body": "Hey, when you get a chance can you look into that thing we discussed? The client pinged again.", "label": "urgent"},
        {"subject": "Re: Re: Re: update", "body": "Sure sounds good. Let me know.", "label": "normal"},
        {"subject": "Important information inside", "body": "Dear user, your account needs verification. Click the link below.", "label": "spam"},
        {"subject": "FYI", "body": "The system will go down tonight at midnight for 6 hours. All teams must be notified.", "label": "urgent"},
        {"subject": "Checking in", "body": "Hi, just wanted to touch base about the quarterly numbers.", "label": "normal"},
    ]
}

class EmailTriageEnv:
    def __init__(self, task_level="easy"):
        self.task_level = task_level
        self.current_index = 0
        self.emails = []
        self.total_score = 0.0
        self.reset()

    def reset(self):
        self.emails = EMAILS[self.task_level].copy()
        random.shuffle(self.emails)
        self.current_index = 0
        self.total_score = 0.0
        return self._get_observation()

    def _get_observation(self):
        email = self.emails[self.current_index]
        return Observation(
            email_id=self.current_index,
            subject=email["subject"],
            body=email["body"],
            task_level=self.task_level
        )

    def step(self, action):
        correct = self.emails[self.current_index]["label"]
        given = action.label.lower().strip()
        if given == correct:
            score = 1.0
        elif given in ["urgent", "normal", "spam"]:
            score = 0.2
        else:
            score = 0.0
        self.total_score += score
        self.current_index += 1
        done = self.current_index >= len(self.emails)
        reward = Reward(score=score, correct_label=correct, given_label=given)
        obs = self._get_observation() if not done else None
        return obs, reward, done

    def state(self):
        return {
            "task_level": self.task_level,
            "current_index": self.current_index,
            "total_emails": len(self.emails),
            "total_score": self.total_score
        }
