import sys

from .base_image_utils import base_gpu_image_util
from . import dependency_utils 

def system_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor
    return f"{major}.{minor}"

def determine_base_image(requirements_filepath: str, deps_type: str):
    requirements = dependency_utils.load_requirements(requirements_filepath, deps_type)
    gpu_image_needed, gpu_image = base_gpu_image_util.needs_compute(requirements)
    
    if gpu_image_needed:
        return gpu_image
    else:
        python_version = system_python_version()
        return f"python:{python_version}-slim"
    