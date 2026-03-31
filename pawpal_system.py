from dataclasses import dataclass, field
from datetime import date


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    description: str = ""
    due_date: date | None = None
    priority: str = "medium"  # "low", "medium", or "high"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        pass

    def remove_task(self, title: str) -> None:
        pass

    def list_tasks(self) -> list[CareTask]:
        ...

    def edit_task(self, title: str, new_title: str = None, new_duration: int = None, new_priority: str = None) -> None:
        pass


@dataclass
class Owner:
    name: str
    email: str = ""
    pets: list[Pet] = field(default_factory=list)
    available_minutes: int = 480  # default: 8 hours

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, name: str) -> None:
        pass

    def list_pets(self) -> list[Pet]:
        ...


class Scheduler:
    def get_all_tasks(self, owner: Owner) -> list[CareTask]:
        ...

    def get_tasks_by_priority(self, owner: Owner, priority: str) -> list[CareTask]:
        ...

    def generate_plan(self, owner: Owner) -> list[CareTask]:
        pass

    def explain_plan(self, plan: list[CareTask]) -> str:
        pass