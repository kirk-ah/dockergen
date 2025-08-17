FROM python:3.12-slim as build
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY . /app

# Set up python venv for container
RUN python3 -m venv /opt/dockerenv
ENV PATH="/opt/dockerenv/bin:$PATH"

# Install system deps for pip requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "myproject:app", "--bind", "0.0.0.0:5000"]