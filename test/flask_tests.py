import os
from pathlib import Path
from src.generators.pygen import generate  # import your generator

BASE_DIR = Path(__file__).resolve().parent / "examples/simple/python/cmd_variants/flask_test_examples"

# TODO: fix problem where it tries to use relative path for requirements.txt
# TODO: figure out if each one is actuslly correct...
def run_examples():
    for case_dir in sorted(BASE_DIR.iterdir()):
        if case_dir.is_dir():
            print(f"\n=== Running {case_dir.name} ===")
            output = os.path.join(case_dir, "Dockerfile")
            try:
                dockerfile = generate(str(case_dir))
                with open(output, "w") as f:
                    f.write(dockerfile)
                print(f"✅ Dockerfile written to {output}")
            except Exception as e:
                print(f"❌ Failed for {case_dir.name}: {e}")

if __name__ == "__main__":
    run_examples()
