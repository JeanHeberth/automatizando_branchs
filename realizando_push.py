import subprocess
import os

REPO_PATH = "/Users/jeanheberth/Documents/GitClone/AutomacaoPW/saucelabs"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"❌ Erro ao executar: {command}\n{result.stderr}")
    else:
        print(result.stdout)
    return result

def get_current_branch():
    result = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    return result.stdout.strip()

def has_changes_to_commit():
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    return result.stdout.strip() != ""

def git_commit_push():
    if not has_changes_to_commit():
        print("⚠️ Nenhuma alteração detectada para commit/push.")
        return

    commit_message = input("Digite a mensagem do commit: ").strip()
    if not commit_message:
        print("⚠️ Mensagem de commit não pode estar vazia.")
        return

    print("\n📦 Adicionando arquivos ao commit...")
    run_command("git add .")

    print(f"\n📝 Realizando commit com a mensagem: \"{commit_message}\"...")
    run_command(f"git commit -m \"{commit_message}\"")

    current_branch = get_current_branch()
    print(f"\n🚀 Enviando alterações para a branch remota '{current_branch}'...")
    run_command(f"git push origin {current_branch}")

    print("\n✅ Commit e push realizados com sucesso!")

if __name__ == "__main__":
    git_commit_push()
