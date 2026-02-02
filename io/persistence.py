import json
from pathlib import Path

class Persistence:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.meta_path = self.base_path / ".decision_meta"
        self.history_file = self.meta_path / "history.json"

    def _save_json(self, file_path, data):
        """Helper para salvar arquivos JSON com formatação."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _save_md(self, file_path, content):
        """Helper para salvar arquivos Markdown."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    # --- Gerenciamento da Árvore (History) ---

    def load_history(self):
        """Carrega o registro global da árvore de decisão."""
        if not self.history_file.exists():
            return {"current_node": "root", "nodes": {}}
        with open(self.history_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_history(self, history):
        """Salva o registro global da árvore de decisão."""
        self._save_json(self.history_file, history)

    # --- Persistência de Dados por Nó ---

    def save_chat_log(self, node_id, messages):
        """Salva o histórico de mensagens do nó atual."""
        chat_path = self.meta_path / "chats" / f"{node_id}.json"
        self._save_json(chat_path, messages)

    def save_summary(self, node_id, content):
        """Salva a síntese (Ancestry Wisdom) do nó."""
        summary_path = self.meta_path / "summaries" / f"{node_id}.md"
        self._save_md(summary_path, content)

    def save_inactivation_report(self, node_id, content):
        """Salva o relatório de encerramento de caminho."""
        report_path = self.meta_path / "inactivations" / f"{node_id}.md"
        self._save_md(report_path, content)

    def save_alternative_proposal(self, node_id, alt_index, content):
        """
        Salva uma proposta de branch alternativa para consulta.
        Nomeia como: {node_id}_alt_{index}.md
        """
        alt_path = self.meta_path / "alternatives" / f"{node_id}_alt_{alt_index}.md"
        self._save_md(alt_path, content)

    # --- Utilitários de Estado ---

    def get_current_node_id(self):
        """Retorna o ID do nó em que o sistema está operando no momento."""
        history = self.load_history()
        return history.get("current_node", "root")

    def update_current_node(self, node_id):
        """Atualiza o ponteiro do nó atual no history.json."""
        history = self.load_history()
        history["current_node"] = node_id
        self.save_history(history)