import os
import textwrap
import sys

from src.utils import pip_sys_generation, python_venv_generation, python_run_command_detect

def system_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor

    return f"{major}.{minor}"


def generate(path: str, include_sysdeps=True, keep_alive=False) -> str:
    if "requirements.txt" in os.listdir(path):
        deps = "requirements.txt"
    elif "pyproject.toml" in os.listdir(path):
        deps = "pyproject.toml"
    else:
        deps = None

    python_version = system_python_version()
    base = f"python:{python_version}-slim"

    dockerfile = textwrap.dedent(f"""
        FROM {base} as build
        ENV DEBIAN_FRONTEND=noninteractive
        WORKDIR /app
        COPY . /app
    """)
    
    dockerfile += textwrap.dedent(python_venv_generation.set_venv())

    if deps == "requirements.txt":
        if include_sysdeps:
            dockerfile += textwrap.dedent(pip_sys_generation.generate_from_reqs_file(f"{path}/requirements.txt"))
        dockerfile += textwrap.dedent("""
            RUN pip install --no-cache-dir -r requirements.txt
        """)
    elif deps == "pyproject.toml":
        dockerfile += textwrap.dedent("""
            RUN pip install --no-cache-dir poetry && poetry install --no-root
        """)
      
    dockerfile += textwrap.dedent(python_run_command_detect.detect(f"{path}", deps, keep_alive))


    return dockerfile.strip()
