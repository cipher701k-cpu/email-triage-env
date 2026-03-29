# Email Triage Environment

## Description
An OpenEnv-compatible environment where AI agents practice triaging emails into three categories: **urgent**, **normal**, or **spam**.

This simulates a real task that office workers do daily.

## Action Space
- `urgent` — needs immediate attention
- `normal` — regular email, no rush
- `spam` — unwanted/junk email

## Observation Space
- `email_id` — index of current email
- `subject` — email subject line
- `body` — email body text
- `task_level` — difficulty level

## Tasks
| Task | Difficulty | Description |
|------|-----------|-------------|
| easy | Easy | Clearly written emails |
| medium | Medium | Moderately ambiguous emails |
| hard | Hard | Tricky, vague emails |

## Baseline Scores
| Task | Score |
|------|-------|
| easy | 0.80 |
| medium | 0.60 |
| hard | 0.40 |

## Setup
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
