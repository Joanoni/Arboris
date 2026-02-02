import os
import sys
from dotenv import load_dotenv
from engine.brain import Brain
from engine.context import ContextBuilder
from engine.actions import ActionHandler
from engine.git_ops import GitOps
from io.persistence import Persistence

def main():
    # 1. Configurações Iniciais
    load_dotenv()
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro") # Fallback se não existir

    if not API_KEY:
        print("[ERRO] GEMINI_API_KEY não encontrada no arquivo .env.")
        sys.exit(1)

    # 2. Instanciação dos Módulos
    persistence = Persistence()
    git_ops = GitOps()
    brain = Brain(api_key=API_KEY, model_name=MODEL_NAME)
    context_builder = ContextBuilder()
    action_handler = ActionHandler(persistence, git_ops)

    # 3. Inicialização do Repositório (Se necessário)
    print(git_ops.init_repo())

    print("\n" + "="*50)
    print("      Arboris: Decision Intelligence Engine v1")
    print("="*50)
    print("Digite 'sair' para encerrar ou 'status' para ver o nó atual.\n")

    while True:
        # 4. Identifica o estado atual
        current_node_id = persistence.get_current_node_id()
        current_branch = git_ops.get_current_branch()
        
        # 5. Entrada do Usuário
        user_input = input(f"[{current_branch}] > ")

        if user_input.lower() in ["sair", "exit", "quit"]:
            break
        
        if user_input.lower() == "status":
            history = persistence.load_history()
            node_info = history["nodes"].get(current_node_id, {})
            print(f"\n--- Status ---")
            print(f"ID do Nó: {current_node_id}")
            print(f"Título: {node_info.get('title', 'N/A')}")
            print(f"Filhos: {node_info.get('children', [])}")
            print(f"--------------\n")
            continue

        # 6. Preparação do Contexto
        system_instruction = context_builder.get_system_instructions()
        messages = context_builder.assemble_full_prompt(current_node_id, user_input)

        # 7. Chamada ao Cérebro (IA)
        print("Pensando...")
        response = brain.generate_response(system_instruction, messages)

        # 8. Processamento da Resposta e Ações
        # O handler cuida de Action 1 (Branch), Action 2 (Investigate), Action 3 (Inactivate)
        action_result = action_handler.handle(response, current_node_id)
        
        # 9. Persistência do Chat e Commit
        # Atualiza o histórico de mensagens local
        chat_history = context_builder.load_chat_history(current_node_id)
        chat_history.append({"role": "user", "parts": [f"[user] {user_input}"]})
        chat_history.append({"role": "model", "parts": [response["chat_response"]]})
        persistence.save_chat_log(current_node_id, chat_history)

        # Registra o estado no Git com o commit message da IA
        git_ops.commit_changes(response["commit_message"])

        # 10. Feedback Visual para o Usuário
        print(f"\nAI: {response['chat_response']}\n")
        
        if action_result["status"] == "branched":
            print(f"[SISTEMA] Novas alternativas geradas: {action_result['new_nodes']}")
            print(f"[SISTEMA] Use 'git checkout <id>' para explorar uma branch.")
        
        if action_result["status"] == "inactivated":
            print(f"[SISTEMA] Caminho encerrado. Retornando ao nó: {action_result['return_to']}")

if __name__ == "__main__":
    main()