import disclog
import toml


def test_version():
    with open("pyproject.toml", "r") as f:
        pyproject = toml.load(f)
        version = pyproject["tool"]["poetry"]["version"]
    assert disclog.__version__ == version
