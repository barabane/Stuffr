from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(url=settings.POSTGRES_URL)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_async_session():
    session: AsyncSession
    async with session_maker() as session:
        yield session
        await session.commit()
