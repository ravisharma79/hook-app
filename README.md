# 🚀 End-to-End DevOps Pipeline: Video Hook API

![CI Status](https://github.com/ravisharma79/hook-app/actions/workflows/main.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/ravisharma7963/devops-hook-app)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📌 Project Overview
This project is a comprehensive demonstration of a modern DevOps lifecycle. It features a lightweight Python (Flask) API that generates video script hooks, but the primary focus is the **infrastructure and automation** surrounding it. 

## 🚀 DevOps Pipeline Architecture
<img width="1536" height="1024" alt="devops-architecture" src="https://github.com/user-attachments/assets/70ce24a0-6213-4f4d-91dd-771e164a41c4" />

I built this pipeline to solve the classic "it works on my machine" problem and to eliminate the friction of manual server deployments. By utilizing containerization and an automated CI/CD pipeline, this project achieves zero-downtime deployments directly to an AWS production environment the moment code is pushed to the main branch.

## 🏗️ Technology

Rather than just throwing code on a server, I selected specific tools to mirror industry-standard production environments:

* **Application (Python/Flask):** Chosen for its lightweight footprint, making it ideal for microservice architecture and fast container build times.
* **Containerization (Docker):** Ensures environment consistency across local development, testing, and production. The application is packaged with its own dependencies and runtime.
* **Continuous Integration (GitHub Actions):** Automates the testing and building phases. Every commit is verified, ensuring broken code never reaches the container registry.
* **Artifact Storage (Docker Hub):** Acts as the central repository for built images, versioned securely.
* **Production Infrastructure (AWS EC2):** Provides a robust, scalable cloud environment running Ubuntu Linux.
* **Continuous Deployment (Watchtower):** Runs on the EC2 instance to actively monitor Docker Hub. It automates the pull-and-restart process, closing the CI/CD loop without requiring manual SSH access to the server.

## ⚙️ How the CI/CD Pipeline Works (Under the Hood)

This repository operates on a fully hands-off deployment model once code is merged.

### 1. The Build Phase (Continuous Integration)
When a developer pushes changes to the `main` branch, the `.github/workflows/main.yml` file triggers a GitHub Actions runner. 
* **Checkout & Setup:** The runner provisions a temporary Ubuntu environment and checks out the source code.
* **Authentication:** It securely logs into Docker Hub using encrypted GitHub Secrets.
* **Build & Push:** It builds a new Docker image from the `Dockerfile`, tagging it with the latest commit, and pushes the immutable artifact to Docker Hub.

### 2. The Deployment Phase (Continuous Deployment)
The AWS EC2 instance runs a persistent container called **Watchtower**.
* **Polling:** Every 60 seconds, Watchtower queries the Docker Hub API to check the hash of the `latest` image.
* **Rolling Update:** If a new hash is detected, Watchtower downloads the new image, sends a graceful shutdown signal (SIGTERM) to the running API container, and instantly spins up the new version on the same port.

## 💻 Local Development Guide

If you want to pull this project down and run it locally, follow these steps:

### Prerequisites
* **Python 3.9+**
* **Docker Desktop** installed and running
* **Git**

### Option A: Run Natively (Good for debugging code)
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)ravisharma79/hook-app.git
   cd hook-app
   ```
2. **Create a virtual environment (to isolate dependencies):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install dependencies and run:**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
##Access the API at http://localhost:5000/hook

### Option B: Run via Docker (Good for testing the production environment)
This builds the exact environment used on the AWS server.
```bash
# Build the image and name it 'devops-hook-app'
docker build -t devops-hook-app .

# Run the container, mapping your machine's port 5000 to the container's port 5000
docker run -p 5000:5000 devops-hook-app
```

### ☁️ Production Server Provisioning
For transparency, the AWS EC2 (Ubuntu) environment was provisioned using the following commands. The server is configured to allow inbound traffic on Port 80 (HTTP) and Port 22 (SSH).
```bash
# 1. Update packages and install Docker engine
sudo apt update && sudo apt install docker.io -y

# 2. Run the main API container in detached mode (-d), mapping web traffic (80) to the app (5000)
docker run -d -p 80:5000 --name hook-api <YOUR-DOCKER-USERNAME>/devops-hook-app:latest

# 3. Deploy Watchtower to enable continuous, automated updates from Docker Hub
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 60
```
### 🔮 Future Enhancements (Observability & IaC)
To further harden this infrastructure, the following upgrades are planned:

[ ] Infrastructure as Code (IaC): Replace manual EC2 console provisioning with Terraform to make the server infrastructure reproducible.

[ ] Metrics Scraping: Instrument the Flask app with the prometheus-flask-exporter to expose real-time usage data.

[ ] Data Visualization: Deploy Grafana alongside Prometheus to create dashboards monitoring API request volume and server health.

### If you have questions about this architecture or want to discuss DevOps best practices, feel free to open an issue or reach out!
