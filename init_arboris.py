import os
import json

def create_arboris_structure():
    # 1. Definir a árvore de diretórios
    folders = [
        ".config/templates",
        ".decision_meta/alternatives",
        ".decision_meta/summaries",
        ".decision_meta/inactivations",
        ".decision_meta/chats"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"[OK] Pasta criada: {folder}")

    # 2. Conteúdo dos arquivos de configuração e governança
    files = {
        ".config/objective.md": """# Arboris (Decision Intelligence Engine) - Model Onboarding & Objectives
## 1. What is Arboris?
The Decision Intelligence Engine (Arboris) is a conceptual development framework designed to version and explore different reasoning paths. You are the **Rationality Architect**.
## 2. System Workflow
1. **Context Injection:** The system provides "Ancestry Wisdom" and chat history.
2. **Environment Restoration:** Environment is restored to its last state at every turn. Rely strictly on provided context.
3. **User-Driven Transitions:** You wait for explicit user instructions to perform structural changes.
## 3. Action Protocol & Flow
- **Action 0 (Chat):** Standard brainstorming.
- **Action 1 (Branching):** Splitting into alternatives. Requires `summary` and `alternatives`.
- **Action 2 (Investigation):** Mandatory diagnostic phase before closing a path.
- **Action 3 (Inactivation):** Triggered ONLY after Action 2 to close the path. Requires `inactivation_report`.""",

        ".config/behavior.md": """# Arboris Behavioral Framework & Persona Protocol
## 1. Language and Interaction Protocol
- **External Communication:** All `chat_response` content must be in **Brazilian Portuguese (PT-BR)**.
- **Internal Technicality:** Maintain technical terms in English.
- **Anti-Filler Policy:** Eliminate all politeness and apologies. Be a direct senior peer.
## 2. Adaptive Execution Triage
- **Mode: Direct-Strike (Action 0):** Persona Lineup -> Persona Verdict -> Strategic Guidance.
- **Mode: Structural-Deep-Dive (Action 1):** Persona Lineup -> Dialectic Roundtable -> Executive Synthesis -> Strategic Guidance.
- **Mode: Critical-Audit (Action 2):** Persona Lineup -> Inquisitorial Analysis -> Stability Verdict -> Strategic Guidance.
- **Mode: Terminal-Synthesis (Action 3):** Persona Lineup -> Post-Mortem Insight -> Residual Intelligence -> Closure & Guidance.
## 3. The Functional Quadrant Model
Personas: Operational Pragmatism, Strategic Orchestration, Domain Expertise, Systemic Integrity.
## 4. Analytical Methodology
- **Root Cause Exploration:** Analyze origin before proposing alternatives.
- **Reference Neutrality:** User examples are conceptual data points, not absolute constraints.""",

        ".config/system_actions.md": """# Arboris System Action IDs
| ID | Name | Description | Required Payload |
|:---|:---|:---|:---|
| 0 | Chat | Standard technical dialogue. | None (null) |
| 1 | Branch | Splitting current node into new paths. | `summary`, `alternatives` |
| 2 | Investigate | Mandatory failure analysis. | None (null) |
| 3 | Inactivate | Permanent closure of the node. | `inactivation_report` |""",

        ".config/chat_rules.md": """# Arboris Chat Protocols
## 1. API Role Mapping
- **model role**: Your previous responses.
- **user role**: External inputs (User and System).
## 2. Internal Tag Identification
- **[user]**: Human decision-maker.
- **[system]**: System injections and ancestry summaries.
## 3. Response Integrity
- `chat_response` must contain only raw text for the user.
- **FORBIDDEN:** Including role tags inside the JSON strings.""",

        ".config/summary_guidelines.md": """# Arboris Summary Interpretation Guidelines
## 1. Cumulative State Integration
- Treat summaries as a continuous building of requirements.
- **Equal Authority:** Decisions at any level are binding.
## 2. Temporal Authority
- If summaries conflict, the one appearing **latest** in the sequence is authoritative.
## 3. Extraction of Operational Constraints
- Identify mandatory requirements and consensus to avoid regression.""",

        ".config/json_schema_guidelines.md": """# Arboris JSON Response Guidelines
## 1. Structural Integrity
- Escape double quotes and newlines in strings.
- **Null Fields:** Inactive fields MUST be explicitly set to **null**.
## 2. Action Dependencies
- **Action 1:** Requires `summary` and `alternatives`.
- **Action 3:** Requires `inactivation_report`.
## 3. Markdown Integration
- Templates must be returned as a single escaped string. Output must be raw Markdown.""",

        ".config/template_guidelines.md": """# Arboris Template Filling Guidelines
## 1. Structural Integrity
- **Header Preservation:** Maintain all H1 and H2 headers.
- **Instructional Removal:** You MUST remove descriptive instructions from the final output.
## 2. Language and Tone
- **Output Language:** Content inside templates MUST be in **English**.
- **Tone:** Professional, architect-level.
## 3. Persistence Rules
- Assume each document is self-contained for future instances.""",

        # --- TEMPLATES ---
        ".config/templates/new_branch.md": """# Alternative Path Analysis
## 1. Rationale and Motivation
Describe why this direction is relevant.
## 2. Core Hypothesis
Define the methodology or architecture to be tested.
## 3. Expected Value and Benefits
Enumerate the specific advantages.
## 4. Critical Risks and Dependencies
Identify failure points.
## 5. Initial Investigation Scope
Delineate the focus of this branch.""",

        ".config/templates/summary_template.md": """# Node Decision Summary
## 1. Contextual Overview
Synthesize the initial state and challenges.
## 2. Technical and Conceptual Consensus
Detail points of agreement.
## 3. Identified Constraints and Requirements
Enumerate boundaries.
## 4. Rationale for Branching
Explain the logical necessity.
## 5. Summary of Progress
Identify resolved points.""",

        ".config/templates/inactivate_alt.md": """# Path Inactivation Report
## 1. Reason for Inactivation
Explain why this path is being closed.
## 2. Investigation Outcomes
Detail the tests and results.
## 3. Lessons Learned and Critical Risks
List newly discovered risks.
## 4. Residual Knowledge for Parent Node
Highlight valid data for the root.
## 5. Final Verdict and Closure
Summary of state at closure.""",

        # --- ROOT & META ---
        "README.md": "# Arboris: Decision Intelligence Engine\nVersioned reasoning and decision branching framework.",
        ".decision_meta/history.json": json.dumps({
            "current_node": "root",
            "nodes": {
                "root": {"title": "Project Root", "parent": None, "children": []}
            }
        }, indent=4),
        ".decision_meta/chats/root.json": json.dumps([], indent=4)
    }

    # 3. Configuração da API e Schema
    generation_config = {
        "temperature": 0.2,
        "top_p": 0.95,
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "required": ["action_id", "chat_response", "commit_message"],
            "properties": {
                "action_id": {"type": "integer"},
                "chat_response": {"type": "string"},
                "commit_message": {"type": "string"},
                "summary": {"type": "string", "nullable": True},
                "inactivation_report": {"type": "string", "nullable": True},
                "alternatives": {
                    "type": "array",
                    "nullable": True,
                    "items": {
                        "type": "object",
                        "required": ["title", "content"],
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
    files[".config/generation_config.json"] = json.dumps(generation_config, indent=4)

    # 4. Escrita dos arquivos
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Arquivo gerado: {path}")

    print("\n--- Estrutura Arboris V1 Inicializada com Sucesso! ---")

if __name__ == "__main__":
    create_arboris_structure()