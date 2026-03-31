from datetime import date
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
    due_date=date.today(),
    priority="high"
))
dog.add_task(CareTask(
    title="Bath Time",
    duration_minutes=45,
    description="Full grooming session",
    due_date=date.today(),
    priority="medium"
))

# Add task to Luna
cat.add_task(CareTask(
    title="Vet Checkup",
    duration_minutes=60,
    description="Annual wellness visit",
    due_date=date.today(),
    priority="high"
))

# Register pets with owner
owner.add_pet(dog)
owner.add_pet(cat)

# Generate and print plan
scheduler = Scheduler()
plan = scheduler.generate_plan(owner)

print("=== Today's Schedule ===")
print(scheduler.explain_plan(plan))
