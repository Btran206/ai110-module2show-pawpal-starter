from datetime import datetime, timedelta
from pawpal_system import CareTask, Pet, Owner, Scheduler

# ── Setup ────────────────────────────────────────────────────────────────────

owner = Owner(name="Alex", email="alex@email.com", available_minutes=120)

dog = Pet(name="Buddy", species="Dog")
cat = Pet(name="Luna", species="Cat")

now = datetime.now()

# Buddy's tasks
dog.add_task(CareTask(
    title="Morning Walk",
    duration_minutes=30,
    description="Walk around the block",
    due_datetime=now - timedelta(minutes=30),  # overdue
    priority="high"
))
dog.add_task(CareTask(
    title="Bath Time",
    duration_minutes=45,
    description="Full grooming session",
    due_datetime=now + timedelta(hours=3),
    priority="medium"
))
dog.add_task(CareTask(
    title="Feed Buddy",
    duration_minutes=10,
    description="Morning kibble",
    due_datetime=now + timedelta(hours=1),
    priority="high"
))

# Luna's tasks
cat.add_task(CareTask(
    title="Vet Checkup",
    duration_minutes=60,
    description="Annual wellness visit",
    due_datetime=now + timedelta(hours=2),
    priority="high"
))
cat.add_task(CareTask(
    title="Clean Litter Box",
    duration_minutes=10,
    description="Scoop and replace litter",
    priority="medium"  # no due date
))
cat.add_task(CareTask(
    title="Playtime",
    duration_minutes=15,
    description="Feather wand session",
    due_datetime=now + timedelta(hours=5),
    priority="low"
))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler()

# Verify get_tasks_by_priority output by printing out all tasks sorted by priority
print("=" * 48)
print("  ALL TASKS — Sorted by Priority & Urgency")
print("=" * 48)
sorted_tasks = scheduler.get_tasks_by_priority(owner)
for task in sorted_tasks:
    overdue_flag = " *** OVERDUE ***" if task.due_datetime and task.due_datetime < now else ""
    due_str = task.due_datetime.strftime("%I:%M %p") if task.due_datetime else "no due time"
    print(f"  [{task.priority.upper():6}] {task.title} ({task.pet_name}) — {task.duration_minutes} min | due: {due_str}{overdue_flag}")

# Verify filter_tasks_by_pet output by printing out tasks for a specific pet
print()
print("=" * 48)
print("  BUDDY'S TASKS — Filtered by Pet")
print("=" * 48)
buddy_tasks = scheduler.filter_tasks_by_pet(owner, "Buddy")
for task in buddy_tasks:
    print(f"  - {task.title} | pet: {task.pet_name} | {task.priority} priority | {task.duration_minutes} min")

# Verify generate_plan output by printing out the generated plan
print()
print("=" * 48)
print(f"  TODAY'S PLAN — {owner.available_minutes} min available")
print("=" * 48)
plan, excluded = scheduler.generate_plan(owner)
print(scheduler.explain_plan(plan, excluded))
