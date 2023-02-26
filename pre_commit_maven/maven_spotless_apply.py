import argparse
import os
import os.path
from pre_commit_maven.utils import generic_main
from pre_commit_maven.utils import shell
from pre_commit_maven.utils.shell import ExecutionResult

CWD = os.getcwd()
ENV = os.environ.copy()

def main(cwd=CWD, print_fn=print, execute_fn=generic_main.execute) -> int:
    return_code = execute_fn(["spotless:apply"], cwd)
    return autoFixAndCommit(return_code, cwd=cwd)

def autoFixAndCommit(previousReturnCode, cwd=CWD):
    # Important that following command is MODIFIED filter only!
    result = ExecutionResult(previousReturnCode, "", "")
    modified_files =  shell.execute_direct("git diff --cached --name-only --diff-filter=M | grep .java$ | tr '\\n' ' '| rev | cut -c 2- | rev", cwd=cwd, env=ENV)
    print(f"ran modified files got {modified_files.stdout} and {modified_files.stderr}")
    if modified_files.stdout != '':
        shell.execute_direct("git add " + modified_files.stdout)
        return result.return_code
    return result.return_code

if __name__ == "__main__":
    exit(main())
