import os
import json
from pathlib import Path

class ContextBuilder:
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.config_path = self.base_path / ".config"
        self.meta_path = self.base_path / ".decision_meta"

    def _load_md(self, file_path):
        """Lê arquivos Markdown com fallback para erro."""
        try:
            return file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return f"Warning: {file_path.name} not found."

    def get_system_instructions(self):
        """
        Consolida diretrizes e os TEMPLATES em uma única 
        System Instruction para garantir que a IA conheça a estrutura de saída.
        """
        instruction_files = [
            "objective.md",
            "behavior.md",
            "system_actions.md",
            "chat_rules.md",
            "summary_guidelines.md",
            "json_schema_guidelines.md",
            "template_guidelines.md"
        ]
        
        template_files = [
            "new_branch.md",
            "summary_template.md",
            "inactivate_alt.md"
        ]
        
        full_instruction = []

        # 1. Carrega Diretrizes de Comportamento
        for file_name in instruction_files:
            content = self._load_md(self.config_path / file_name)
            full_instruction.append(f"--- GUIDELINE: {file_name.upper()} ---\n{content}")

        # 2. Carrega os Blueprints (Templates)
        for file_name in template_files:
            content = self._load_md(self.config_path / "templates" / file_name)
            full_instruction.append(f"--- RAW TEMPLATE TO FILL: {file_name.upper()} ---\n{content}")
        
        return "\n\n".join(full_instruction)

    def get_ancestry_wisdom(self, current_node_id):
        """
        Percorre a árvore de decisão do nó atual até a raiz, 
        coletando os resumos (summaries) para dar contexto histórico.
        """
        history_path = self.meta_path / "history.json"
        if not history_path.exists():
            return []

        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

        ancestry_messages = []
        node_ptr = current_node_id
        
        # Coleta os IDs dos pais
        path_to_root = []
        while node_ptr and node_ptr in history["nodes"]:
            parent = history["nodes"][node_ptr]["parent"]
            if parent:
                path_to_root.append(parent)
            node_ptr = parent
        
        # Inverte para ler da raiz para o presente
        for node_id in reversed(path_to_root):
            summary_file = self.meta_path / "summaries" / f"{node_id}.md"
            if summary_file.exists():
                summary_content = summary_file.read_text(encoding="utf-8")
                # Injeta como [system] dentro da role 'user' conforme chat_rules.md
                ancestry_messages.append({
                    "role": "user",
                    "parts": [f"[system] Ancestry Summary (Node: {node_id}):\n{summary_content}"]
                })
        
        return ancestry_messages

    def load_chat_history(self, node_id):
        """Carrega o histórico de chat específico do nó atual."""
        chat_file = self.meta_path / "chats" / f"{node_id}.json"
        if not chat_file.exists():
            return []
        
        with open(chat_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def assemble_full_prompt(self, current_node_id, user_input):
        """
        Monta a lista final de mensagens para a API.
        Estrutura: Ancestry Wisdom -> Chat History -> New User Input
        """
        messages = []
        
        # 1. Sabedoria Ancestral (Resumos dos pais)
        messages.extend(self.get_ancestry_wisdom(current_node_id))
        
        # 2. Histórico de Chat do Nó atual
        messages.extend(self.load_chat_history(current_node_id))
        
        # 3. Input atual do usuário (com a tag [user])
        messages.append({
            "role": "user",
            "parts": [f"[user] {user_input}"]
        })
        
        return messages