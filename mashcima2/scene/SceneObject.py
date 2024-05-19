from typing import Any, List
from dataclasses import dataclass, field


class Link:
    source: "SceneObject"
    target: "SceneObject"
    name: str

    def __init__(self, source: "SceneObject", target: "SceneObject", name: str):
        self.source = source
        self.target = target
        self.name = name
    
    def __repr__(self) -> str:
        return f"{self.source.__class__.__name__}-->" + \
            f"{self.target.__class__.__name__}"


@dataclass
class SceneObject:
    inlinks: List[Link] = field(default_factory=list, init=False, repr=False)
    outlinks: List[Link] = field(default_factory=list, init=False, repr=False)

    def __setattr__(self, name: str, value: Any) -> None:
        if isinstance(value, SceneObject):
            self.replace_outlink(target=value, name=name)
            value.replace_inlink(source=self, name=name)

        super().__setattr__(name, value)
    
    def replace_outlink(self, target: "SceneObject", name: str):
        # remove the outlink with the given name
        self.outlinks = [
            l for l in self.outlinks
            if l.name != name
        ]

        # add the new outlink
        self.outlinks.append(Link(self, target, name))

    def replace_inlink(self, source: "SceneObject", name: str):
        # remove the inlink from the given source via the given name
        self.outlinks = [
            l for l in self.outlinks
            if not (l.name == name and l.source is source)
        ]

        # add the new inlink
        self.inlinks.append(Link(source, self, name))
