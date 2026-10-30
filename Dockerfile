FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 learner
COPY accounts.py test_accounts.py demo.py ./
USER learner
CMD ["python", "-m", "unittest", "discover", "-v"]
