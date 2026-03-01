# ddd-fastapi

FastAPI example with async SQLAlchemy, Domain-Driven Design (Entities, Value Objects, Repository + Unit of Work patterns), Pydantic v2.

## Architecture

```
src/
├── domain/
│   ├── entities/account.py        # Account entity, AccountStatus
│   ├── value_objects/money.py     # Money value object
│   └── exceptions.py              # Domain exceptions
├── application/
│   ├── interfaces/account.py      # IAccountRepository interface
│   ├── services/account.py        # Use cases: create, deposit, withdraw, freeze, unfreeze, delete
│   └── uow.py                     # Unit of Work
├── infrastructure/
│   ├── models/account.py          # SQLAlchemy ORM model
│   ├── repositories/base.py       # SQLAlchemyRepository — generic CRUD base
│   ├── repositories/account.py    # SQLAlchemyAccountRepository
│   └── database.py                # async engine/session
├── presentation/
│   ├── v1/accounts.py             # FastAPI routes
│   ├── schemas/accounts.py        # Pydantic request/response schemas
│   └── exception_handlers.py      # Maps domain exceptions → HTTP responses
└── config.py                      # Settings via pydantic-settings
```

### Layers

```
presentation → application → domain ← infrastructure
```

- **domain** — entities, value objects, domain exceptions. No framework dependencies.
- **application** — use cases (services), repository interfaces, Unit of Work. Depends only on domain.
- **infrastructure** — SQLAlchemy ORM, concrete repository implementations. Implements domain interfaces.
- **presentation** — FastAPI routes, Pydantic schemas. Calls application services.

### Patterns

- **Entity** — `Account` with identity (`uuid4`) and business logic (`deposit`, `withdraw`, `freeze`, `unfreeze`). Validates invariants in `__post_init__`.
- **Factory method** — `Account.new(owner, balance)` creates a valid aggregate with generated id and `ACTIVE` status.
- **Value Object** — `Money` (immutable, compared by value, currency-aware arithmetic)
- **Repository** — `BaseRepository[E]` defines abstract CRUD interface (abstract methods raise `NotImplementedError`); `SQLAlchemyRepository[E, ORM]` provides default implementation using `INSERT/UPDATE/DELETE ... RETURNING`; concrete repos only implement `_to_entity` and `_dump`.
- **Unit of Work** — wraps session lifecycle, commits/rollbacks in one place
- **Dependency Inversion** — application depends on domain interfaces, not SQLAlchemy directly

## Getting started

```bash
cp .env.example .env
```

Edit `.env`:

```env
MY_APP__DB__USERNAME=postgres
MY_APP__DB__PASSWORD=postgres
MY_APP__DB__DATABASE=app
```

```bash
just install  # install dependencies
just up       # start PostgreSQL
just migrate  # apply migrations
just dev      # start server
```

API docs: http://localhost:8000/docs

## Commands

```bash
just install              # install dependencies
just dev                  # start development server
just up                   # start Docker services
just down                 # stop Docker services
just logs                 # follow Docker logs
just migrate              # apply all pending migrations
just migration "add ..."  # create a new migration
just lint                 # run linters and formatters
just check                # lint + type checking
```

## Migrations

```bash
just migration "add accounts table"  # create
just migrate                         # apply
uv run alembic downgrade -1          # rollback one step
```

## API

| Method   | Endpoint                         | Description      |
|----------|----------------------------------|------------------|
| `GET`    | `/api/v1/accounts/{id}`          | Get account      |
| `POST`   | `/api/v1/accounts`               | Create account   |
| `POST`   | `/api/v1/accounts/{id}/deposit`  | Deposit money    |
| `POST`   | `/api/v1/accounts/{id}/withdraw` | Withdraw money   |
| `POST`   | `/api/v1/accounts/{id}/freeze`   | Freeze account   |
| `POST`   | `/api/v1/accounts/{id}/unfreeze` | Unfreeze account |
| `DELETE` | `/api/v1/accounts/{id}`          | Delete account   |

All responses follow the `ApiResponse[T]` envelope:

```json
{
  "data": { "id": "...", "owner": "John", "balance": 1000, "currency": "RUB", "status": "active" }
}
```

## License

[MIT](LICENSE)
