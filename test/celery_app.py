from celery import Celery

# Celery 애플리케이션 생성
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # Redis 브로커 설정
    backend='redis://localhost:6379/0'  # 결과 저장소로 Redis 사용
)

# 작업자 수, 태스크 시간 제한 등 설정 가능
app.conf.update(
    worker_concurrency=4,  # 병렬로 실행할 작업자 수 설정
    task_time_limit=300,  # 태스크의 최대 실행 시간
)
