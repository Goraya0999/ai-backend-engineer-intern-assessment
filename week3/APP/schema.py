from pydantic import BaseModel, Field


class BaseTask(BaseModel):
    pass


class CreateTask(BaseTask):
    title: str = Field(min_length=1)
    done: bool = False


class UpdateTask(BaseTask):
    title: str = Field(min_length=1)
    done: bool = False


class ReadTask(BaseTask):
    id: int
    title: str
    done: bool
