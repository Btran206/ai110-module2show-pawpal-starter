from dataclasses import dataclass, field


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str = "medium"  # "low", "medium", or "high"
    completed: bool = False


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)
    available_minutes: int = 480  # default: 8 hours

    def add_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def generate_plan(self, owner: Owner) -> list[CareTask]:
        pass
