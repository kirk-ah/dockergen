import os
from pathlib import Path
from src.generators.pygen import generate  # import your generator
from test.utils import test_dockerfile_correctness
import requests

BASE_DIR = Path(__file__).resolve().parent / "examples/simple/python/cmd_variants/flask_test_examples"    

def flask_health_check(url: str):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except Exception:
        return False
    
def run_examples():
    for case_dir in sorted(BASE_DIR.iterdir()):
        if case_dir.is_dir():
            print(f"\n=== Running {case_dir.name} ===")
            output = os.path.join(case_dir, "Dockerfile")
            try:
                dockerfile = generate(str(case_dir))
                with open(output, "w") as f:
                    f.write(dockerfile)
                test_dockerfile_correctness(case_dir, case_dir.name, flask_health_check, endpoint="http://127.0.0.1:5000")
            except Exception as e:
                print(f"❌ Failed for {case_dir.name}: {e}")

if __name__ == "__main__":
    run_examples()
