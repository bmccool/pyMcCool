""" A class for math operations and utilities """
from collections.abc import Sequence
from typing import overload, Iterator
from typing_extensions import (
    Self,
    SupportsIndex,
    final,
)

@final
class InclusiveRange(Sequence[int]):
    @property
    def start(self) -> int: ...
    @property
    def stop(self) -> int: ...
    @property
    def step(self) -> int: ...
    @overload
    def __new__(cls, __stop: SupportsIndex) -> Self: ...
    @overload
    def __new__(cls, __start: SupportsIndex, __stop: SupportsIndex, __step: SupportsIndex = ...) -> Self: ...
    def count(self, __value: int) -> int: ...
    def index(self, __value: int) -> int: ...  # type: ignore[override]
    def __len__(self) -> int: ...
    def __eq__(self, __value: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __contains__(self, __key: object) -> bool: ...
    def __iter__(self) -> Iterator[int]: ...
    @overload
    def __getitem__(self, __key: SupportsIndex) -> int: ...
    @overload
    def __getitem__(self, __key: slice) -> range: ...
    def __reversed__(self) -> Iterator[int]: ...