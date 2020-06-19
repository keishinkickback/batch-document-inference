from dataclasses import dataclass, field
from typing import Any
from typing import List, Union

from typeguard import typechecked

from .result import Result

@typechecked
@dataclass
class Sentence:
    id_document: int
    text: str
    result: Any = field(default_factory=Result)
    id_sentence: Union[int, None] = None
    title: bool = False


@typechecked
@dataclass
class Document:
    id: int
    title: str = ""
    body: str = ""
    sentences: List[Sentence] = field(default_factory=list)
    result: Any = field(default_factory=Result)


@typechecked
@dataclass
class Entity:
    text: str
    ne_type: str
    confidence_score: float
    id_sentence: Union[int, None] = None
    position_start: Union[int, None] = None
    position_end: Union[int, None] = None
