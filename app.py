import streamlit as st
from pawpal_system import CareTask, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.caption("Plan and schedule daily care tasks for your pets.")

st.divider()

# Initialize session state once so objects persist across Streamlit reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="", available_minutes=10)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "plan" not in st.session_state:
    st.session_state.plan = []
if "excluded" not in st.session_state:
    st.session_state.excluded = []

# --- Owner Registration (Sidebar) ---
# Updates the existing owner in-place so pets are not wiped on re-submit
with st.sidebar:
    st.header("Owner Profile")
    with st.form("owner_form"):
        owner_name = st.text_input("Name", value=st.session_state.owner.name)
        owner_email = st.text_input("Email", value=st.session_state.owner.email)
        available_minutes = st.number_input("Available minutes today", min_value=10, max_value=1440, value=st.session_state.owner.available_minutes)
        owner_submitted = st.form_submit_button("Save")

    if owner_submitted:
        st.session_state.owner.name = owner_name
        st.session_state.owner.email = owner_email
        st.session_state.owner.available_minutes = int(available_minutes)

    owner = st.session_state.owner
    st.markdown(f"**Name:** {owner.name or '—'}")
    st.markdown(f"**Email:** {owner.email or '—'}")
    st.markdown(f"**Available minutes:** {owner.available_minutes}")

owner = st.session_state.owner

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
    st.table([{"name": p.name, "species": p.species, "task_count": p.task_count} for p in pets])

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
    description = st.text_input("Description", value="")
    due_date = st.date_input("Due date", value=None)
    due_time = st.time_input("Due time", value=None)

    if st.button("Add task"):
        from datetime import datetime, time
        due_datetime = datetime.combine(due_date, due_time if due_time else time(0, 0)) if due_date else None
        task = CareTask(title=task_title, duration_minutes=int(duration), priority=priority,
                        description=description, due_datetime=due_datetime)
        selected_pet.add_task(task)

    # Show task list and remove/complete options only when tasks exist for the selected pet
    if selected_pet.list_tasks():
        st.write(f"Tasks for {selected_pet.name}:")
        st.table([{
            "title": t.title,
            "description": t.description,
            "due_datetime": t.due_datetime.strftime("%Y-%m-%d %H:%M") if t.due_datetime else "—",
            "duration_minutes": t.duration_minutes,
            "priority": t.priority,
            "completed": t.completed
        } for t in selected_pet.list_tasks()])

        all_titles = [t.title for t in selected_pet.list_tasks()]
        task_labels = [
            f"{t.title} id:{i}" if all_titles.count(t.title) > 1 else t.title
            for i, t in enumerate(selected_pet.list_tasks())
        ]
        selected_idx = st.selectbox(
            "Select a task", range(len(task_labels)),
            format_func=lambda i: task_labels[i], key="task_action_select"
        )
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("Mark complete", use_container_width=True):
                selected_pet.list_tasks()[selected_idx].mark_complete()
                st.rerun()
        with action_col2:
            if st.button("Remove task", use_container_width=True):
                selected_pet.remove_task_at(selected_idx)
                st.rerun()
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

pet_filter_options = ["All pets"] + [p.name for p in owner.list_pets()]
pet_filter = st.selectbox("Filter by pet", pet_filter_options, key="task_pet_filter")
if pet_filter != "All pets":
    all_tasks = scheduler.filter_tasks_by_pet(owner, pet_filter)

if all_tasks:
    with st.expander("View tasks"):
        st.table([{"pet": t.pet_name, "title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority, "due_datetime": t.due_datetime.strftime("%Y-%m-%d %H:%M") if t.due_datetime else "—"} for t in all_tasks])
else:
    st.info("No tasks added yet.")

# Generate a plan fitted to the owner's available minutes and store it in session state
if st.button("Generate schedule"):
    st.session_state.plan, st.session_state.excluded = scheduler.generate_plan(owner)

# Display the human-readable schedule explanation
if st.session_state.plan or st.session_state.excluded:
    from datetime import datetime
    now = datetime.now()
    st.markdown("### Today's Schedule")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tasks Scheduled", len(st.session_state.plan))
    col2.metric("Tasks Excluded", len(st.session_state.excluded))
    col3.metric("Minutes Used", sum(t.duration_minutes for t in st.session_state.plan))

    for task in st.session_state.plan:
        if task.completed:
            st.success(f"✓ {task.title} ({task.pet_name}) — {task.duration_minutes} min")
        elif task.due_datetime and task.due_datetime < now:
            st.error(f"⚠ OVERDUE: {task.title} ({task.pet_name}) — {task.priority} priority, {task.duration_minutes} min")
        else:
            st.warning(f"• {task.title} ({task.pet_name}) — {task.priority} priority, {task.duration_minutes} min")

    if st.session_state.excluded:
        st.markdown("**Excluded (insufficient time):**")
        for task in st.session_state.excluded:
            st.error(f"✗ {task.title} ({task.pet_name}) — {task.duration_minutes} min needed")
