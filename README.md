
## 🚗 End-to-End Vehicle Insurance MLOps Pipeline
This repository showcases a production-ready MLOps framework for managing, modeling, and deploying vehicle insurance data. Built to demonstrate industry-standard practices, it integrates robust data engineering, automated validation, cloud-native storage, and full CI/CD infrastructure.
------------------------------
## 🏗️ Phase 1: Environment & Project Initialization## 1. Structural Architecture

* template.py Execution: Generates standard folder trees and placeholder modules automatically.
* Package Packaging: Configures setup.py and pyproject.toml for clean internal local package imports.
* Reference Docs: Key architectural fundamentals are documented inside crashcourse.txt.

## 2. Dependency Management

* Virtualization: Uses a localized Conda environment running Python 3.10.
* Installation: Installs locked dependencies via pip requirements management.

conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
pip list # Verifies local package links

------------------------------
## 📊 Phase 2: Data Engineering & Validation Storage## 3. Database Layer (MongoDB Atlas)

* Cloud Cluster: Provisioned via an M0 Free Tier cluster on MongoDB Atlas.
* Network Security: Configured with global IP access (0.0.0.0/0) during development.
* Ingestion Seed: Run notebook/mongoDB_demo.ipynb to seed raw insurance datasets into collections.

## 4. System Observability & EDA

* Logging System: Custom timestamped event streaming built into core components.
* Exception Layer: Overridden error-handling hooks to trap system faults via demo.py.
* Data Insights: Deep feature engineering scripts written inside dedicated EDA notebooks.

------------------------------
## ⚙️ Phase 3: Core Pipeline Engineering## 5. Automated Data Ingestion

* Remote Extraction: configuration.mongo_db_connections.py manages cloud cluster handshakes.
* Data Sink: components.data_ingestion.py splits extracted files into immutable artifacts.
* Runtime Trigger: Pass the connection string as an environment variable to execute:

# Bash Environment Setup
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/"
# PowerShell Environment Setup
$env:MONGODB_URL = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"

## 6. Validation & Preprocessing

* Schema Enforcement: Validates raw datasets against strict specifications in config.schema.yaml.
* Data Integrity: Checks for data drift and anomalies using helpers in utils.main_utils.py.
* Transformation Engine: components.data_transformation.py builds robust preprocessing pipelines.

## 7. Model Training & Versioning

* Training Loops: components.model_trainer.py orchestrates model training runs.
* Abstraction: Model parameters and preprocessing pipelines are encapsulated using entity.estimator.py.

------------------------------
## ☁️ Phase 4: AWS Cloud Architecture## 8. Access Management

* IAM Security: Configured with minimal necessary actions under an AdministratorAccess policy hook.
* System Keys: Credentials provisioned locally via temporary CLI environment blocks:

export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"

## 9. Storage & Registry Link

* S3 Storage: Bucket created at my-model-mlopsproj in the us-east-1 region.
* Model Registry: src.aws_storage and entity.s3_estimator.py pull/push trained weights to S3.

------------------------------
## 🚀 Phase 5: Production Deployment & CI/CD## 10. Serving & UI Layer

* Prediction API: app.py exposes REST endpoints for high-throughput model scoring.
* Web Interface: Custom HTML/CSS frontend built using assets in /templates and /static.

## 11. Containerized CI/CD Workflow

* Docker Engine: Multi-stage Dockerfile structures reproducible, lightweight runtime containers.
* GitHub Actions: Automated pipeline securely builds and pushes images using GitHub Secrets:
* AWS_ACCESS_KEY_ID
   * AWS_SECRET_ACCESS_KEY
   * AWS_DEFAULT_REGION
   * ECR_REPO

## 12. Cloud Hosting (AWS EC2)

* Runner Agent: EC2 host linked directly to GitHub as a private self-hosted runner.
* Production Proxy: Container runs natively on Docker inside EC2.
* Network Rule: Route traffic by exposing port 5080 via EC2 Security Groups.

URL Endpoint: http://<YOUR_EC2_PUBLIC_IP>:5080

------------------------------
## 🎯 Architectural Workflow Summary

[MongoDB Atlas] ➔ [Data Ingestion] ➔ [Data Validation] ➔ [Data Transformation]
                                                                  │
[AWS EC2 Host] ⇠ [Amazon ECR] ⇠ [GitHub Actions] ⇠ [Model Trainer & S3]



