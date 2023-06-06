from types import FrameType
from typing import Any, Callable, Dict, Tuple, Union
from uuid import UUID

RelationshipIdentifier = Union[UUID, str, int, float]
"""идентификатор взаимосвязанности"""

FuncToPatch = Callable
FuncToPathcArgs = Tuple[Any]
FuncToPatchKwargs = Dict[Any, Any]
DecoratorInnerFunc = Callable[[FuncToPatch, FuncToPathcArgs, FuncToPatchKwargs, FrameType, RelationshipIdentifier], Any]
