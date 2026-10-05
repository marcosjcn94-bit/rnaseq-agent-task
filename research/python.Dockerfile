FROM rnaseq-python:dev@sha256:13b69b245a31c45a9ab9c37d319797b1c25b1a9f3145286c8e601db3d500cd97
WORKDIR /app
COPY research /app/research
COPY tests /app/tests
COPY src /app/src
COPY config.json /app/config.json
COPY data /data
ENV PYTHONPATH=/app PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg MPLCONFIGDIR=/tmp/matplotlib
CMD ["python", "-m", "pytest", "research/tests", "-q", "-p", "no:cacheprovider"]
