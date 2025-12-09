from pydantic import BaseModel, HttpUrl

class TestCase(BaseModel):
    id: int
    code: str
    requirements: str