from datetime import datetime, timedelta

from pawpal_system import CareTask, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = CareTask(title="Feed", duration_minutes=10)
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_task_count():
    pet = Pet(name="Buddy", species="Dog")
    task = CareTask(title="Walk", duration_minutes=30)
    assert pet.task_count == 0
    pet.add_task(task)
    assert pet.task_count == 1


def test_get_tasks_by_priority_sorts_high_to_low():
    owner = Owner(name="Alex", available_minutes=480)
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(CareTask(title="Low Task", duration_minutes=10, priority="low"))
    pet.add_task(CareTask(title="High Task", duration_minutes=10, priority="high"))
    pet.add_task(CareTask(title="Medium Task", duration_minutes=10, priority="medium"))
    owner.add_pet(pet)

    sorted_tasks = Scheduler().get_tasks_by_priority(owner)
    priorities = [t.priority for t in sorted_tasks]
    assert priorities == ["high", "medium", "low"]


def test_generate_plan_does_not_exceed_available_minutes():
    owner = Owner(name="Alex", available_minutes=60)
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(CareTask(title="Walk", duration_minutes=40, priority="high"))
    pet.add_task(CareTask(title="Bath", duration_minutes=40, priority="medium"))
    owner.add_pet(pet)

    plan, excluded = Scheduler().generate_plan(owner)
    total = sum(t.duration_minutes for t in plan)
    assert total <= owner.available_minutes


def test_overdue_tasks_sort_before_non_overdue_same_priority():
    owner = Owner(name="Alex", available_minutes=480)
    pet = Pet(name="Buddy", species="Dog")
    future = datetime.now() + timedelta(hours=2)
    past = datetime.now() - timedelta(hours=1)
    pet.add_task(CareTask(title="Future Task", duration_minutes=10, priority="medium", due_datetime=future))
    pet.add_task(CareTask(title="Overdue Task", duration_minutes=10, priority="medium", due_datetime=past))
    owner.add_pet(pet)
    sorted_tasks = Scheduler().get_tasks_by_priority(owner)
    assert sorted_tasks[0].title == "Overdue Task"


def test_no_due_date_sorts_last_within_priority():
    owner = Owner(name="Alex", available_minutes=480)
    pet = Pet(name="Buddy", species="Dog")
    future = datetime.now() + timedelta(hours=3)
    pet.add_task(CareTask(title="No Date Task", duration_minutes=10, priority="high"))
    pet.add_task(CareTask(title="Has Date Task", duration_minutes=10, priority="high", due_datetime=future))
    owner.add_pet(pet)
    sorted_tasks = Scheduler().get_tasks_by_priority(owner)
    assert sorted_tasks[0].title == "Has Date Task"
    assert sorted_tasks[1].title == "No Date Task"


def test_filter_tasks_by_pet_returns_only_that_pets_tasks():
    owner = Owner(name="Alex", available_minutes=480)
    buddy = Pet(name="Buddy", species="Dog")
    buddy.add_task(CareTask(title="Walk", duration_minutes=30))
    whiskers = Pet(name="Whiskers", species="Cat")
    whiskers.add_task(CareTask(title="Brush", duration_minutes=15))
    owner.add_pet(buddy)
    owner.add_pet(whiskers)
    result = Scheduler().filter_tasks_by_pet(owner, "Buddy")
    assert len(result) == 1
    assert result[0].title == "Walk"


def test_generate_plan_skips_completed_tasks():
    owner = Owner(name="Alex", available_minutes=60)
    pet = Pet(name="Buddy", species="Dog")
    done = CareTask(title="Done Task", duration_minutes=40, priority="high")
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(CareTask(title="Pending Task", duration_minutes=40, priority="medium"))
    owner.add_pet(pet)
    plan, excluded = Scheduler().generate_plan(owner)
    titles = [t.title for t in plan]
    assert "Done Task" not in titles
    assert "Pending Task" in titles


def test_remove_task_decrements_task_count():
    pet = Pet(name="Buddy", species="Dog")
    pet.add_task(CareTask(title="Walk", duration_minutes=30))
    assert pet.task_count == 1
    pet.remove_task("Walk")
    assert pet.task_count == 0
