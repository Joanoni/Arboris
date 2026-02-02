# Arboris: Decision Intelligence Engine (V1)

**Arboris** is a framework for conceptual development and complex decision-making. It leverages Large Language Models (LLMs) and version control logic to explore, document, and branch technical reasoning paths.

Unlike standard AI assistants, Arboris acts as a **Rationality Architect**, ensuring that every decision is backed by investigation, summarized for posterity, and structured within a decision tree.

---

## 🧠 Core Concept

Arboris operates on the principle of **Branching Rationality**. Every complex problem is broken down into decision nodes. When a crossroad is reached, the engine "branches" the conversation into multiple alternatives, allowing each to be explored in isolation without losing the parent context.

### The System Actions
The engine's state machine is driven by four primary Action IDs:
- **Action 0 (Chat):** Standard technical dialogue within the current node.
- **Action 1 (Branching):** Splitting the current path into multiple alternatives.
- **Action 2 (Investigation):** Mandatory "Red Teaming" or failure analysis before closing a path.
- **Action 3 (Inactivation):** Closing a failed or inferior path and returning to the parent node.

---

## 📁 Project Structure

### `.config/` (The Brain)
Contains the governance and operational rules for the AI Model.
- `objective.md`: The onboarding manual for the Model.
- `behavior.md`: Persona, tone, and logical rigor guidelines.
- `system_actions.md`: Technical definitions of Action IDs.
- `generation_config.json`: The JSON Schema for API response enforcement.
- `templates/`: Markdown structures for summaries, new branches, and reports.

### `.decision_meta/` (The Memory)
The persistent storage for the decision tree's intelligence.
- `summaries/`: Ancestry wisdom (synthesis of every parent node).
- `alternatives/`: Detailed technical proposals for each branch.
- `history.json`: The global registry of node IDs, titles, and paths.

---

## 🚀 Workflow

1. **Initialization:** The system loads the `.config/` and injects the decision lineage into the model.
2. **Interaction:** The user discusses concepts with the model in Portuguese.
3. **Decision Points:** Upon user command, the model triggers **Action 1**, generating a summary and technical alternatives in English.
4. **Exploration:** The user selects a path, and the system restores the environment to that specific node.
5. **Pruning:** If a path is invalid, an **Investigation (Action 2)** is performed before **Inactivation (Action 3)** returns the state to the previous decision point.
