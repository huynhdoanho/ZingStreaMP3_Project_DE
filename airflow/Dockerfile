FROM apache/airflow:2.7.1

# Cài đặt các gói cần thiết
USER root

# Cài đặt Java (yêu cầu cho Spark)
RUN apt-get update && \
    apt-get install -y default-jdk


ENV SPARK_HOME=/opt/airflow/spark
ENV SPARK_MASTER_URL=spark://spark-master:7077

RUN curl -O https://dlcdn.apache.org/spark/spark-3.3.4/spark-3.3.4-bin-hadoop3.tgz \
    && tar zxvf spark-3.3.4-bin-hadoop3.tgz \
    && rm -rf spark-3.3.4-bin-hadoop3.tgz \
    && rm -rf /opt/airflow/spark \
    && ln -s /opt/airflow/spark-3.3.4-bin-hadoop3 /opt/airflow/spark

RUN curl -O https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.18.41/s3-2.18.41.jar \
    && curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.12.367/aws-java-sdk-1.12.367.jar \
    && curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar \
    && curl -O https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.2.0/delta-core_2.12-2.2.0.jar \
    && curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/2.2.0/delta-storage-2.2.0.jar \
    && curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar \
    && curl -O https://repo1.maven.org/maven2/org/postgresql/postgresql/42.6.0/postgresql-42.6.0.jar \
    && mv s3-2.18.41.jar /opt/airflow/spark/jars \
    && mv aws-java-sdk-1.12.367.jar /opt/airflow/spark/jars \
    && mv aws-java-sdk-bundle-1.11.1026.jar /opt/airflow/spark/jars \
    && mv delta-core_2.12-2.2.0.jar /opt/airflow/spark/jars \
    && mv delta-storage-2.2.0.jar /opt/airflow/spark/jars \
    && mv hadoop-aws-3.3.2.jar /opt/airflow/spark/jars \
    && mv postgresql-42.6.0.jar /opt/airflow/spark/jars


# Đặt Spark Master trong airflow.cfg
RUN echo "[core]" >> /opt/airflow/airflow.cfg && \
    echo "spark.master ${SPARK_MASTER_URL}" >> /opt/airflow/airflow.cfg


USER airflow

# install packages
RUN pip install pyspark
RUN pip install minio
RUN pip install pyarrow
RUN pip install pandas
RUN pip install apache-airflow
RUN pip install apache-airflow-providers-postgres
RUN pip install dbt-postgres
RUN pip install dbt-core
RUN pip install sqlalchemy

