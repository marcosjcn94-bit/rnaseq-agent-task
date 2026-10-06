# Build this base from the repository's pinned Dockerfile dependencies target first.
FROM rnaseq-python:dev
WORKDIR /app
COPY research /app/research
COPY tests /app/tests
COPY src /app/src
COPY config.json /app/config.json
COPY data /data
ENV PYTHONPATH=/app PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg MPLCONFIGDIR=/tmp/matplotlib
CMD ["python", "-m", "pytest", "research/tests", "-q", "-p", "no:cacheprovider"]
