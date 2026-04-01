from datetime import datetime
from pawpal_system import CareTask, Pet, Owner, Scheduler

# Create owner
owner = Owner(name="Alex", email="alex@email.com", available_minutes=120)

# Create pets
dog = Pet(name="Buddy", species="Dog")
cat = Pet(name="Luna", species="Cat")

# Add tasks to Buddy
dog.add_task(CareTask(
    title="Morning Walk",
    duration_minutes=30,
    description="Walk around the block",
    due_datetime=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
    priority="high"
))
dog.add_task(CareTask(
    title="Bath Time",
    duration_minutes=45,
    description="Full grooming session",
    due_datetime=datetime.now().replace(hour=14, minute=0, second=0, microsecond=0),
    priority="medium"
))

# Add task to Luna
cat.add_task(CareTask(
    title="Vet Checkup",
    duration_minutes=60,
    description="Annual wellness visit",
    due_datetime=datetime.now().replace(hour=10, minute=30, second=0, microsecond=0),
    priority="high"
))

# Register pets with owner
owner.add_pet(dog)
owner.add_pet(cat)

# Generate and print plan
scheduler = Scheduler()
plan, excluded = scheduler.generate_plan(owner)

print("=== Today's Schedule ===")
print(scheduler.explain_plan(plan, excluded))
