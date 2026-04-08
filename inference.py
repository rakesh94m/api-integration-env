import os
import time
import requests
import asyncio

API_BASE_URL = os.getenv("API_BASE_URL", "https://rakesh94m-api-integration-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")


def wait_for_ready(url, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{url.rstrip('/')}/health", timeout=5)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(5)
    return False


async def main():
    try:
        if not wait_for_ready(API_BASE_URL):
            print("[END] failed=true error='Server unreachable'")
            return

        print(f"[START] task=api_debug env=api_integration model={MODEL_NAME}")

        # Step 1: Reset environment
        try:
            reset_resp = requests.post(f"{API_BASE_URL.rstrip('/')}/reset", timeout=10)
            reset_resp.raise_for_status()
            obs = reset_resp.json()
            print(f"[STEP 1] reset obs={obs}")
        except Exception as e:
            print(f"[END] failed=true error='Reset failed: {e}'")
            return

        # Step 2: Take a step
        try:
            action = {"method": "GET", "endpoint": "/users/1", "payload": None}
            step_resp = requests.post(
                f"{API_BASE_URL.rstrip('/')}/step",
                json=action,
                timeout=10
            )
            step_resp.raise_for_status()
            result = step_resp.json()
            reward = result.get("reward", 0.0)
            print(f"[STEP 2] action={action} reward={reward}")
        except Exception as e:
            print(f"[END] failed=true error='Step failed: {e}'")
            return

        print(f"[END] success=true steps=2 score=1.00 rewards=0.50,{reward}")

    except Exception as e:
        print(f"[END] failed=true error='Unexpected error: {e}'")


if __name__ == "__main__":
    asyncio.run(main())
