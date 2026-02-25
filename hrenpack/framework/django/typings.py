from typing import Protocol, TypeVar, Dict, Any

D = TypeVar('D', default=Dict[str, Any])


class Form(Protocol[D]):
    cleaned_data: D

    def is_valid(self) -> bool: ...
