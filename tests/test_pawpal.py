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

    plan = Scheduler().generate_plan(owner)
    total = sum(t.duration_minutes for t in plan)
    assert total <= owner.available_minutes
