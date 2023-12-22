ZingStreaMP3

## Description:
The project will stream events that are created by a fictitious music streaming service that operates similarly to Spotify. Additionally, a data pipeline that consumes real-time data will be developed. The incoming data would be analogous to an event that occurred when a person listened to music, navigated around the website, or authenticated themselves. The processing of the data would take place in real-time, and it would be saved to the data lake at regular intervals (every two minutes). The hourly batch job will then make use of this data by consuming it, applying transformations to it, and creating the tables that are needed for our dashboard so that analytics may be generated. We are going to try to conduct an analysis of indicators such as the most played songs, active users, user demographics, etc.

You will be able to generate a sample dataset for this project by using Eventsim and the Million Songs dataset. Apache Kafka and Apache Spark are two examples of streaming technologies that are used for processing data in real-time. The Structured Streaming API offered by Spark makes it possible for data to be processed in real-time in mini-batches, which in turn offers low-latency processing capabilities. The processed data are uploaded to MinIO, where they are then subjected to transformation with the assistance of dbt. We can clean the data, convert the data, and aggregate the data using dbt so that it is ready for analysis. The data is then sent to PostgreSQL, which serves as a data warehouse, and Power BI is used to create a visual representation of the data. Apache AirFlow has been used for the purpose of orchestration, whilst Docker is the tool of choice when it comes to containerization.

## Technologies:
- Orchestration: Apache Airflow 
- Streaming: Apache Spark, Apache Kafka
- Transform data: dbt
- Storage: PostgreSQL, MinIO
- Docker
- Data generate: Eventsim
- Data visualize: Power BI

## Overview:
![alt text](https://github.com/huynhdoanho/ZingStreaMP3_Project_DE/blob/9646116ad2d5a4da0c0704d1519fd9d712f0862a/images/overview.png)


# UPDATING ....
