from invoke.tasks import task   # type: ignore
from invoke.context import Context


@task
def clean(c: Context):
    """Clean build artifacts."""
    file_patterns = [
        ".__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.log",
        "dist",
        "*.egg-info",
    ]
    for pattern in file_patterns:
        c.run(f"find . -name '{pattern}' -exec rm -rf {{}} +", warn=True)

@task
def setup(c: Context):
    """Set up the development environment."""
    c.run("pip install -e .")

@task
def build(c: Context):
    """Build the package."""
    c.run("rm -rf dist")
    c.run("python -m pip install --upgrade build twine")
    c.run("python -m build")
