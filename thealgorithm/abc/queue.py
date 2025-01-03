from collections.abc import Iterable

from .base import ABCIterable
from .node import Node


class Queue(ABCIterable):
    def __init__(self, values=None, size=1000):
        super().__init__()
        self._head = None
        self._tail = None
        self._max_size = size

        if values is not None:
            if not isinstance(values, Iterable):
                raise TypeError(f"{type(values).__name__} object is not an iterable.")
            self.extend(values)

    def __iter__(self):
        self._curr = self._head
        return self

    def __next__(self):
        if self._curr is None:
            raise StopIteration
        value = self._curr.value
        self._curr = self._curr.next
        return value

    def clear(self):
        self._size = 0
        self._head = None

    def enqueue(self, value):
        if not self:
            self._head = self._tail = Node(value)
            self._size = 1
            return

        if len(self) >= self._max_size:
            raise OverflowError("the queue has reached its maximum capacity.")

        self._tail.next = Node(value, next=self._tail.next, prev=self._tail)
        self._tail = self._tail.next
        self._size += 1

    def dequeue(self):
        if not self:
            raise IndexError("dequeue from empty queue")
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        return value

    def extend(self, other):
        if not isinstance(other, Iterable):
            raise TypeError(f"{type(other).__name__} object is not an iterable.")

        if len(self) + sum(1 for _ in other) > self._max_size:
            raise OverflowError("The queue has reached its maximum capacity.")

        for value in other:
            self.enqueue(value)
