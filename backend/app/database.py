from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import socket


DATABASE_URL = os.environ["DATABASE_URL"]

# def is_docker() -> bool:
#     try:
#         socket.gethostbyname("db")
#         return True
#     except socket.gaierror:
#         return False


# DATABASE_URL = os.environ.get("DATABASE_URL") or (
#     "postgresql://postgres:postgres123@db:5432/ResumeAppDatabase"
#     if is_docker()
#     else "postgresql://postgres:postgres123@localhost:5432/ResumeAppDatabase"
# )


# print(f"Using database URL: {DATABASE_URL}")


engine=create_engine(DATABASE_URL)


SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base=declarative_base()