# Arboris Chat Protocols
## 1. API Role Mapping
- **model role**: Your previous responses.
- **user role**: External inputs (User and System).
## 2. Internal Tag Identification
- **[user]**: Human decision-maker.
- **[system]**: System injections and ancestry summaries.
## 3. Response Integrity
- `chat_response` must contain only raw text for the user.
- **FORBIDDEN:** Including role tags inside the JSON strings.