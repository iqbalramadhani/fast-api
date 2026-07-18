## AI Features (Week 2)

This project extends the basic CRUD API with AI capabilities using Google Gemini API.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /ask | Simple Q&A with AI, no context |
| POST | /ask/stream | Streaming response (word-by-word) |
| POST | /chat | Multi-turn conversation with function calling |
| POST | /todos/summary | AI-generated summary of all todos |

### How the AI Assistant works

The `/chat` endpoint uses function calling — the AI decides which tool 
to call based on natural language input:

- `create_todo_tool` — creates a new todo
- `list_all_todos_tool` — lists all todos with IDs
- `list_pending_todos_tool` — lists only incomplete todos  
- `update_todo_status_tool` — marks a todo as done/undone

Example: sending "buatkan todo beli susu, prioritas tinggi" via /chat 
triggers the AI to call `create_todo_tool(title="beli susu", priority="high")` 
automatically, without hardcoded logic.

### Key concepts implemented
- **RAG pattern** (`/todos/summary`): retrieve data from DB → augment prompt → generate response
- **Function calling**: AI autonomously decides which Python function to invoke
- **Multi-turn memory**: conversation history maintained per `session_id`
- **Streaming**: token-by-token response using async generators
- **System prompts**: constrain AI behavior/persona via `system_instruction`
- **Temperature control**: low temperature (0.2) for factual summaries vs default (0.7) for chat

### Known limitations
- Chat history is stored in-memory (`dict`), lost on server restart
- No confirmation step before destructive actions — update tool exists 
  but delete was intentionally not implemented without human-in-the-loop safeguards