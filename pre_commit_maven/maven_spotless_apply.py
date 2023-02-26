import argparse
import os
import os.path
from pre_commit_maven.utils import generic_main
from pre_commit_maven.utils import shell
from pre_commit_maven.utils.shell import ExecutionResult

CWD = os.getcwd()
ENV = os.environ.copy()
GREP_FILTER_AND_CLEAN = "grep .java$ | tr '\\n' \' \' | rev | cut -c 2- | rev"
GIT_DIFF_MODIFIED_ONLY = f"git diff --cached --name-only --diff-filter=M | {GREP_FILTER_AND_CLEAN}"
GIT_DIFF_ADDED_MODIFIED = f"git diff --cached --name-only --diff-filter=AM | {GREP_FILTER_AND_CLEAN}"
DINCLUDES_ADDED_MODIFIED = f"-Dincludes=\'$(git diff --cached --name-only --diff-filter=AM | {GREP_FILTER_AND_CLEAN})\'"



def main(cwd=CWD, print_fn=print, execute_fn=generic_main.execute) -> int:
    return_code = execute_fn(["spotless:apply", f"-Dincludes=\'$({GIT_DIFF_ADDED_MODIFIED})\'"], cwd)
    return auto_fix_and_add(return_code, cwd=cwd)

def auto_fix_and_add(previous_return_code, cwd=CWD):
    # Important that following command is MODIFIED filter only!
    result = ExecutionResult(previous_return_code, "", "")
    modified_files =  shell.execute_direct(GIT_DIFF_MODIFIED_ONLY, cwd=cwd, env=ENV)
    print(f"ran modified files got {modified_files.stdout} and {modified_files.stderr}")
    if modified_files.stdout != '':
        shell.execute_direct("git add " + modified_files.stdout)
        return result.return_code
    return result.return_code

if __name__ == "__main__":
    exit(main())
