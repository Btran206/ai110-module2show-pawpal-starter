import streamlit as st
from pawpal_system import CareTask, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize session state once so objects persist across Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="", available_minutes=10)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "plan" not in st.session_state:
    st.session_state.plan = []

# --- Owner Registration ---
# Updates the existing owner in-place so pets are not wiped on re-submit
st.subheader("Registration")
with st.form("owner_form"):
    owner_name = st.text_input("Name", value=st.session_state.owner.name)
    owner_email = st.text_input("Email", value=st.session_state.owner.email)
    available_minutes = st.number_input("Available minutes today", min_value=10, max_value=1440, value=st.session_state.owner.available_minutes)
    owner_submitted = st.form_submit_button("Register")

if owner_submitted:
    st.session_state.owner.name = owner_name
    st.session_state.owner.email = owner_email
    st.session_state.owner.available_minutes = int(available_minutes)

# Display current owner summary
owner = st.session_state.owner
st.markdown(f"**Name:** {owner.name or '—'}")
st.markdown(f"**Email:** {owner.email or '—'}")
st.markdown(f"**Available minutes:** {owner.available_minutes}")

# --- Pet Management ---
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted = st.form_submit_button("Add pet")

if submitted:
    st.session_state.owner.add_pet(Pet(name=pet_name, species=species))

# Show pet list and remove option only when pets exist
pets = st.session_state.owner.list_pets()
if pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in pets])

    remove_name = st.selectbox("Select pet to remove", [p.name for p in pets], key="remove_pet")
    if st.button("Remove pet"):
        st.session_state.owner.remove_pet(remove_name)
        st.rerun()  # Force re-render so table reflects removal immediately
else:
    st.info("No pets yet. Add one above.")

# --- Task Management ---
st.subheader("Add a Task")

pets = st.session_state.owner.list_pets()
if pets:
    # Select which pet to assign the task to
    pet_names = [p.name for p in pets]
    selected_name = st.selectbox("Select pet", pet_names, key="add_task_pet")
    selected_pet = next(p for p in pets if p.name == selected_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        task = CareTask(title=task_title, duration_minutes=int(duration), priority=priority)
        selected_pet.add_task(task)

    # Show task list and remove option only when tasks exist for the selected pet
    if selected_pet.list_tasks():
        st.write(f"Tasks for {selected_pet.name}:")
        st.table([{"title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority} for t in selected_pet.list_tasks()])

        remove_task_title = st.selectbox("Select task to remove", [t.title for t in selected_pet.list_tasks()], key="remove_task")
        if st.button("Remove task"):
            selected_pet.remove_task(remove_task_title)
            st.rerun()  # Force re-render so table reflects removal immediately
    else:
        st.info(f"No tasks yet for {selected_pet.name}.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

# --- Scheduler ---
st.subheader("Build Schedule")

scheduler = st.session_state.scheduler
owner = st.session_state.owner

# Toggle between flat list (get_all_tasks) and priority-sorted list (get_tasks_by_priority)
sort_option = st.selectbox("Task view", ["All tasks", "Sorted by priority"], key="task_sort")
if sort_option == "Sorted by priority":
    all_tasks = scheduler.get_tasks_by_priority(owner)
else:
    all_tasks = scheduler.get_all_tasks(owner)

if all_tasks:
    with st.expander("View tasks"):
        st.table([{"pet": t.pet_name, "title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority} for t in all_tasks])
else:
    st.info("No tasks added yet.")

# Generate a plan fitted to the owner's available minutes and store it in session state
if st.button("Generate schedule"):
    st.session_state.plan = scheduler.generate_plan(owner)

# Display the human-readable schedule explanation
if st.session_state.plan:
    st.markdown("### Today's Schedule")
    st.text(scheduler.explain_plan(st.session_state.plan))
