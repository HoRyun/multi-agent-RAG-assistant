from sqlalchemy.orm import declarative_base

# WHY: Base를 별도 파일로 분리해 models.py와 session.py 간 순환 import를 방지한다.
Base = declarative_base()
