from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    "owner": "fernando",
    "depends_on_past": False,
}

with DAG(
    dag_id="spark_sales_pipeline",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["spark", "sales", "local-lab"],
) as dag:

    spark_job = SparkSubmitOperator(
        task_id="spark_sales_job",
        conn_id="spark_default",
        application="/opt/airflow/spark-jobs/process_sales.py",
        application_args=[
            "--input_path",
            "file:///opt/spark/data/sales.csv",
            "--output_path",
            "hdfs://namenode:9000/tmp/sales_processed/{{ ts_nodash }}",
        ],
        conf={"spark.hadoop.fs.defaultFS": "hdfs://namenode:9000"},
        packages="org.postgresql:postgresql:42.7.3",
        name="spark_sales_job",
        verbose=True,
    )

    spark_job
