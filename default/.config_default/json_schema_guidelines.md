# Arboris JSON Response Guidelines
## 1. Structural Integrity
- Escape double quotes and newlines in strings.
- **Null Fields:** Inactive fields MUST be explicitly set to **null**.
## 2. Action Dependencies
- **Action 1:** Requires `summary` and `alternatives`.
- **Action 3:** Requires `inactivation_report`.
## 3. Markdown Integration
- Templates must be returned as a single escaped string. Output must be raw Markdown.