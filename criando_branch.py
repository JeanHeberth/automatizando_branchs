import subprocess
import os

REPO_PATH = "/Users/jeanheberth/Documents/GitClone/API/usuario"  # Defina o caminho do repositório aqui
branch_developer = "develop"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"Erro ao executar: {command}\n{result.stderr}")
    else:
        print(result.stdout)

def automate_git_workflow():
    branch_name = input("Digite o nome da nova branch: ")
    feature_branch = f"feature/{branch_name}"

    print("\nTrocando para a branch main...")
    run_command("git checkout main")

    print("\nExcluindo todas as branches locais, exceto main...")
    run_command("git branch | grep -v 'main' | xargs git branch -D")

    print("\nAtualizando a branch main...")
    run_command("git pull")

    print(f"\nCriando e trocando para a nova branch {feature_branch}...")
    run_command(f"git checkout -b {feature_branch}")

    print(f"\nAtualizando a nova branch com a {branch_developer}...")
    run_command(f"git pull origin {branch_developer}")

    print("\nProcesso concluído!")

if __name__ == "__main__":
    automate_git_workflow()
