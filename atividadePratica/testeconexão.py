from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# SQLAlchemy Configuration
DATABASE_URL = "postgresql+psycopg2://postgres:147258@localhost/northwind"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        # Tenta criar uma sessão
        db = SessionLocal()
        db.execute(text('SELECT 1'))  # Declara a expressão SQL textualmente
        print("Conexão com o banco de dados estabelecida com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()

