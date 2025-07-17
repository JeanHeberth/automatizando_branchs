import os
import subprocess


def run_command(command, repo_path):
    result = subprocess.run(command, cwd=repo_path, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"❌ Erro ao executar: {command}\n{result.stderr}")
    else:
        print(result.stdout)
    return result

def get_default_branch(repo_path):
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            capture_output=True,
            text=True,
            cwd=repo_path
        )
        ref = result.stdout.strip()
        if ref:
            return ref.split("/")[-1]
    except subprocess.CalledProcessError:
        pass

    # Fallback: verifica presença de main/master
    result = subprocess.run(["git", "branch", "-r"], capture_output=True, text=True, cwd=repo_path)
    branches = result.stdout
    if "origin/main" in branches:
        return "main"
    elif "origin/master" in branches:
        return "master"
    else:
        raise Exception("❗ Não foi possível detectar a branch principal.")

def remote_branch_exists(repo_path, branch):
    result = subprocess.run(["git", "ls-remote", "--heads", "origin", branch],
                            capture_output=True, text=True, cwd=repo_path)
    return branch in result.stdout

def get_current_branch(repo_path):
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True, cwd=repo_path)
    return result.stdout.strip()

def has_changes_to_commit(repo_path):
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=repo_path)
    return result.stdout.strip() != ""

def delete_all_branches_except(repo_path, branch_to_keep):
    result = subprocess.run(["git", "branch"], capture_output=True, text=True, cwd=repo_path)
    local_branches = [b.strip().replace("* ", "") for b in result.stdout.strip().splitlines()]
    for branch in local_branches:
        if branch != branch_to_keep:
            run_command(f"git branch -D {branch}", repo_path)

# === FUNCIONALIDADES ===

def criar_branch(repo_path):
    try:
        branch_main = get_default_branch(repo_path)
        print(f"🔍 Branch principal detectada: {branch_main}")

        branch_name = input("Digite o nome da nova branch: ").strip()
        if not branch_name:
            print("⚠️ Nome da branch não pode estar vazio.")
            return

        feature_branch = f"feature/{branch_name}"

        print(f"\n🔄 Trocando para a branch {branch_main}...")
        run_command(f"git checkout {branch_main}", repo_path)

        print(f"\n🧹 Excluindo todas as branches locais, exceto {branch_main}...")
        delete_all_branches_except(repo_path, branch_main)

        print(f"\n⬇️ Atualizando a branch {branch_main}...")
        run_command("git pull", repo_path)

        print(f"\n🌱 Criando e trocando para a nova branch {feature_branch}...")
        run_command(f"git checkout -b {feature_branch}", repo_path)

        if remote_branch_exists(repo_path, "develop"):
            print(f"\n⬇️ Atualizando a nova branch com a develop...")
            run_command("git pull origin develop", repo_path)
        else:
            print("⚠️ Branch 'develop' não existe no remoto. Pulando pull da develop.")

        print("\n✅ Branch criada com sucesso!")

    except Exception as e:
        print(f"\n❗ Erro geral: {e}")

def fazer_commit(repo_path):
    if not has_changes_to_commit(repo_path):
        print("⚠️ Nenhuma alteração detectada para commit.")
        return

    commit_message = input("Digite a mensagem do commit: ").strip()
    if not commit_message:
        print("⚠️ Mensagem de commit não pode estar vazia.")
        return

    print("\n📦 Adicionando arquivos ao commit...")
    run_command("git add .", repo_path)

    print(f"\n📝 Realizando commit com a mensagem: \"{commit_message}\"...")
    run_command(f"git commit -m \"{commit_message}\"", repo_path)

    print("\n✅ Commit realizado com sucesso!")

def fazer_commit_e_push(repo_path):
    if not has_changes_to_commit(repo_path):
        print("⚠️ Nenhuma alteração detectada para commit/push.")
        return

    commit_message = input("Digite a mensagem do commit: ").strip()
    if not commit_message:
        print("⚠️ Mensagem de commit não pode estar vazia.")
        return

    print("\n📦 Adicionando arquivos ao commit...")
    run_command("git add .", repo_path)

    print(f"\n📝 Realizando commit com a mensagem: \"{commit_message}\"...")
    run_command(f"git commit -m \"{commit_message}\"", repo_path)

    current_branch = get_current_branch(repo_path)
    print(f"\n🚀 Enviando alterações para a branch remota '{current_branch}'...")
    run_command(f"git push origin {current_branch}", repo_path)

    print("\n✅ Commit e push realizados com sucesso!")

# === MENU INTERATIVO UNIVERSAL ===

def menu():
    print("📁 Automação Git Interativa (Mac / Linux / Windows)\n")

    repo_path = input("Digite o caminho completo do repositório Git: ").strip()
    if not os.path.isdir(repo_path):
        print("❌ Caminho inválido. Encerrando.")
        return

    while True:
        print("\nEscolha uma opção:")
        print("1 - Criar nova branch (workflow)")
        print("2 - Fazer apenas commit")
        print("3 - Fazer commit e push")
        print("4 - Sair")

        opcao = input("Digite o número da opção desejada: ").strip()

        if opcao == "1":
            criar_branch(repo_path)
        elif opcao == "2":
            fazer_commit(repo_path)
        elif opcao == "3":
            fazer_commit_e_push(repo_path)
        elif opcao == "4":
            print("👋 Encerrando...")
            break
        else:
            print("❗ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
