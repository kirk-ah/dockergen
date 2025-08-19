import subprocess
import time
import requests
def build_image(image_name: str, project_dir: str) -> bool:
    try:
        result = subprocess.run(["docker", "build", "-t", f"{image_name}", "."], cwd=f"{project_dir}", capture_output=True, text=True)
        if result.returncode != 0:
            print("Subprocess error building docker image -- test failed")
            print(f"{result.stderr}")
            return False
        else:
            print(f"Successfully build image {image_name}")
            return True
    except Exception as e:
        print(f"Test Failed: Python exception building docker image: {image_name} -- {e}")
        remove_image(image_name)
        return False

def remove_image(image_name: str) -> bool:
    try:
        subprocess.run(["docker", "rmi", f"{image_name}:latest"], capture_output=True, text=True)
    except Exception as e:
        print(f"Python exception removing docker image: {image_name} -- {e}")
        
def run_and_test_image(image_name: str, check_function, timeout: int = 20, endpoint: str = "http://127.0.0.1:5000/") -> bool:
    container_name = f"test_{image_name}"
    try:
        run_result = subprocess.run(
            ["docker", "run", "-d", "--rm", "--name", container_name, "--network=host", f"{image_name}:latest"],
            capture_output=True,
            text=True,
        )
        if run_result.returncode != 0:
            print("❌ Failed to start container -- test failed")
            print(run_result.stderr)
            return False
        
        try:
        # Poll until check_fn passes or timeout
            start = time.time()
            while time.time() - start < timeout:
                if check_function(endpoint):
                    print(f"✅ {image_name} container is responding -- test passed!")
                    return True
                time.sleep(2)
            print(f"❌ {image_name} container did not respond in time -- test failed")
            return False
        finally:
            # Cleanup
            subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
            remove_image(image_name)
    finally:
        # Always stop the container
        subprocess.run(["docker", "stop", container_name], capture_output=True, text=True)
        remove_image(image_name)

def test_dockerfile_correctness(project_dir: str, image_name: str, check_function, endpoint: str = "127.0.0.1:5000"):
    if not build_image(image_name, project_dir):
        return
        
    if not run_and_test_image(image_name, check_function=check_function, endpoint=endpoint):
        return
        
    remove_image(image_name)     
