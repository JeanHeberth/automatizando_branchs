import subprocess

REPO_PATH = "/Users/jeanheberth/Documents/GitClone/AutomacaoPW/saucelabs"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=REPO_PATH)
    if result.returncode != 0:
        print(f"❌ Erro ao executar: {command}\n{result.stderr}")
    else:
        print(result.stdout)
    return result

def get_default_branch():
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_PATH,
            check=True
        )
        ref = result.stdout.strip()
        return ref.split("/")[-1]
    except subprocess.CalledProcessError:
        branches = subprocess.check_output(["git", "branch", "-r"], cwd=REPO_PATH).decode()
        if "origin/main" in branches:
            return "main"
        elif "origin/master" in branches:
            return "master"
        else:
            raise Exception("❗ Não foi possível determinar a branch principal (main ou master).")

def remote_branch_exists(branch):
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", branch],
            capture_output=True,
            text=True,
            cwd=REPO_PATH
        )
        return branch in result.stdout
    except subprocess.CalledProcessError:
        return False

def automate_git_workflow():
    try:
        branch_main = get_default_branch()
        print(f"🔍 Branch principal detectada: {branch_main}")

        branch_name = input("Digite o nome da nova branch: ")
        feature_branch = f"feature/{branch_name}"

        print(f"\n🔄 Trocando para a branch {branch_main}...")
        run_command(f"git checkout {branch_main}")

        print(f"\n🧹 Excluindo todas as branches locais, exceto {branch_main}...")
        run_command(f"git branch | grep -v '{branch_main}' | xargs git branch -D")

        print(f"\n⬇️ Atualizando a branch {branch_main}...")
        run_command("git pull")

        print(f"\n🌱 Criando e trocando para a nova branch {feature_branch}...")
        run_command(f"git checkout -b {feature_branch}")

        if remote_branch_exists("develop"):
            print(f"\n⬇️ Atualizando a nova branch com a develop...")
            run_command("git pull origin develop")
        else:
            print("⚠️ Branch 'develop' não existe no remoto. Pulando pull da develop.")

        print("\n✅ Processo concluído!")

    except Exception as e:
        print(f"\n❗ Erro geral: {e}")

if __name__ == "__main__":
    automate_git_workflow()
