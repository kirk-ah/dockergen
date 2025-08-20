import requests
import re
import subprocess

# todo: check

MAX_CUDA_VERSION = "12.2"

MISC_GPU_DEPS = ["jax", "rapids"]

pytorch_to_cuda_compatibility_map = {
  "2.2": ["12.1", "11.8"],
  "2.1": ["12.1", "11.8"],
  "2.0.1": ["11.8", "11.7"],
}

def get_latest_pytorch_version():
    url = "https://pypi.org/pypi/torch/json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["info"]["version"]

def get_latest_tensorflow_version():
    url = "https://pypi.org/pypi/tensorflow/json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["info"]["version"]

def find_version_for_gpu_pip_dep(dependencies: list, specific_dependency: str):
    """
    dependencies: list of strings like ["flask", "torch", "torch==2.1.0"]
    returns: ("torch", version) where version is None if unpinned
    """
    for dep in dependencies:
        # Exact match "torch" (unpinned)
        if dep.strip().lower() == f"{specific_dependency}":
            return True, "any"

        # Match "torch==<version>"
        match = re.match(fr"{specific_dependency}==([\d\.]+)", dep.strip().lower())
        if match:
            return True, match.group(1)

    return False, "none"  # torch not found

def pick_cuda_version(torch_version, cuda_max=MAX_CUDA_VERSION):
    options = pytorch_to_cuda_compatibility_map.get(torch_version, [])
    for cuda_ver in options:
        if float(cuda_ver) <= float(cuda_max):
            return cuda_ver
    return options[0] if options else MAX_CUDA_VERSION

def get_cuda_version():
    try:
        output = subprocess.check_output(["nvidia-smi"], encoding="utf-8")
        match = re.search(r"CUDA Version:\s+(\d+\.\d+)", output)
        if match:
            return match.group(1)
    except Exception as e:
        return None

def check_other_gpu_deps(dependencies: list):
    for lib in MISC_GPU_DEPS:
        dep_present, _ = find_version_for_gpu_pip_dep(dependencies, lib)
        if dep_present:
            return True
    return False

def needs_compute(requirements: list):
    is_torch, torch_ver = find_version_for_gpu_pip_dep(requirements, "torch")
    is_tensorflow, tensorflow_ver = find_version_for_gpu_pip_dep(requirements, "tensorflow")
    is_other_gpu_requirement = check_other_gpu_deps(requirements)
    if is_torch:
        if torch_ver == "any":
            return True, f"pytorch/pytorch:{get_latest_pytorch_version()}-cuda{pick_cuda_version(get_latest_pytorch_version())}-runtime"
        else:
            return True, f"pytorch/pytorch:{torch_ver}-cuda{pick_cuda_version(torch_ver)}-runtime"
    elif is_tensorflow:
        if tensorflow_ver == "any":
            return True, f"tensorflow/tensorflow:{get_latest_tensorflow_version()}-gpu"
        else:
            return True, f"tensorflow/tensorflow:{tensorflow_ver}-gpu"
    elif is_other_gpu_requirement:
        if get_cuda_version() is None:
            return True, f"nvidia/cuda:{get_cuda_version()}-runtime-ubuntu22.04"
        else:
            return True, f"nvidia/cuda:{MAX_CUDA_VERSION}-runtime-ubuntu22.04"
    else:
        return False, ""