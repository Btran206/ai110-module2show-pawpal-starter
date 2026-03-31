from __future__ import annotations
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
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[CareTask] = field(default_factory=list)
    task_count: int = 0

    def add_task(self, task: CareTask) -> None:
        """Add a task to this pet and increment the task counter."""
        task.pet_name = self.name
        self.tasks.append(task)
        self.task_count += 1

    def remove_task(self, title: str) -> None:
        """Remove the task matching the given title and decrement the task counter."""
        self.tasks = [t for t in self.tasks if t.title != title]
        self.task_count -= 1

    def list_tasks(self) -> list[CareTask]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def edit_task(self, title: str, new_title: str | None = None, new_duration: int | None = None,
                  new_priority: str | None = None, new_description: str | None = None,
                  new_due_date: date | None = None) -> None:
        """Update any provided fields on the task matching the given title."""
        for task in self.tasks:
            if task.title == title:
                if new_title is not None:
                    task.title = new_title
                if new_duration is not None:
                    task.duration_minutes = new_duration
                if new_priority is not None:
                    task.priority = new_priority
                if new_description is not None:
                    task.description = new_description
                if new_due_date is not None:
                    task.due_date = new_due_date
                break


@dataclass
class Owner:
    name: str
    email: str = ""
    pets: list[Pet] = field(default_factory=list)
    available_minutes: int = 480  # default: 8 hours

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove the pet matching the given name from this owner's pet list."""
        self.pets = [p for p in self.pets if p.name != name]

    def list_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


class Scheduler:
    def get_all_tasks(self, owner: Owner) -> list[CareTask]:
        """Return a flat list of all tasks across every pet the owner has."""
        all_tasks = []
        for pet in owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_tasks_by_priority(self, owner: Owner) -> list[CareTask]:
        """Return all tasks sorted from highest to lowest priority."""
        priority_order = {"low": 0, "medium": 1, "high": 2}
        return sorted(self.get_all_tasks(owner), key=lambda t: priority_order.get(t.priority, 1), reverse=True)

    def generate_plan(self, owner: Owner) -> list[CareTask]:
        """Build a schedule of incomplete tasks that fits within the owner's available minutes."""
        tasks = self.get_tasks_by_priority(owner)
        plan = []
        remaining = owner.available_minutes
        for task in tasks:
            if not task.completed and task.duration_minutes <= remaining:
                plan.append(task)
                remaining -= task.duration_minutes
        return plan

    def explain_plan(self, plan: list[CareTask]) -> str:
        """Return a human-readable summary of the scheduled plan."""
        if not plan:
            return "No tasks scheduled."
        lines = []
        total = 0
        for task in plan:
            lines.append(f"- [{task.priority.upper()}] {task.title} ({task.pet_name}) — {task.duration_minutes} min")
            total += task.duration_minutes
        lines.append(f"\nTotal time: {total} min")
        return "\n".join(lines)