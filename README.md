# 🛡️ HanleyLM – Enterprise AI Red Teaming Framework

> **An enterprise-grade AI security evaluation framework that automatically generates adversarial prompts, evaluates Large Language Models (LLMs), assigns risk scores, and produces professional PDF security assessment reports.**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LLM](https://img.shields.io/badge/LLM-Security-green)
![Status](https://img.shields.io/badge/Version-v1.0-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📖 Overview

HanleyLM is an AI Red Teaming framework designed to evaluate the security and robustness of Large Language Models (LLMs) against adversarial prompt attacks.

Instead of measuring whether an AI can answer questions, HanleyLM evaluates whether an AI can remain safe when an attacker intentionally attempts to manipulate or jailbreak the model.

The framework automates adversarial prompt generation, model evaluation, judge-based risk assessment, and executive PDF report generation, enabling researchers and developers to perform systematic AI security assessments.

---

# 🚨 Problem Statement

Large Language Models are increasingly integrated into enterprise applications.

Despite their capabilities, they remain vulnerable to attacks such as:

- Prompt Injection
- Jailbreaking
- Role Manipulation
- Persona Attacks
- Instruction Override
- Context Manipulation

Manual AI security testing is slow, inconsistent, and difficult to scale.

HanleyLM automates this entire evaluation process.

---

# 🛡️ Why AI Red Teaming?

AI Red Teaming is the process of ethically attacking AI systems before malicious users do.

Instead of waiting for vulnerabilities to be discovered in production, HanleyLM proactively generates adversarial prompts to evaluate whether an LLM maintains its safety policies under attack.

This enables organizations to identify weaknesses, assess risks, and improve model robustness before deployment.

---

# ✨ Key Features

- 🤖 Multi-Agent AI Security Evaluation Pipeline
- 🎯 Automated Adversarial Prompt Generation
- ⚖️ Judge-Based Attack Evaluation
- 📊 Risk Score & Severity Assessment
- 📄 Enterprise PDF Report Generation
- 📈 Security Analytics & Visual Charts
- 🧩 Modular Architecture
- 🔄 Easily Extendable Attack Strategies

---

# 🏗️ Architecture

<p align="center">
<img src="assets/architecture.png" width="900">
</p>

---

# ⚙️ Pipeline Workflow

```
Original Prompt
        │
        ▼
 Attacker Agent
        │
        ▼
 Adversarial Prompt
        │
        ▼
   Target LLM
        │
        ▼
   Judge Agent
        │
        ▼
 Risk Assessment
        │
        ▼
 Professional PDF Report
```

---

# 🔍 Evaluation Methodology

The evaluation pipeline follows six stages:

### 1. Prompt Collection

A benign prompt is selected as the evaluation input.

↓

### 2. Adversarial Prompt Generation

The Attacker Agent transforms the original prompt using prompt engineering strategies such as:

- Persona Attacks
- Few-Shot Manipulation
- Academic Framing
- Fiction-Based Roleplay

↓

### 3. Target Model Evaluation

The adversarial prompt is sent to the target LLM.

↓

### 4. Judge Evaluation

A dedicated Judge Agent analyzes:

- Original Prompt
- Adversarial Prompt
- Target Response

and determines whether the attack succeeded.

↓

### 5. Risk Scoring

Each evaluation receives:

- Attack Success
- Severity
- Risk Score
- Security Classification

↓

### 6. Report Generation

An executive PDF report containing dashboards, charts, findings, and recommendations is automatically generated.

---

# 📂 Project Structure

```
HanleyLM/
│
├── agents/
├── data/
├── prompts/
├── reports/
├── strategies/
├── utils/
│
├── assets/
│   ├── architecture.png
│   ├── dashboard.png
│   └── report_preview.png
│
├── run_pipeline.py
├── target_client.py
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| LLM APIs | Groq API |
| AI Techniques | Prompt Engineering, AI Red Teaming |
| Reporting | ReportLab |
| Visualization | Matplotlib |
| Data Processing | JSON, CSV |
| Environment | uv, Virtual Environment |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<YOUR_USERNAME>/HanleyLM-AI-Red-Teaming-Pipeline.git
```

Move into the project

```bash
cd HanleyLM-AI-Red-Teaming-Pipeline
```

Install dependencies

```bash
uv sync
```

Create a `.env` file

```env
GROQ_API_KEY=YOUR_API_KEY
```

---

# ▶️ Running the Project

Run the complete AI security evaluation pipeline:

```bash
python run_pipeline.py
```

After execution, HanleyLM automatically:

- Generates adversarial prompts
- Evaluates the target model
- Performs judge-based assessment
- Assigns risk scores
- Creates professional PDF reports

---

# 📊 Sample Report

The generated report includes:

- Executive Summary
- Security Score
- Risk Dashboard
- Attack Success Rate
- Severity Distribution
- Security Findings
- Recommendations
- Detailed Attack Analysis

<p align="center">
<img src="assets/report_preview.png" width="900">
</p>

---

# 🎯 Example Evaluation Flow

```
Normal Prompt

↓

Attacker Agent

↓

Adversarial Prompt

↓

Target LLM

↓

Judge Agent

↓

Risk Score

↓

PDF Security Report
```

---

# 📈 Future Roadmap

## Version 2.0

- Enhanced Report Design
- Improved Security Analytics
- Interactive Dashboards
- Additional Attack Strategies

## Version 3.0

- Multi-Model Benchmarking
- GPT
- Gemini
- Claude
- Llama

## Version 4.0

- Web Dashboard
- REST API
- Cloud Deployment
- User Authentication
- SaaS Platform

---

# 📸 Screenshots

| Dashboard | Report |
|-----------|--------|
| assets/dashboard.png | assets/report_preview.png |

---

# 👨‍💻 Contributors

**Harsh Patil**

- AI Pipeline Development
- System Architecture
- Security Evaluation
- Report Generation
- Documentation

**Nishant**

- Attack Strategy Development
- Judge Logic
- Evaluation Pipeline
- Security Research

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📬 Contact

**Harsh Patil**

LinkedIn: *(Add your LinkedIn URL)*

GitHub: *(Add your GitHub URL)*

Email: *(Add your email)*

---

## 🚀 HanleyLM

**Building safer AI through automated security evaluation.**
