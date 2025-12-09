  ### Прототип Agentic-Системы для Генерации и Оптимизации Тест-Кейсов

#### Структура проекта
```
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── utils/
│   └── package.json
├── docker-compose.yml
└── tests/
```

---

#### 1. Backend (Python + FastAPI)

**app.py** (основное API)
```python
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
    prompt = f"Сгенерируй {request.type}-тест-кейсы по требованиям:\n{request.requirements}\nВ формате 
Allure TestOps as Code."
    response = await request_llm(prompt)
    return {"code": response}
```

**models.py** (схемы данных)
```python
from pydantic import BaseModel, HttpUrl

class TestCase(BaseModel):
    id: int
    code: str
    requirements: str
```

---

#### 2. Frontend (React)

**components/TestGenerator.tsx**
```typescript
import React, { useState } from 'react';
import axios from 'axios';

const TestGenerator = () => {
    const [requirements, setRequirements] = useState('');
    const [testType, setTestType] = useState('UI');
    const [generatedCode, setGeneratedCode] = useState('');

    const generateTests = async () => {
        try {
            const response = await axios.post('/api/generate', {
                requirements,
                type: testType
            });
            setGeneratedCode(response.data.code);
        } catch (error) {
            console.error('Error generating tests:', error);
        }
    };

    return (
        <div>
            <textarea value={requirements} onChange={(e) => setRequirements(e.target.value)} />
            <select value={testType} onChange={(e) => setTestType(e.target.value)}>
                <option value="UI">UI</option>
                <option value="API">API</option>
            </select>
            <button onClick={generateTests}>Generate</button>
            <pre>{generatedCode}</pre>
        </div>
    );
};
```

---

#### 3. Интеграция с GitLab

**app.py** (добавить эндпоинт для отправки кода в репозиторий)
```python
from fastapi import HTTPException

async def push_to_gitlab(repo_url: str, branch: str, code: str):
    # Используем GitLab API для создания/обновления README
    headers = {"Private-Token": config.GITLAB_TOKEN}
    data = {"content": code, "branch": branch}
    await httpx.post(repo_url, headers=headers, data=data)
```

---

#### 4. Docker и CI/CD

**docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - USER_TOKEN=your_cloudru_token
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

**.gitlab-ci.yml**
```yaml
image: python:3.9

stages:
  - test
  - deploy

test-job:
  script:
    - pip install -r requirements.txt
    - pytest tests/
```

---

#### 5. Пример вывода для UI-теста

```python
import allure
from selenium import webdriver

@allure.story("Калькулятор")
@allure.feature("Сложение")
def test_calculator_addition():
    driver = webdriver.Chrome()
    driver.get("http://localhost:3000/calculator")

    with allure.step("Ввод числа 5"):
        driver.find_element("id", "num1").send_keys("5")
    
    with allure.step("Выбор операции +"):
        driver.find_element("id", "operation").click()
    
    with allure.step("Ввод числа 3"):
        driver.find_element("id", "num2").send_keys("3")
    
    with allure.step("Проверка результата"):
        assert driver.find_element("id", "result").text == "8"
```

---

#### 6. Валидация и Оптимизация

**app.py** (оптимизация тестов)
```python
def optimize_tests(test_cases: List[TestCase]) -> List[dict]:
    prompt = f"Оптimize the following test cases: {test_cases}\nProvide recommendations for improving 
coverage."
    response = request_llm(prompt)
    return response["recommendations"]
```

---

### Инструкция по эксплуатации
1. Установите зависимости: `pip install fastapi uvicorn httpx`
2. Запустите сервер: `uvicorn app:app --reload`
3. Откройте `http://localhost:3000` для использования интерфейса
4. Для интеграции с GitLab добавьте токены в `config.py`

### Особенности реализации
- Использование асинхронных запросов к LLM для эффективности
- Реактивный интерфейс для комфортного взаимодействия
- CI/CD интеграция для автоматизации процессов
- Поддержка обеих типов тестов (UI и API) в единой системе

Для улучшения результатов можно добавить:
- Более детальную валидацию структуры тестов
- Историю генераций для анализа трендов
- Машинное обучение для подбора оптимальных параметров тестов
