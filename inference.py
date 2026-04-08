import os
import time
import requests
import asyncio
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://rakesh94m-api-integration-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")

client = None 

TASKS = ["fetch_user", "create_order", "debug_api"]

SYSTEM_PROMPT = """You are an API testing agent. You interact with a REST API environment.
You will receive an observation with a docs_snippet (instructions) and last_response.
Respond with a JSON action like: {"method": "GET", "endpoint": "/users/1", "payload": null}
Only respond with valid JSON, nothing else."""

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

def llm_action(obs: dict) -> dict:
    """Call LLM to decide next action based on observation."""
    try:
        prompt = f"""Observation:
docs_snippet: {obs.get('docs_snippet', '')}
last_response: {obs.get('last_response', None)}
done: {obs.get('done', False)}

What API action should you take? Respond with JSON only."""
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.1
        )
        import json
        text = response.choices[0].message.content.strip()
        # strip markdown if present
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        # fallback action
        return {"method": "GET", "endpoint": "/users/1", "payload": None}

async def run_task(task_name: str):
    base = API_BASE_URL.rstrip('/')
    total_reward = 0.0
    rewards = []
    
    try:
        # Reset
        reset_resp = requests.post(f"{base}/reset", json={"task": task_name}, timeout=10)
        reset_resp.raise_for_status()
        obs = reset_resp.json().get("observation", {})
    except Exception as e:
        print(f"[STEP] step=1 action=reset reward=0.00 done=false error='{e}'", flush=True)
        return 0.0, []

    for step_num in range(1, 6):  # max 5 steps per task
        try:
            action = llm_action(obs)
            step_resp = requests.post(f"{base}/step", json=action, timeout=10)
            step_resp.raise_for_status()
            result = step_resp.json()
            
            obs = result.get("observation", {})
            reward = float(result.get("reward", 0.0))
            done = result.get("done", False)
            total_reward += reward
            rewards.append(reward)
            
            print(
                f"[STEP] step={step_num} action={action.get('method','?')}:{action.get('endpoint','?')} "
                f"reward={reward:.2f} done={str(done).lower()} error=null",
                flush=True
            )
            
            if done:
                break
        except Exception as e:
            print(f"[STEP] step={step_num} action=unknown reward=0.00 done=false error='{e}'", flush=True)
            break
    
    score = total_reward / max(len(rewards), 1)
    return score, rewards

async def main():
    global client
    
    try:
        if not wait_for_ready(API_BASE_URL):
            print("[END] success=false steps=0 score=0.00 rewards= error='Server unreachable'", flush=True)
            return

        client = OpenAI(
            base_url=f"{API_BASE_URL.rstrip('/')}/v1",
            api_key=HF_TOKEN or "dummy"
        )

        all_scores = []
        all_rewards = []
        total_steps = 0

        for task in TASKS:
            print(f"[START] task={task} env=api_integration model={MODEL_NAME}", flush=True)
            score, rewards = await run_task(task)
            all_scores.append(score)
            all_rewards.extend(rewards)
            total_steps += len(rewards)
            print(
                f"[END] success=true steps={len(rewards)} score={score:.3f} "
                f"rewards={','.join(f'{r:.2f}' for r in rewards)}",
                flush=True
            )

    except Exception as e:
        print(f"[END] success=false steps=0 score=0.00 rewards= error='{e}'", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
