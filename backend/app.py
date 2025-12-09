from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import httpx

app = FastAPI()

# Настройка подключения к LLM (CloudRU API)
async def request_llm(prompt: str) -> str:
    url = "https://api.cloud.ru/v1/models/predict"
    headers = {"Authorization": f"Bearer {config.USER_TOKEN}"}
    data = {"prompt": prompt, "model": "cloudru/evolution-1.5"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()["response"]

class TestCaseRequest(BaseModel):
    requirements: str
    type: str  # "UI" или "API"

@app.post("/generate")
async def generate_test_cases(request: TestCaseRequest):
    prompt = f"Сгенерируй {request.type}-тест-кейсы по требованиям:\n{request.requirements}\nВ формате Allure TestOps as Code."
    response = await request_llm(prompt)
    return {"code": response}



# 3. Интеграция с GitLab
# app.py (добавить эндпоинт для отправки кода в репозиторий)

from fastapi import HTTPException

async def push_to_gitlab(repo_url: str, branch: str, code: str):
    # Используем GitLab API для создания/обновления README
    headers = {"Private-Token": config.GITLAB_TOKEN}
    data = {"content": code, "branch": branch}
    await httpx.post(repo_url, headers=headers, data=data)


# 6. Валидация и Оптимизация
# app.py (оптимизация тестов)

def optimize_tests(test_cases: List[TestCase]) -> List[dict]:
    prompt = f"Оптimize the following test cases: {test_cases}\nProvide recommendations for improving coverage."
    response = request_llm(prompt)
    return response["recommendations"]

