FROM python:3.15-slim-bookworm@sha256:122756f3fe72c4f5d3d71897888204ee85774bc79de952555b8a474e1d0a5d53 AS dependencies
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
