import os

def detect(path: str) -> bool:
    files = os.listdir(path)
    return any(f in files for f in ["requirements.txt", "pyproject.toml", "Pipfile"])