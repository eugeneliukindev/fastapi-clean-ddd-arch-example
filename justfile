default:
    @just --list

# Install dependencies
install:
    uv sync

# Run linters and formatters via pre-commit
lint:
    pre-commit run --all-files --verbose

# Run lint + type checking
check: lint
    mypy .

# Start the development server
dev:
    uv run uvicorn src.main:app --reload

# Start Docker services (PostgreSQL)
up:
    docker compose up -d

# Stop Docker services
down:
    docker compose down

# Follow Docker logs
logs:
    docker compose logs -f

# Apply all pending migrations
migrate:
    uv run alembic upgrade head

# Create a new migration: just migration "add accounts table"
migration msg:
    uv run alembic revision --autogenerate -m "{{msg}}"
