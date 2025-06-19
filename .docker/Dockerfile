FROM python:3.10-slim


WORKDIR /code

# System dependencies
RUN apt-get update && apt-get install -y \
    espeak \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /code/requirements.txt


# Install Python dependencies globally (inside the image)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt  && \
    pip install "fastapi[standard]"

# Copy models
COPY ./download /code/download

# Copy app files
COPY ./app /code/app

# Expose the FastAPI port
EXPOSE 8080

# Run the app without activating any venv
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
