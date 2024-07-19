import os
import subprocess
from pathlib import Path

import fire

from r2e.paths import REPOS_DIR
from r2e.repo_builder.repo_args import RepoArgs


def main(repo_args: RepoArgs):
    if not repo_args.repo_name:
        raise ValueError("Please provide the repository name using --repo_name argument.")

    repo_path = REPOS_DIR / repo_args.repo_name

    if not repo_path.exists():
        raise ValueError("Please provide a valid repo name. {} does not exist locally".format(repo_args.repo_name))

    with open("r2e/repo_builder/docker_builder/r2e_base_dockerfile.txt", "r") as f:
        dockerfile = f.read()

    dockerfile += f"COPY . /{repo_args.repo_name}\n\n"

    dockerfile += f"WORKDIR /install_code\n\n"

    dockerfile += f"RUN pip install -r requirements.txt\n\n"

    dockerfile += f"RUN python3 one_on_one_installer.py {repo_args.repo_name}\n\n"
    
    output_dockerfile_path = "r2e/repo_builder/docker_builder/r2e_final_dockerfile.dockerfile"
    
    with open(output_dockerfile_path, "w") as f:
        f.write(dockerfile)
    
    print(f"\nDockerfile created at path {os.path.abspath(output_dockerfile_path)}")

if __name__ == "__main__":
    repo_args = fire.Fire(RepoArgs)
    main(repo_args)

