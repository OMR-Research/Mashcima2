import punq
from typing import TypeVar, Type


T = TypeVar("T")
U = TypeVar("U", bound=T)


class Container:
    """Service container used for Model services"""
    def __init__(self, register_itself=True):
        self._container = punq.Container()

        # register the container itself into the container
        if register_itself:
            self.instance(Container, self)
    
    def instance(self, instance_type: Type[T], instance: T):
        self._container.register(instance_type, instance=instance)

    def type(self, concrete_type: Type[T]):
        self._container.register(
            concrete_type,
            scop=punq.Scope.singleton
        )

    def interface(self, abstract_type: Type[T], concrete_type: Type[U]):
        self._container.register(
            abstract_type,
            concrete_type,
            scope=punq.Scope.singleton
        )
    
    def resolve(self, resolve_type: Type[T]) -> T:
        return self._container.resolve(resolve_type)
