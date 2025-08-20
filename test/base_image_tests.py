from pathlib import Path
import os
import sys
import re

from src.generators.pygen import generate  # import your generator
from src.utils.base_image_utils.base_gpu_image_util import get_latest_pytorch_version, get_latest_tensorflow_version, pick_cuda_version

BASE_CASE_DIR = Path(__file__).resolve().parent / "examples/simple/python/base"    
CMD_VARIANTS_DIR = Path(__file__).resolve().parent / "examples/simple/python/cmd_variants" 
BASE_VARIANTS = Path(__file__).resolve().parent / "examples/simple/python/base_variants" 

def find_dgcase_dirs(start_path):
    matches = []
    for root, dirs, _ in os.walk(start_path):
        for d in dirs:
            if d.startswith("dgCase"):
                matches.append(os.path.abspath(os.path.join(root, d)))
    return matches

def find_specific_dgcase_dirs(start_path: str, start_str: str):
    matches = []
    for root, dirs, _ in os.walk(start_path):
        for d in dirs:
            if d.startswith(f"{start_str}"):
                matches.append(os.path.abspath(os.path.join(root, d)))
    return matches

def get_base_image(dockerfile_str):
    match = re.search(r"^FROM\s+([^\s]+)", dockerfile_str, flags=re.MULTILINE | re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def system_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor
    return f"{major}.{minor}"

def test_all_base_images():
    failed = 0
    for base_case_dir in find_dgcase_dirs(BASE_CASE_DIR):
        dockerfile = generate(base_case_dir, include_sysdeps=False) # skip ai query since we dont build
        python_version = system_python_version()
        if get_base_image(dockerfile) != f"python:{python_version}-slim":
            failed += 1
            print(f"Test failed for {base_case_dir}: expected python:{python_version}-slim but got {get_base_image(dockerfile)}")
            
    for cmd_variant_dir in find_dgcase_dirs(CMD_VARIANTS_DIR):
        dockerfile = generate(cmd_variant_dir, include_sysdeps=False) # skip ai query since we dont build
        python_version = system_python_version()
        if get_base_image(dockerfile) != f"python:{python_version}-slim":
            failed += 1
            print(f"Test failed for {cmd_variant_dir}: expected python:{python_version}-slim but got {get_base_image(dockerfile)}")
       
    # manually check the specific gpu ones
    dockerfile = generate(Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_tensorflow_no_version", include_sysdeps=False)
    if get_base_image(dockerfile) != f"tensorflow/tensorflow:{get_latest_tensorflow_version()}-gpu":
        failed += 1
        print(f"Test failed for {Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_tensorflow_no_version"}: expected tensorflow/tensorflow:{get_latest_tensorflow_version()}-gpu but got {get_base_image(dockerfile)}")
        
    dockerfile = generate(Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_tensorflow_with_version", include_sysdeps=False)
    if get_base_image(dockerfile) != "tensorflow/tensorflow:2.18.0-gpu":
        failed += 1
        print(f"Test failed for {Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_tensorflow_with_version"}: expected tensorflow/tensorflow:2.18.0-gpu but got {get_base_image(dockerfile)}")
      
    dockerfile = generate(Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_torch_no_version", include_sysdeps=False)
    if get_base_image(dockerfile) != f"pytorch/pytorch:{get_latest_pytorch_version()}-cuda{pick_cuda_version(get_latest_pytorch_version())}-runtime":
        failed += 1
        print(f"Test failed for {Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_torch_no_version"}: expected pytorch/pytorch:{get_latest_pytorch_version()}-cuda{pick_cuda_version(get_latest_pytorch_version())}-runtime but got {get_base_image(dockerfile)}")
        
    dockerfile = generate(Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_torch_with_version", include_sysdeps=False)
    if get_base_image(dockerfile) != f"pytorch/pytorch:2.2-cuda{pick_cuda_version("2.2")}-runtime":
        failed += 1
        print(f"Test failed for {Path(__file__).resolve().parent / "examples/simple/python/base_variants/gpu/dgCase_torch_with_version"}: expected pytorch/pytorch:2.2-cuda{pick_cuda_version("2.2")}-runtime but got {get_base_image(dockerfile)}")
  
    if failed == 0:
        print("All base image tests passed!")
    


            
    
    
