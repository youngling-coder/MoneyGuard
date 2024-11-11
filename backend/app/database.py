from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .settings import application_settings

DATABASE_URL = f"postgresql+asyncpg://{application_settings.db_user}:{application_settings.db_password}@{application_settings.db_host}:{application_settings.db_port}/{application_settings.db_name}"



# TODO: SET ECHO VALUE TO FALSE BEFORE PRODUCTION!!!

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with async_session() as session:
        yield session
        await session.commit()