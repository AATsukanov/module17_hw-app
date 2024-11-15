from .db import SessionLocal
# или??? from app.backend.db import SessionLocal

# Функция-генератор для подключения к БД:
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()