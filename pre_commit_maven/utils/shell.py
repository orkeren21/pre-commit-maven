import subprocess
from subprocess import CalledProcessError


class ExecutionResult:
    return_code: int
    stdout: str
    stderr: str

    def __init__(self, return_code, stdout, stderr):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr


def execute(cmd: list, **kwargs):
    assert cmd is not None and len(cmd) > 0, "cmd is empty"

    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    kwargs.setdefault("universal_newlines", True)
    kwargs.setdefault("shell", True)
    kwargs.setdefault("bufsize", 1)

    process = subprocess.Popen(" ".join(cmd), **kwargs)
    stdout, stderr = process.communicate()

    return ExecutionResult(process.returncode, stdout, stderr)
