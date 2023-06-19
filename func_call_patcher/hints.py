from types import FrameType
from typing import Any, Callable, Dict, Tuple, Union
from uuid import UUID

RelationshipIdentifier = Union[UUID, str, int, float]
"""идентификатор взаимосвязанности"""

FuncToPatch = Callable
FuncToPatchArgs = Tuple[Any]
FuncToPatchKwargs = Dict[Any, Any]
DecoratorInnerFunc = Callable[[FuncToPatch, FuncToPatchArgs, FuncToPatchKwargs, FrameType, RelationshipIdentifier], Any]
