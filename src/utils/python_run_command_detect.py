import os

def check_for_django(py_files: list, requirements: list) -> tuple[bool, list]:
    for file in py_files:
        if os.path.basename(file) == "manage.py":
            if "gunicorn" in requirements:
                return True, ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
            return True, ["python", "manage.py", "runserver", "0.0.0.0:8000"]
        
    return False, []

def check_for_flask_app(py_files: list, requirements: list) -> tuple[bool, list]:
    for file in py_files:
        if "app = Flask(" in open(file).read():
            if os.path.basename(file) == "__init__.py":
                package = os.path.basename(os.path.dirname(file))
                if "gunicorn" in requirements:
                    return True, ["gunicorn", f"{package}:app", "--bind", "0.0.0.0:5000"]
                else:
                    return True, ["flask", "run", "--host=0.0.0.0", "--app", package]
            else:
                module = os.path.splitext(os.path.basename(file))[0]
                if "gunicorn" in requirements:
                    return True, ["gunicorn", f"{module}:app", "--bind", "0.0.0.0:5000"]
                else:
                    return True, ["python", file]
    return False, []

def check_for_fastapi(py_files: list, requirements: list) -> tuple[bool, list]:
    for file in py_files:
        content = open(file, "r", encoding="utf-8").read()
        if "from fastapi import FastAPI" in content or "from starlette" in content:
            module = os.path.splitext(os.path.basename(file))[0]
            return True, ["uvicorn", f"{module}:app", "--host", "0.0.0.0", "--port", "8000"]
    return False, []

def check_for_celery(py_files: list, requirements: list) -> tuple[bool, list]:
    for file in py_files:
        content = open(file, "r", encoding="utf-8").read()
        if "from celery import Celery" in content:
            module = os.path.splitext(os.path.basename(file))[0]
            return True, ["celery", "-A", module, "worker", "--loglevel=info"]
    return False, []

def check_for_jupyter(start_dir: str) -> tuple[bool, list]:
    jupyter_files = []
    for root, dirs, files in os.walk(start_dir):
        ipynb_files = [os.path.join(root, file) for file in files if file.endswith('.ipynb')]
        jupyter_files.extend(ipynb_files)
        
    if len(jupyter_files) > 0:
        return True, ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
    else:
        return False, []


def file_is_main(file: str) -> bool:
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            if 'if __name__ == "__main__":' in line.strip():
                return True
    return False

def check_for_main_file(py_files: list):
    for file in py_files:
        if file_is_main(file):
            return True, file
    return False, ""

def list_python_files(start_dir):
    all_files = []
    for root, dirs, files in os.walk(start_dir):
        py_files = [os.path.join(root, file) for file in files if file.endswith('.py')]
        all_files.extend(py_files)
    return all_files

def parse_pyproject_dependencies(path: str):
    import tomllib

    with open(path, "rb") as f:
        data = tomllib.load(f)

    # Case 1: PEP 621 standard
    if "project" in data and "dependencies" in data["project"]:
        return data["project"]["dependencies"]

    # Case 2: Poetry
    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    return [
        f"{pkg}{ver if ver != '*' else ''}"
        for pkg, ver in poetry_deps.items()
        if pkg.lower() != "python"
    ]
    
def parse_requirements_file_dependencies(path: str):
    reqs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                reqs.append(line)
    return reqs

def load_requirements(path=os.getcwd(), deps_type="requirements.txt"):
    deps_filepath = os.path.join(path, deps_type)
    if deps_type == "pyproject.toml":
        return parse_pyproject_dependencies(deps_filepath)
    else:
        return parse_requirements_file_dependencies(deps_filepath)

def determine_command(path: str, deps_type: str) -> list:
    project_files = list_python_files(path)
    is_flask_app, flask_cmd = check_for_flask_app(project_files, load_requirements(path, deps_type)) # TODO: be compatible with project.toml 
    if is_flask_app:
        return flask_cmd
    else:
        is_django_app, django_cmd = check_for_django(project_files, load_requirements(path, deps_type))
        if is_django_app:
            return django_cmd
        else:
            is_fastapi_app, fastapi_cmd = check_for_fastapi(project_files, load_requirements(path, deps_type))
            if is_fastapi_app:
                return fastapi_cmd
            else:
                is_celery_app, celery_cmd = check_for_celery(project_files, load_requirements(path, deps_type))
                if is_celery_app:
                    return celery_cmd
                else:
                    is_jupyter_app, jupyter_cmd = check_for_jupyter(path)
                    if is_jupyter_app:
                        return jupyter_cmd
                    else:
                        has_main, main_file = check_for_main_file(project_files)
                        if has_main:
                            return ["python", f"{os.path.relpath(main_file, path)}"]
                        else:
                            return ["python", "main.py"]

                        
def double_quote_list(ugly_list: list) -> str:
    quoted_elements = [f'"{item}"' for item in ugly_list]
    elements_string = ", ".join(quoted_elements)
    list_as_string_with_double_quotes = f"[{elements_string}]"
    return list_as_string_with_double_quotes

    

def detect(path: str, deps_type: str, keep_alive: bool) -> str:    
    if keep_alive:
        alive_base = ["sh", "-c"]
        alive_base.extend(determine_command(path, deps_type))
        alive_base[-1] = alive_base[-1] + " & tail -f /dev/null"
        return f"""
            CMD {double_quote_list(alive_base)}
        """
    else:
        return f"""
            CMD {double_quote_list(determine_command(path, deps_type))}
        """
