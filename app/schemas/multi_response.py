from typing import Generic, Optional, Type, TypeVar, List

from pydantic import BaseModel

ModelType = TypeVar('ModelType')

class multi_response(BaseModel, Generic[ModelType]):
    count : int
    next : str
    previous : str
    results : List[ModelType]
