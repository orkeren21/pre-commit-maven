import argparse
import os
import os.path
from pre_commit_maven.utils import generic_main
from pre_commit_maven.utils import shell
from pre_commit_maven.utils.shell import ExecutionResult
from pre_commit_maven.utils.maven import Colours

CWD = os.getcwd()
ENV = os.environ.copy()
ADDED_FILTER = "A"
MODIFIED_FILTER = "M"
GREP_FILTER_AND_CLEAN = "grep .java$ | tr '\\n' \' \' | rev | cut -c 2- | rev"
GIT_DIFF_MODIFIED_ONLY = f"git diff --cached --name-only --diff-filter={MODIFIED_FILTER} | {GREP_FILTER_AND_CLEAN}"
GIT_DIFF_ADDED_MODIFIED = f"git diff --cached --name-only --diff-filter={ADDED_FILTER}{MODIFIED_FILTER} | {GREP_FILTER_AND_CLEAN}"


def main(cwd=CWD, print_fn=print, execute_fn=generic_main.execute) -> int:
    print(f"{Colours.BOLD}{Colours.OKBLUE} Running spotless:apply on staged files")
    return_code = execute_fn(["spotless:apply", f"-Dincludes=\"$({GIT_DIFF_ADDED_MODIFIED})\""], cwd)
    return auto_fix_and_add(return_code, cwd=cwd)

def auto_fix_and_add(previous_return_code, cwd=CWD):
    # Important that following command is MODIFIED filter only!
    result = ExecutionResult(previous_return_code, "", "")
    modified_files =  shell.execute_direct(GIT_DIFF_MODIFIED_ONLY, cwd=cwd, env=ENV)
    if modified_files.stdout != '':
        file_list = modified_files.split(" ")
        print(f"{Colours.OKBLUE} Spotless modified these files: {', '.join(file_list)} \nAdding them to commit{Colours.ENDC}")
        shell.execute_direct("git add " + modified_files.stdout)
        print(f"{Colours.BOLD} {Colours.OKGREEN} Successfully added modified files {Colours.ENDC}")
        return result.return_code
    else:
        print(f"{Colours.OKBLUE} Spotless didn't modify any files{Colours.ENDC}")
    return result.return_code

if __name__ == "__main__":
    exit(main())
