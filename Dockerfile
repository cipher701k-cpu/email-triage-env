FROM python:3.10-slim

# 1. Set the working directory
WORKDIR /app

# 2. Copy dependency files first (for faster building)
COPY requirements.txt .
COPY pyproject.toml .
# If you have uv.lock, uncomment the next line:
# COPY uv.lock .

# 3. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir .

# 4. Copy the rest of the project (including the 'server' folder)
COPY . .

# 5. Set the Port for Hugging Face (7860 is the default)
ENV PORT=7860
EXPOSE 7860

# 6. Start the server using the entry point defined in pyproject.toml
# This matches 'server = "server.app:main"'
CMD ["python", "-m", "server.app"]
