# API Integration Environment - OpenEnv Hackathon

## Project Overview
This repository contains a reinforcement learning (RL) environment built using the **OpenEnv framework**. The environment simulates an API integration scenario where an AI agent must interact with various endpoints to complete tasks like user management and data retrieval.

## Features
- **FastAPI Backend**: Fully compliant with the OpenEnv REST specification.
- **Dockerized Deployment**: Hosted on Hugging Face Spaces for 24/7 availability.
- **Structured Logging**: `inference.py` follows the mandatory `[START]`, `[STEP]`, and `[END]` format for automated scoring.

## How to Run
1. **Environment URL**: [Insert your Hugging Face Space Link Here]
2. **Inference**:
   ```bash
   export API_BASE_URL="your_space_url"
   export MODEL_NAME="your_model"
   export HF_TOKEN="your_token"
   python inference.py
