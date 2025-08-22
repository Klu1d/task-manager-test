from dataclasses import dataclass


@dataclass(slots=True)
class TaskDTO:
    title: str
    description: str
