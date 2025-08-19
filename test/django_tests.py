import os
from pathlib import Path
from src.generators.pygen import generate 
from test.utils import test_dockerfile_correctness
import requests

DJANGO_DIR = Path(__file__).resolve().parent / "examples/simple/python/cmd_variants/django_project"    

def django_check(url: str) -> bool:
    try:
        r = requests.get(url)
        return "Hello from Django" in r.text
    except Exception:
        return False
    
def run_examples():
    print(f"\n=== Running {DJANGO_DIR.name} ===")
    output = os.path.join(DJANGO_DIR, "Dockerfile")
    try:
        dockerfile = generate(str(DJANGO_DIR))
        with open(output, "w") as f:
            f.write(dockerfile)
        test_dockerfile_correctness(DJANGO_DIR, DJANGO_DIR.name, django_check, endpoint="http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Failed for {DJANGO_DIR.name}: {e}")

if __name__ == "__main__":
    run_examples()
