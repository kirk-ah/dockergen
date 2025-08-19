FROM python:3.12-slim as build
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY . /app

# Set up python venv for container
RUN python3 -m venv /opt/dockerenv
ENV PATH="/opt/dockerenv/bin:$PATH"

# Install system deps for pip requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]