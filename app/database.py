from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Substitua 'usuario', 'senha', 'localhost' e 'nome_do_banco' com as informações do seu banco de dados
DATABASE_URL = "postgresql+asyncpg://admin:senha123@localhost:5432/patrocars"

# Criação do engine para PostgreSQL com asyncpg
engine = create_async_engine(DATABASE_URL, echo=True)

# Criação de uma sessão assíncrona para se comunicar com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Base para criação das tabelas com SQLAlchemy
Base = declarative_base()

# Função para obter uma sessão de banco de dados em rotas do FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
