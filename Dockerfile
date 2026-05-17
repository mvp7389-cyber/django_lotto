# 1. 파이썬 3.14 공식 가벼운 버전(Slim)을 베이스 이미지로 사용
FROM python:3.14-slim

# 2. 컨테이너 내부에서 파이썬이 터미널로 로그를 즉시 출력하도록 설정
ENV PYTHONUNBUFFERED=1

# 3. 컨테이너 안에서 작업할 기본 폴더 위치 설정
WORKDIR /app

# 4. 윈도우의 패키지 명세서를 컨테이너 안으로 먼저 복사
COPY requirements.txt /app/

# 5. 컨테이너 안의 파이썬 환경에 패키지들을 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 현재 폴더의 모든 소스코드를 컨테이너 안의 /app 폴더로 복사
COPY . /app/

# 7. 컨테이너가 켜질 때 장고 서버를 자동으로 실행하도록 명령 지정
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
