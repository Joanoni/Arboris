import os
import json
import google.generativeai as genai
from pathlib import Path

class Brain:
    def __init__(self, api_key, model_name="gemini-1.5-pro", config_path=".config/generation_config.json"):
        self.api_key = api_key
        self.model_name = model_name 
        self.config_path = Path(config_path)
        self._setup_api()
        self.generation_config = self._load_generation_config()

    def _setup_api(self):
        """Inicializa o SDK do Google Generative AI."""
        if not self.api_key:
            raise ValueError("API Key não encontrada. Configure a variável de ambiente.")
        genai.configure(api_key=self.api_key)

    def _load_generation_config(self):
        """Carrega as configurações técnicas e o JSON Schema."""
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def generate_response(self, system_instruction, messages):
        # Use o self.model_name aqui
        model = genai.GenerativeModel(
            model_name=self.model_name, 
            generation_config=self.generation_config,
            system_instruction=system_instruction
        )

        try:
            # O SDK do Gemini espera uma lista de dicionários com 'role' e 'parts'
            response = model.generate_content(messages)
            return self._parse_json_response(response.text)
        except Exception as e:
            return {
                "action_id": 0,
                "chat_response": f"Erro crítico na API: {str(e)}",
                "commit_message": "system_error",
                "summary": None,
                "inactivation_report": None,
                "alternatives": None
            }

    def _parse_json_response(self, raw_text):
        """
        Extrai e valida o JSON da resposta, tratando possíveis 
        blocos de código Markdown que o modelo possa incluir.
        """
        clean_text = raw_text.strip()
        
        # Remove markdown code blocks se presentes
        if clean_text.startswith("```json"):
            clean_text = clean_text.replace("```json", "", 1).rsplit("```", 1)[0]
        elif clean_text.startswith("```"):
            clean_text = clean_text.replace("```", "", 1).rsplit("```",