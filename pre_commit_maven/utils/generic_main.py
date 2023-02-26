import argparse
import os.path
from pre_commit_maven.utils import maven


def execute(goals: list, cwd: str, maven_helper=maven):
    execution_result = maven_helper.execute(goals, cwd)
    if execution_result.return_code != 0:
        print(execution_result.stderr)
        maven_helper.print_error(execution_result)

    return execution_result.return_code
