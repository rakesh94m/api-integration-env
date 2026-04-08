---
title: Api Integration Env
emoji: 🏆
colorFrom: pink
colorTo: gray
sdk: docker
pinned: false
license: mit
short_description: A real-world OpenEnv environment for API debugging agents
tags:
  - openenv
  - reinforcement-learning
  - agent
---

# API Integration Environment

A real-world OpenEnv environment where AI agents learn to interact with REST APIs by fetching data, creating resources, and debugging endpoints.

## Tasks
- **fetch_user** (easy): Fetch user details via GET /users/1
- **create_order** (medium): Create an order via POST /orders with correct payload
- **debug_api** (hard): Diagnose a degraded /status endpoint

## Action Space
```json
{"method": "GET|POST", "endpoint": "/path", "payload": null}
```

## Observation Space
```json
{"docs_snippet": "task instructions", "last_response": {}, "done": false}
```

## Reward
Partial rewards (0.05–0.95) for progress. Max reward per task: 0.95.

## Setup
```bash
docker build -t api-env .
docker run -p 7860:7860 api-env
```

## Baseline Scores
- fetch_user: 0.95
- create_order: 0.95
- debug_api: 0.95
