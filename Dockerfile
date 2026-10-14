FROM python:3.11-slim-bookworm@sha256:0a310eeecf4e1f5a0743f9a6520c90c88d089c903ca5fd283f501e3a805f5f89 AS dependencies
WORKDIR /app
ENV MPLBACKEND=Agg MPLCONFIGDIR=/tmp/matplotlib PYTHONUNBUFFERED=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
COPY requirements.lock.txt /app/requirements.lock.txt
RUN pip install --no-cache-dir -r /app/requirements.lock.txt

FROM dependencies AS pipeline
COPY src /app/src
COPY tests /app/tests
COPY benchmark /app/benchmark
COPY config.json /app/config.json
COPY data /data
CMD ["python", "-m", "src.cli", "--help"]

FROM dependencies AS participant
COPY data /data
COPY config.json benchmark/TASK.md benchmark/SOURCES.md /task/
WORKDIR /submission
ENV PYTHONPATH=/submission
USER 65532:65532
ENTRYPOINT ["python","/submission/analyze.py"]
