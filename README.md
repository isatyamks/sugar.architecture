# AI Reflection Service

AI-powered reflection prompt generation for the Sugar Journal.

## Quick Start

```bash
# 1. Clone and enter the directory
cd ai-reflection-service

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Copy environment config
cp .env.example .env

# 5. Run development server
uvicorn app.main:app --reload --port 8000

# 6. Open API docs
# http://localhost:8000/docs
```

## Project Structure

```
app/
├── api/v1/          # FastAPI routes, schemas, dependencies
├── core/            # Business logic: engine, frameworks, routing, prompts
├── llm/             # LLM provider abstraction and implementations
├── cache/           # Optional prompt caching
├── logging_/        # Structured logging and response audit
├── storage/         # Persistent storage for interaction logs
├── analytics/       # Future analytics hooks
└── exceptions/      # Global error handling
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/
```

## Configuration

All settings are loaded from environment variables prefixed with `REFLECT_`.
See `.env.example` for all available options.

## LLM Providers

The system supports multiple LLM backends via a pluggable provider interface:

| Provider | Use Case | Config |
|----------|----------|--------|
| `local` | Self-hosted model on school server | `REFLECT_LLM_PROVIDER=local` |
| `ollama` | Local Ollama instance | `REFLECT_LLM_PROVIDER=ollama` |
| `openai` | OpenAI / Azure / vLLM | `REFLECT_LLM_PROVIDER=openai` |
| `huggingface` | HF Inference API | `REFLECT_LLM_PROVIDER=huggingface` |

## License

GPL-3.0-or-later — Sugar Labs
