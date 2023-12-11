from sqlalchemy import Column, Integer, Float, String, DateTime, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy"
DATABASE_URL = "sqlite+aiosqlite:///clients.sqlite"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


class BookRec(Base):
    __tablename__ = "books"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    datetime = Column(DateTime, default=datetime.utcnow)
    title = Column(String, unique=False)
    x_avg_count_in_line = Column(Float)


async def get_all_books() -> list[BookRec]:
    async with async_session() as session:
        result = await session.execute(select(BookRec))
    return result.scalars().all()


async def add_book(title: str, average: float):
    async with async_session() as session:
        new_book = BookRec(datetime=datetime.utcnow(), title=title, x_avg_count_in_line=average)
        session.add(new_book)
        await session.commit()
    return new_book
