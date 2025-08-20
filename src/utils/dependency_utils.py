import os

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