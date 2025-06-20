from typing import List, Optional, TypeVar

from pydantic import BaseModel

MODEL_T = TypeVar("MODEL_T", bound=BaseModel)


class APIResponse(BaseModel):
    pass


class APIPaginationMetaData(BaseModel):
    result_count: int
    page_count: int
    page_size: int
    current_page: int
    next_page: Optional[int]
    previous_page: Optional[int]


class APIPaginatedResponse(BaseModel):
    pagination: APIPaginationMetaData
    results: List[MODEL_T]
