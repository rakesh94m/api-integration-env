# API Integration Environment - OpenEnv Round 1

## Environment Access
- **Hugging Face Space:** [https://huggingface.co/spaces/rakesh94m/api_integration_env](https://huggingface.co/spaces/rakesh94m/api_integration_env)
- **API Base Endpoint:** `https://rakesh94m-api-integration-env.hf.space`

> **Note:** The API Endpoint will return a `404 Not Found` if visited in a browser. This is expected as it is a headless API. Please use the `/docs` suffix to view the interactive API documentation.

## How to Run Inference
To evaluate this environment, set the following environment variables in your terminal:

```bash
export API_BASE_URL="[https://rakesh94m-api-integration-env.hf.space](https://rakesh94m-api-integration-env.hf.space)"
export MODEL_NAME="meta-llama/Llama-3.1-8B-Instruct"
export HF_TOKEN="your_huggingface_token_here"

python inference.py
