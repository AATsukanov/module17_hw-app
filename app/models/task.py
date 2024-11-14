from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
#import user #-- закомментируем т.к. не дает собрать alembic revision --autogenerate -m "Initial migration"

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    priority = Column(Integer, default=0, unique=True, index=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship('User', back_populates='tasks')

if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Task.__table__))