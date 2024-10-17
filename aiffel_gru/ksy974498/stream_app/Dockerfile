# Python 3.12.7 기반의 이미지 사용
FROM python:3.12.7-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --upgrade pip && \
    pip install poetry

# Poetry 설정을 통해 가상환경을 Docker 컨테이너 내에 만들지 않도록 설정
RUN poetry config virtualenvs.create false

# 프로젝트의 pyproject.toml만 복사 (poetry.lock 파일은 복사하지 않음)
COPY pyproject.toml ./

# 의존성 설치 (poetry.lock 파일 없이 설치)
RUN poetry install --no-root

# 프로젝트 파일 복사
COPY . .

# 컨테이너 시작 시 실행할 명령어
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]