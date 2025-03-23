# Overview Writer Backend

FastAPI backend with JWT authentication & SQLite persistence.

## Tech Stack
- Python 3.9+
- FastAPI
- Pydantic (Type validation)
- SQLAlchemy ORM
- JWT Token
- SQLite

## Setup

1. **Environment**
```bash
pip install -r requirements.txt
```

2. **Initialize DB**
```bash
python -c "from app.database import engine; from app.models.user import User; User.metadata.create_all(bind=engine)"
```

## Run

**Development Mode**
```bash
python -m app.main
```

**Production Mode**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 11451 --workers 4
```

## API Docs
Access after starting server:  
`http://localhost:11451/docs`  
`http://localhost:11451/redoc`

### Endpoints
**Health Check**
```bash
GET /health
```

**User Login**
```bash
POST /auth/login
# Request
curl -X POST http://localhost:11451/auth/login -d '{"username":"admin","password":"secret"}'
```

## Create Test User
```python
# In Python shell
from app.database import SessionLocal
from app.models.user import User
from app.security import get_password_hash

db = SessionLocal()
db.add(User(username="admin", hashed_password=get_password_hash("secret")))
db.commit()
```

## Notes
- Default port hardcoded to 11451 (see `app/main.py`)
- Secret key in `security.py` should be changed in production
- SQLite file will be created at `./test.db`