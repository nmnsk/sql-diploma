from typing import Any


def update_attrs(instance: Any, **kwargs: Any) -> None:
    for k, v in kwargs.items():
        setattr(instance, k, v)
