import subprocess
import os

REPO_PATH = "/Users/jeanheberth/Documents/GitClone/API/agenteqaIA/agenteqaIA" # Defina o caminho do repositório aqui

import subprocess

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"Erro ao executar: {command}\n{result.stderr}")
    else:
        print(result.stdout)

def git_commit():
    commit_message = input("Digite a mensagem do commit: ")

    print("\nAdicionando arquivos ao commit...")
    run_command("git add .")

    print(f"\nRealizando commit com a mensagem: {commit_message}...")
    run_command(f"git commit -m \"{commit_message}\"")

    print("\nCommit e push realizados com sucesso!")

if __name__ == "__main__":
    git_commit()
