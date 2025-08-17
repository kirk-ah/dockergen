import click

from src.detectors import python_detector 
from src.generators import pygen

@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--skip-sysdeps", is_flag=True, help="Skip system dependencies inference")
@click.option("--keep-alive", is_flag=True, help="Keep container running after start")
@click.option("--output", "-o", default="Dockerfile", help="Output Dockerfile name")
def main(path, skip_sysdeps, keep_alive, output):
    # Step 1: Detect project type
    if python_detector.detect(path):
        include_sysdeps = not skip_sysdeps
        dockerfile = pygen.generate(path, keep_alive=keep_alive, include_sysdeps=include_sysdeps)
    else:
        click.echo("❌ Could not detect project type")
        return

    # Step 2: Write Dockerfile
    with open(output, "w") as f:
        f.write(dockerfile)
    click.echo(f"✅ Dockerfile written to {output}")
    
if __name__ == "__main__":
    main() 