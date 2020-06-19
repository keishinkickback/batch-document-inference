import abc
from typing import TypeVar

Result = TypeVar("Result")


class Result(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __add__(self, new_result: Result) -> Result:
        pass

    @abc.abstractmethod
    def add(self) -> None:
        pass

    @abc.abstractmethod
    def to_dict(self) -> dict:
        pass

    def __repr__(self) -> str:
        lines = [f"  {k}={v}" for k, v in self.to_dict().items()]
        str_lines = ",\n".join(lines)
        string = f"""{type(self).__name__}(\n{str_lines}\n)"""
        return string
