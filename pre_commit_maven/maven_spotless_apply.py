import argparse
import os
import os.path
from pre_commit_maven.utils import generic_main
from pre_commit_maven.utils import shell

CWD = os.getcwd()
ENV = os.environ.copy()

def main(cwd=CWD, print_fn=print, execute_fn=generic_main.execute) -> int:
    result = execute_fn(["spotless:apply"], cwd)
    print(f"ran spotless apply got {result.stdout} and {result.stderr}")
    # Important that following command is MODIFIED filter only!
    modified_files =  shell.execute_direct("git diff --cached --name-only --diff-filter=M | tr '\n' ' '| rev | cut -c 2- | rev", cwd=cwd, env=ENV)
    print(f"ran modified files got {modified_files.stdout} and {modified_files.stderr}")
    if modified_files.stdout != '':
        shell.execute_direct("git add " + modified_files.stdout)
        result = shell.execute_direct("git commit -m \"spotless apply auto-commit\"")
        print(f"ran commit got {result.stdout} and {result.stderr}")
        return result
    return result


if __name__ == "__main__":
    exit(main())
