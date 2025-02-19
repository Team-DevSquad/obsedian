# Obsidian Guard

Obsidian Guard is an advanced, AI-enhanced security tool designed to proactively detect and mitigate vulnerabilities in software applications during development. By combining static and dynamic analysis with machine learning, it identifies security flaws early, reducing risk and ensuring robust protection.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

In today’s rapidly evolving threat landscape, traditional security solutions often lag behind emerging vulnerabilities. Obsidian Guard addresses this challenge by automating the scanning of source code and simulating real-world attack scenarios. This comprehensive approach helps developers secure their applications with minimal disruption to modern development workflows.

## Features

- **Static Analysis**
  - Scans Git commits for leaked credentials (API keys, access tokens, passwords) using GitLeaks and custom regex patterns.
  - Analyzes code structures and dependencies with AI-powered LLMs to uncover potential vulnerabilities.
  
- **Dynamic Analysis**
  - Executes YAML-based test cases simulating real-world attack scenarios.
  - Identifies runtime security flaws by evaluating application behavior and interactions.
  
- **Intuitive Dashboard**
  - Provides a visually engaging interface categorizing vulnerabilities by severity.
  - Offers actionable remediation suggestions to help developers quickly resolve issues.
  
- **Multi-Platform Support**
  - Seamlessly integrates into various environments such as .NET, Java, Eclipse, iOS, and more.
  - Designed for scalability and adaptability in diverse development ecosystems.

## Architecture

Obsidian Guard is built on a modular architecture comprising three main components:

1. **Backend API (apis.onsedianguard)**
   - Developed in Python using Django.
   - Integrates with PostgreSQL for data storage, Redis for caching, and Celery with Celery beat for asynchronous task processing.
   - Handles both static and dynamic security analysis.

2. **Dashboard (onsedian-dashboard)**
   - Built with Next.js and Typescript.
   - Offers an interactive interface for monitoring security findings, visualizing vulnerability data, and managing remediation efforts.

3. **Machine Learning (ML codes)**
   - Contains AI/ML models and scripts, including integration with the LLM `lily-cybersecurity-7b-v0.2`.
   - Enhances vulnerability detection using GenAI techniques.

Additional components include Docker for containerization and Minio S3 storage for handling file storage requirements.

## Technology Stack

- **Backend**: Python, Django, PostgreSQL, Redis, Celery, Celery beat
- **Frontend**: Next.js, Typescript
- **Security Scanning**: GitLeaks, custom regex patterns, AI/ML, LLM, GenAI
- **AI Integration**: lily-cybersecurity-7b-v0.2
- **DevOps**: Docker, Minio S3 storage

## Project Structure

The repository is organized into three main directories:

- **apis.onsedianguard**: Contains the Django-based backend API responsible for orchestrating security scans and analyses.
- **onsedian-dashboard**: Houses the Next.js/Typescript frontend code for the intuitive security dashboard.
- **ML codes**: Includes machine learning models and scripts that drive the AI-enhanced vulnerability detection mechanisms.

## Setup and Installation


### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Team-DevSquad/obsedian.git
   cd obsedian
   ```

2. **Backend**

    1. Create virtual environment 
    ```bash
    python -m venv venv
    source venv/bin/activate
    cd apis.obsedianguard
    ```

    2. Install dependencies 
    ```bash
    pip install -r requirements.txt
    ```

    3. Run Backend
        1. Start Django Project
        ```bash
        python manage.py runserver
        ```

        2. Start Celery
        ```bash
        celery -A obsedianguard.celery worker --pool=solo -l info
        ```

        3. Start celery beat
        ```bash 
        celery -A obsedianguard beat -l info
        ```

3. **Frontend**
    1. Install dependencies
        ```bash
        cd  obsedian-dashboard
        npm i
        ```
    2. Start Dashboard
        ```bash
        npm run dev
        ```


## Usage
1. **Static Analysis**: Once integrated with your source code repository, Obsidian Guard continuously scans for leaked credentials and code vulnerabilities.

2. **Dynamic Analysis**: Predefined YAML-based test cases simulate real-world attack scenarios to identify runtime issues.

3. **Dashboard**: The intuitive dashboard displays categorized vulnerability reports and provides actionable remediation suggestions, enabling prompt and effective responses.