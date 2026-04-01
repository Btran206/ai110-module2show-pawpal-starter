from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    description: str = ""
    due_datetime: datetime | None = None
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
        """Remove the first task matching the given title and decrement the task counter."""
        for i, t in enumerate(self.tasks):
            if t.title == title:
                self.tasks.pop(i)
                self.task_count -= 1
                return

    def remove_task_at(self, index: int) -> None:
        """Remove the task at the given index and decrement the task counter."""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.task_count -= 1

    def list_tasks(self) -> list[CareTask]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def edit_task(self, title: str, new_title: str | None = None, new_duration: int | None = None,
                  new_priority: str | None = None, new_description: str | None = None,
                  new_due_datetime: datetime | None = None) -> None:
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
                if new_due_datetime is not None:
                    task.due_datetime = new_due_datetime
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
    _PRIORITY_ORDER = {"low": 0, "medium": 1, "high": 2}

    def get_all_tasks(self, owner: Owner) -> list[CareTask]:
        """Return a flat list of all tasks across every pet the owner has."""
        all_tasks = []
        for pet in owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_tasks_by_priority(self, owner: Owner) -> list[CareTask]:
        """Return all tasks sorted by priority, with due-datetime urgency as a tiebreaker.

        Tasks due sooner are ranked higher within the same priority level.
        Overdue tasks are treated as most urgent. Tasks with no due datetime rank last.
        """
        now = datetime.now()

        def sort_key(task):
            is_overdue = bool(task.due_datetime and task.due_datetime < now)
            priority_rank = -self._PRIORITY_ORDER.get(task.priority, 1)
            if task.due_datetime:
                seconds_until_due = (task.due_datetime - now).total_seconds()
            else:
                seconds_until_due = float("inf")  # no due date → sort last
            return (not is_overdue, priority_rank, seconds_until_due)

        return sorted(self.get_all_tasks(owner), key=sort_key)

    def filter_tasks_by_pet(self, owner: Owner, pet_name: str) -> list[CareTask]:
        """Return all tasks belonging to the pet with the given name."""
        return [t for t in self.get_all_tasks(owner) if t.pet_name == pet_name]

    def generate_plan(self, owner: Owner) -> tuple[list[CareTask], list[CareTask]]:
        """Build a schedule of incomplete tasks that fits within the owner's available minutes.

        Returns a tuple of (scheduled_tasks, excluded_tasks) so callers can surface
        what got dropped due to time constraints.
        """
        tasks = self.get_tasks_by_priority(owner)
        plan = []
        excluded = []
        remaining = owner.available_minutes
        for task in tasks:
            if task.completed:
                continue
            if task.duration_minutes <= remaining:
                plan.append(task)
                remaining -= task.duration_minutes
            else:
                excluded.append(task)
        return plan, excluded

    def explain_plan(self, plan: list[CareTask], excluded: list[CareTask] | None = None) -> str:
        """Return a human-readable summary of the scheduled plan.

        If excluded tasks are provided, appends a section listing what was dropped.
        """
        if not plan and not excluded:
            return "No tasks scheduled."
        lines = []
        total = 0
        if plan:
            for task in plan:
                lines.append(f"- [{task.priority.upper()}] {task.title} ({task.pet_name}) — {task.duration_minutes} min")
                total += task.duration_minutes
            lines.append(f"\nTotal time: {total} min")
        else:
            lines.append("No tasks fit within available time.")
        if excluded:
            lines.append("\nNot scheduled (insufficient time):")
            for task in excluded:
                lines.append(f"  * [{task.priority.upper()}] {task.title} ({task.pet_name}) — {task.duration_minutes} min")
        return "\n".join(lines)