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
    cargo \
    gfortran \
    libblas-dev \
    libjpeg-dev \
    liblapack-dev \
    libpq5 \
    libpng-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
    rustc \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "my_app:app", "--bind", "0.0.0.0:5000"]