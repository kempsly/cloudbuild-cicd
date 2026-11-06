# Cloud Build CI/CD Pipeline for Flask, BigQuery & Cloud Run

An end-to-end MLOps project demonstrating automated testing, Docker image building, container storage, and application deployment using Google Cloud Platform (GCP) and GitHub.

## Overview

This project implements a Continuous Integration and Continuous Deployment (CI/CD) pipeline using Google Cloud Build. Every push to the configured GitHub branch can trigger the pipeline automatically.

The Flask application loads a CSV file stored in Google Cloud Storage (GCS) into a BigQuery table and returns a JSON response containing the table name and number of rows loaded.

## Architecture

```text
Developer
    |
    | git push
    v
GitHub Repository
    |
    | Push trigger
    v
Google Cloud Build
    |
    +--> Install Python dependencies
    |
    +--> Run pytest unit tests
    |
    +--> Build Docker image
    |
    +--> Push image to Artifact Registry
    |
    +--> Deploy to Cloud Run
                  |
                  v
             Flask API
                  |
                  +--> Cloud Storage (CSV)
                  |
                  +--> BigQuery (table)
```

## Tech Stack

- **Language:** Python
- **Web framework:** Flask
- **Testing:** pytest, unittest.mock
- **Containerization:** Docker
- **CI/CD:** Google Cloud Build
- **Source control:** Git and GitHub
- **Container registry:** Google Artifact Registry
- **Application hosting:** Google Cloud Run
- **Data storage:** Google Cloud Storage
- **Data warehouse:** Google BigQuery

## Project Structure

```text
cloudbuild-cicd/
├── cloudbuild.yaml   # CI/CD pipeline configuration
├── Dockerfile        # Container image definition
├── main.py           # Flask API and BigQuery integration
├── test_main.py      # Unit tests
├── requirements.txt  # Python dependencies
├── us-states.csv     # Sample dataset
├── .gitignore        # Files excluded from Git
└── README.md         # Project documentation
```

## How It Works

### 1. Automated Testing

Cloud Build installs the Python dependencies and runs the unit tests using pytest.

```bash
pip install -r requirements.txt
python -m pytest -v
```

The pipeline stops if the tests fail, preventing subsequent build and deployment steps from running.

### 2. Docker Image Build

Docker packages the Flask application and its dependencies into a container image targeting `linux/amd64`.

### 3. Artifact Registry

The built image is pushed to Google Artifact Registry.

Example image URI:

```text
us-docker.pkg.dev/PROJECT_ID/mlops-docker/demo-flask-app:BUILD_ID
```

### 4. Cloud Run Deployment

Cloud Build deploys the image to the `demo-flask-app` Cloud Run service in `us-central1`.

### 5. Application Execution

When the API endpoint `/` is called, the application loads the CSV from Cloud Storage into BigQuery and returns a JSON response.

Example response:

```json
{
  "message": "CSV loaded successfully",
  "table": "PROJECT_ID.test_schema.us_states",
  "rows": 50
}
```

The row count shown is an example based on the sample dataset and successful test configuration.

## Prerequisites

Before deploying this project, ensure you have:

- A Google Cloud project with billing configured.
- The Google Cloud CLI installed and authenticated.
- Docker installed for local container testing.
- A GitHub repository connected to Cloud Build.
- An Artifact Registry Docker repository.
- A Cloud Storage bucket containing the CSV dataset.
- A BigQuery dataset in a compatible location.
- Appropriate IAM permissions for the Cloud Build and Cloud Run service accounts.

Enable the required APIs:

```bash
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  --project=YOUR_PROJECT_ID
```

## Local Setup

Clone the repository:

```bash
git clone https://github.com/kempsly/cloudbuild-cicd.git
cd cloudbuild-cicd
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the unit tests:

```bash
python -m pytest -v
```

Run the application locally:

```bash
python main.py
```

The API will be available at:

```text
http://localhost:8080/
```

The application requires valid Google Cloud credentials and appropriate permissions for actual BigQuery operations. The unit tests mock BigQuery requests and do not require live cloud access.

## Google Cloud Configuration

Update the project-specific settings in `main.py` and `cloudbuild.yaml` to match your environment.

| Resource | Example |
|---|---|
| GCP project | `YOUR_PROJECT_ID` |
| Artifact Registry repository | `mlops-docker` |
| Docker image | `demo-flask-app` |
| Cloud Run service | `demo-flask-app` |
| Region | `us-central1` |
| BigQuery dataset | `test_schema` |
| BigQuery table | `us_states` |
| Cloud Storage bucket | `YOUR_BUCKET_NAME` |

Ensure the Cloud Run runtime service account can read the source CSV and write to the destination BigQuery table.

## GitHub-Triggered CI/CD

To automate deployments:

1. Push the project to GitHub.
2. Connect the GitHub repository to Google Cloud Build.
3. Create a trigger for pushes to the `main` branch.
4. Select `cloudbuild.yaml` as the build configuration file.
5. Configure the trigger's service account with the necessary IAM permissions.
6. Push a code change to start a build.

Example:

```bash
git add .
git commit -m "Update application"
git push origin main
```

Cloud Build will execute the configured pipeline automatically.

## Security and Cost Considerations

- Never commit service account keys, API keys, or other secrets.
- Prefer service account IAM permissions and Application Default Credentials over hardcoded credentials.
- Restrict public access unless the API is intentionally public.
- Each request to the current endpoint reloads the CSV into BigQuery using `WRITE_TRUNCATE`; repeated requests overwrite the table contents and may incur costs.
- Cloud Build, Artifact Registry, Cloud Run, BigQuery, and Cloud Storage usage may incur charges depending on your usage and available free credits.

## Future Improvements

- Add automated code formatting and linting.
- Use separate development and production environments.
- Add integration tests against a dedicated test dataset.
- Implement structured logging and monitoring.
- Add API authentication and request validation.
- Deploy only after tests and image security checks pass.
- Introduce versioned releases and rollback strategies.

## Learning Objectives

This project demonstrates practical skills in:

- CI/CD pipeline design.
- Automated Python testing.
- Docker image creation.
- Artifact Registry integration.
- Serverless deployment with Cloud Run.
- Cloud Storage and BigQuery integration.
- GitHub-triggered deployments.
- IAM permissions and cloud resource management.

---

**Author:** [Kempsly Silencieux](https://github.com/kempsly)

**Repository:** https://github.com/kempsly/cloudbuild-cicd
