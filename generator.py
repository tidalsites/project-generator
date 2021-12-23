import os, shutil, subprocess

# Ingest configuration file

cwd = os.getcwd()

# TODO: Proper error handling

# Helper function for subprocess
def execute_subprocess(command):
    subprocess.run(command, shell=True)

# Install github CLI
def install_gh():
    try:
        gh_version = 'curl "https://api.github.com/repos/cli/cli/releases/latest" | grep '"tag_name"''

        VERSION = subprocess.run(gh_version, shell=True, capture_output=True).stdout.decode("utf-8").strip()
        # TODO: Really need to find a better way to do this
        VERSION = VERSION.split(':')[1].replace("\"", "").replace(",", "").replace("v", "").strip()
        command = f'wget https://github.com/cli/cli/releases/download/v{VERSION}/gh_{VERSION}_linux_amd64.tar.gz'
        execute_subprocess(command)
        extract_tar = f'tar xvf gh_{VERSION}_linux_amd64.tar.gz'
        execute_subprocess(extract_tar)
        copy_tar = f'sudo cp gh_{VERSION}_linux_amd64/bin/gh /usr/local/bin/'
        execute_subprocess(copy_tar)
    except:
        print('Unable to install Github CLI')

# Pull template git repo
def pull_template():
    # modify to fork
    command = 'gh repo clone tidalsites/tidalsites-template'
    execute_subprocess(command)

# Login to Github CLI using token
def login_gh(token):
    try:
        # TODO: Find a way to pass token without writing file
        with open('token.txt', 'w') as f:
            f.write(token)
        command = f'gh auth login --with-token < token.txt'
        execute_subprocess(command)
    except:
        print('Unable to login to Github')

# Create new Github Repo with project name as argument
def create_gh_repo(project_name):
    try:
        command = f'gh repo create {project_name} --public'
        execute_subprocess(command)
    except Exception as e:
        print(f'Unable to create repo\nError: {e}')

def reset_git(directory):
    try:
        shutil.rmtree(os.path.join(cwd, directory, '.git'))
        print('Reset Git')
    except:
        print('Something went wrong when resetting git')


def update_local_repo(project_name):
    project_directory = os.path.join(cwd, 'tidalsites-template')
    git_init = 'git init'
    try:
        if(os.path.isdir(project_directory)):
            os.rename(project_directory, project_name)
            os.chdir(f'./{project_name}')
            execute_subprocess(git_init)
        else:
            print('Unable to find directory')
    except:
        print('Unable to update local repo')

# Push repo to newly created Github repo
def push_repo(project_name, token):
    commands = ["git add *",
    "git commit -m 'Initial commit'",
    f"git remote add origin https://{token}@github.com/tidalsites/{project_name}.git",
    "git branch -M main",
    "git push -u origin main"
    ]
    try:
        os.chdir(os.path.join(cwd, project_name))
        for command in commands:
            execute_subprocess(command)
    except:
        print('Unable to push to repo')

# Generator function to create new project
def generator(data, token):
    repo = data["project_name"]
    try:
        install_gh()
        login_gh(token)
        pull_template()
        reset_git('tidalsites-template')
        update_local_repo(repo)
        create_gh_repo(repo)
        push_repo(repo, token)
    except Exception as e:
        return e
