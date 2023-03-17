## About

This project is a data pipeline that streams data from multiple sources, saves it to a local PostgreSQL database, and uploads it to Amazon S3. The pipeline is orchestrated using Apache Airflow and all components are deployed in Docker containers, making it easy to manage and scale the pipeline as needed.

The goal is to demonstrate how a professional data pipeline is engineered and what considerations should be taken.

## Requirements

To use this project, you will need:

-   Docker and Docker Compose installed on your system.
-   Basic understanding of Docker and Docker Compose.
-   Access to multiple data sources that you want to stream data from.
-   An Amazon S3 bucket to upload the data to. If you don't have an account you can get a free tier [here](https://aws.amazon.com/free).
-   An understanding of PostgreSQL and how to configure a database.

## Installation

To get started with this project, follow these steps:

1.  Clone the project repository to your local system:
    
``` bash
git clone https://github.com/yourusername/data-pipeline.git
```
    
2.  Navigate to the project directory:
       
``` bash
cd data-pipeline
```
    
3.  Edit the `docker-compose.yml` file and configure the services to your liking. For example, you can specify the credentials for the data sources, PostgreSQL database, and Amazon S3 bucket.
    
4.  Start the services using Docker Compose:
        
``` docker
docker-compose build && docker compose airflow-init && docker compose up -d
```
    
    This will first build all the required images for the project. Then it will migrate the postgre database for the airflow services. Finally it will start all the services specified in the `docker-compose.yml` file and run them in detached mode.
    
5.  Access the Airflow web interface by visiting the following URL:
    
    -   Airflow: [http://localhost:18080](http://localhost:8080/)
    
    Note that the URL may vary depending on the configuration you have specified in the `docker-compose.yml` file. In my case I am using port 18080 because 8080 is already taken.

6.  Navigate to Admin - Connections and three new records for the postgre databases and the aws server. We will be using hooks for our connections so this is needed. You may find the details in the `configurations.json` file.
    
7.  Activate both __dag_set_blockchain_db__ and __dag_get_transactions_save_s3__ DAGs to run the pipeline.
    
    Note that the last step of the pipeline will fail if you haven't set up an s3 bucket called __blockchain-token-events__.

7.  Configure the data pipeline by creating other DAGs (Directed Acyclic Graphs) in Airflow. DAGs define the workflow of the data pipeline, including the sources to stream data from, the data processing steps, and the destination to upload the data to.
    
    You can create DAGs using Python scripts and the Airflow API. Refer to the Airflow documentation for more information on how to create DAGs. To look at the DAGs created by this workflow go to airflow/dags/
    

## Usage

Once the data pipeline is up and running, it will automatically stream data from the specified sources, process the data, and upload it to Amazon S3. You can monitor the progress of the data pipeline using the Airflow web interface.

Here's a brief overview of what each service does:

-   Data sources: These are the sources of the data that you want to stream. You can configure the credentials for each data source in the `docker-compose.yml` file.
-   PostgreSQL: This is the database where the data is saved. You can configure the database settings in the `docker-compose.yml` file.
-   Amazon S3: This is the destination where the processed data is uploaded. You can configure the S3 bucket and credentials in the `docker-compose.yml` file.
-   Airflow: This is the tool that orchestrates the data pipeline. You can create DAGs using Python scripts and the Airflow API to define the workflow of the data pipeline.

You can configure each component according to your preferences and stream and process data using this pipeline.

## Conclusion

By using this project, you can create a data pipeline that streams data from multiple sources, processes it, and uploads it to Amazon S3. Docker makes it easy to deploy and manage the pipeline, while Airflow orchestrates the workflow of the pipeline. You can configure each component to your preferences and stream and process data with ease.

