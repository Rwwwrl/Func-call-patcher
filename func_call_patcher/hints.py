from types import FrameType
from typing import Any, Callable, Dict, Tuple

FuncToPatch = Callable
FuncToPathcArgs = Tuple[Any]
FuncToPatchKwargs = Dict[Any, Any]
DecoratorInnerFunc = Callable[[FuncToPatch, FuncToPathcArgs, FuncToPatchKwargs, FrameType], Any]
