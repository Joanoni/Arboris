import subprocess
from pathlib import Path

class GitOps:
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)

    def _run_git(self, args):
        """Executa um comando Git e retorna o resultado."""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Silencia erros comuns como "branch already exists" se necessário
            return f"Git Error: {e.stderr.strip()}"

    def init_repo(self):
        """Inicializa o repositório Git e cria o commit inicial."""
        if not (self.repo_path / ".git").exists():
            self._run_git(["init"])
            self._run_git(["checkout", "-b", "root"])
            self.commit_changes("Initial Arboris state (root)")
            return "Git repository initialized at root."
        return "Git repository already exists."

    def create_branch(self, node_id, parent_id=None):
        """
        Cria uma nova branch a partir de um nó pai.
        Se parent_id for fornecido, faz o checkout dele primeiro.
        """
        if parent_id:
            self.switch_branch(parent_id)
        
        return self._run_git(["checkout", "-b", node_id])

    def switch_branch(self, node_id):
        """Muda para uma branch (nó) existente."""
        return self._run_git(["checkout", node_id])

    def commit_changes(self, message):
        """Adiciona todos os arquivos e faz o commit do estado atual."""
        self._run_git(["add", "."])
        # Usamos o commit message vindo da IA (commit_message field)
        return self._run_git(["commit", "-m", message])

    def get_current_branch(self):
        """Retorna o ID do nó (branch) atual."""
        return self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])