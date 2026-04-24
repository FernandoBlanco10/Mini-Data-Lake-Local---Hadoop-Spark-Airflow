# 🏗️ Mini Data Lake Local (Cloud Architecture Simulation)

## 📌 Overview

This project implements a **local Mini Data Lake** designed to simulate the behavior of a modern cloud-based data engineering architecture.  

Beyond just making the system work, the main goal is to **understand how key components in a distributed ecosystem interact** and how they map to managed services in cloud platforms such as Azure.

---

## 🎯 Objective

Design and implement an end-to-end data pipeline that enables:

- Workflow orchestration using Apache Airflow  
- Distributed data processing with Apache Spark  
- Data storage in a distributed file system (HDFS)  
- Structured data persistence in PostgreSQL  
- Full environment reproducibility using Docker  

The purpose is to **replicate real-world cloud architecture patterns locally**, focusing not only on the *how*, but also the *why* behind each component.

---

## ⚙️ Tech Stack

- Apache Airflow (orchestration)
- Apache Spark (distributed processing)
- HDFS (storage layer)
- PostgreSQL (relational persistence)
- Docker & Docker Compose (local infrastructure)

---

## 🏛️ Architecture

**Pipeline flow:**
Airflow → Spark → HDFS → PostgreSQL

1. Airflow triggers a scheduled DAG  
2. The DAG launches a Spark job  
3. Spark processes sales data  
4. Processed data is stored in HDFS  
5. Results are loaded into PostgreSQL  

This flow replicates a common industry pattern:  
**Data Lake (storage) + distributed processing + structured consumption layer**

---

## ☁️ Cloud Approach (Azure Mapping)

This project was explicitly designed to understand cloud equivalences:

| Local Component | Azure Equivalent |
|---------------|------------------|
| Airflow       | Azure Data Factory / Synapse Pipelines |
| Spark         | Azure Databricks / Synapse Spark |
| HDFS          | Azure Data Lake Storage Gen2 |
| PostgreSQL    | Azure Database for PostgreSQL |
| Docker Compose| Infrastructure as Code (Bicep / Terraform) |

This enables seamless knowledge transfer to real-world cloud environments.

---

## 📂 Project Structure

### 🔹 Orchestration (`airflow/`)
- DAG definitions for pipeline execution  
- Custom Airflow image with Spark integration  
- Task dependency and workflow management  

### 🔹 Processing (`spark/`)
- Data transformation job (`process_sales.py`)  
- Metric calculation (`total_sales`)  
- Writes output to HDFS and loads into PostgreSQL  

### 🔹 Infrastructure (`docker-compose.yml`)
- Multi-service environment:
  - Airflow (webserver + scheduler)
  - Spark (master + worker)
  - HDFS (namenode + datanode)
  - PostgreSQL  

👉 Provides a fully reproducible distributed environment locally.

---

## 🔄 Data Pipeline

**Input:** Sales CSV file  
**Transformation:** Data cleaning and metric calculation  
**Output:**
- Processed data stored in HDFS (Data Lake)  
- Structured data loaded into PostgreSQL (consumption layer)

---

## 💡 Key Learnings

- End-to-end distributed pipeline design  
- Layered architecture (orchestration, processing, storage, consumption)  
- Handling distributed environments and containerized systems  
- Simulating cloud architectures locally  
- Troubleshooting real-world data engineering infrastructure issues  

---

## 🚀 Execution

```bash
docker-compose up
```

Airflow UI: http://localhost:8080
HDFS UI: http://localhost:9870

Ejecutar DAG:

```bash
spark_sales_pipeline
```

## Conclusión

This project goes beyond data processing by providing a practical understanding of modern cloud data architectures, enabling the application of these concepts in platforms such as Azure, AWS, or GCP.
