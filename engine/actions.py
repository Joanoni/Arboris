import uuid
from datetime import datetime

class ActionHandler:
    def __init__(self, persistence, git_ops=None):
        self.persistence = persistence
        self.git_ops = git_ops  # Será integrado na próxima etapa

    def handle(self, response_data, current_node_id):
        """
        Direciona a resposta da IA para o executor correto com base no action_id.
        """
        action_id = response_data.get("action_id", 0)
        
        actions = {
            0: self._action_chat,
            1: self._action_branch,
            2: self._action_investigate,
            3: self._action_inactivate
        }
        
        executor = actions.get(action_id, self._action_chat)
        return executor(response_data, current_node_id)

    def _action_chat(self, data, node_id):
        """Ação 0: Apenas atualiza o log de conversa do nó atual."""
        # A persistência do chat em si será feita pelo main.py no loop,
        # mas aqui podemos validar se algo extra precisa ser feito.
        return {"status": "success", "next_node": node_id}

    def _action_branch(self, data, node_id):
        """Ação 1: Cria um resumo do nó atual e gera novas alternativas."""
        # 1. Salva o resumo (Summary) do nó que está sendo "selado"
        if data.get("summary"):
            self.persistence.save_summary(node_id, data["summary"])

        # 2. Processa as alternativas e registra no history.json
        history = self.persistence.load_history()
        alternatives = data.get("alternatives", [])
        
        new_children_ids = []
        for index, alt in enumerate(alternatives):
            alt_id = str(uuid.uuid4())[:8] # ID curto para facilidade de uso
            
            # Salva o arquivo .md da proposta para leitura humana
            self.persistence.save_alternative_proposal(node_id, index, alt["content"])
            
            # Registra o novo nó no mapa global
            history["nodes"][alt_id] = {
                "title": alt["title"],
                "parent": node_id,
                "children": [],
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            new_children_ids.append(alt_id)
        
        # 3. Atualiza o nó pai com os novos filhos
        history["nodes"][node_id]["children"].extend(new_children_ids)
        self.persistence.save_history(history)
        
        return {
            "status": "branched", 
            "new_nodes": new_children_ids,
            "message": f"{len(new_children_ids)} novas branches criadas."
        }

    def _action_investigate(self, data, node_id):
        """Ação 2: Modo de auditoria crítica (Red Teaming)."""
        # No nível do motor, a investigação é um chat focado em falhas.
        # As regras de behavior.md já garantem o tom inquisitorial.
        return {"status": "investigating", "next_node": node_id}

    def _action_inactivate(self, data, node_id):
        """Ação 3: Encerra o nó atual e retorna para o pai."""
        # 1. Salva o relatório de encerramento
        if data.get("inactivation_report"):
            self.persistence.save_inactivation_report(node_id, data["inactivation_report"])
        
        # 2. Marca o nó como inativo no history.json
        history = self.persistence.load_history()
        if node_id in history["nodes"]:
            history["nodes"][node_id]["status"] = "inactive"
            parent_id = history["nodes"][node_id]["parent"]
        else:
            parent_id = "root"

        # 3. Move o ponteiro para o nó pai (Retorno)
        history["current_node"] = parent_id
        self.persistence.save_history(history)
        
        return {
            "status": "inactivated", 
            "return_to": parent_id,
            "message": "Caminho encerrado. Retornando ao nó pai."
        }