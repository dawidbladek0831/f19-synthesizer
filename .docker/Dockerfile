FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    espeak \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy models
COPY download /download

# Copy app files
COPY app /app
COPY requirements.txt .


# Install Python dependencies globally (inside the image)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt  && \
    pip install "fastapi[standard]"

# Expose the FastAPI port
EXPOSE 80

# Run the app without activating any venv
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
