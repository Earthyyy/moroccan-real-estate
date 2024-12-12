# Use official Airflow image
FROM apache/airflow:2.10.3-python3.11


# Switch to root to install system dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*


USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark==2.1.3

# Install Poetry
RUN pip install poetry==1.8.4

# Set working directory
WORKDIR /opt/airflow

# Copy project files
COPY --chown=airflow:root pyproject.toml poetry.lock* ./

RUN poetry lock
# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Download required JAR file
RUN mkdir -p ./libs \
    && wget -O ./libs/duckdb_jdbc.jar https://repo1.maven.org/maven2/org/duckdb/duckdb_jdbc/1.1.3/duckdb_jdbc-1.1.3.jar
