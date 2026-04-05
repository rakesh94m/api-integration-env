# API Integration Environment - OpenEnv Hackathon

## Project Overview
This repository contains a reinforcement learning (RL) environment built using the **OpenEnv framework**. The environment simulates an API integration scenario where an AI agent must interact with various endpoints to complete tasks like user management and data retrieval.

## Features
- **FastAPI Backend**: Fully compliant with the OpenEnv REST specification.
- **Dockerized Deployment**: Hosted on Hugging Face Spaces for 24/7 availability.
- **Structured Logging**: `inference.py` follows the mandatory `[START]`, `[STEP]`, and `[END]` format for automated scoring.
  
## Environment Details
- **OpenEnv Space:** [https://huggingface.co/spaces/rakesh94m/api_integration_env](https://huggingface.co/spaces/rakesh94m/api_integration_env)
- **API Endpoint:** [https://rakesh94m-api-integration-env.hf.space](https://rakesh94m-api-integration-env.hf.space)

## Running Inference
To run the evaluation script, use the following commands in your terminal:

```bash
export API_BASE_URL="[https://rakesh94m-api-integration-env.hf.space](https://rakesh94m-api-integration-env.hf.space)"
export MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
export HF_TOKEN="your_huggingface_token_here"

python inference.py
