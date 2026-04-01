# PawPal+ Project Reflection

## 1. System Design
The three core actions a user should be able to perform includes:
Add a pet:
The user can setup their pet's profile with name, species, age, needs, etc.

Add/edit tasks:
The user can add tasks like walk, feed, meds, grooming, etc and set priorities. Users also have the ability to revise/remove tasks.

Generate plan with explanation:
The user can generate a daily schedule that fits the pets needs with a short explanation of why each task was chosen/ordered.

**a. Initial design**

- Briefly describe your initial UML design.

My UML uses a simple chain: an Owner owns one or more Pet objects, and each Pet has its own list of CareTask objects. The scheduler processes the owner's preferences, etc and figures out a plan from there.

- What classes did you include, and what responsibilities did you assign to each?

Owner is the starting point it holds the person's name, how much time they have in a day, and the list of pets they're caring for. Pet stores the pet's name and species, and it keeps track of its own tasks. CareTask holds the tasks, duration, priority level, and a flag for whether it's done. The Scheduler processes the owner, and it figures out what tasks to fit into the day.

**b. Design changes**

- Did your design change during implementation?

Yes after asking the AI to review the skeleton, It suggested some changes.
- If yes, describe at least one change and why you made it.

There was missing functionality within the readme specs that I did not address. I added an edit function to the skeleton because the readme specifies that it needed this functionality. The AI also found that caretask has no reference to a pet_name which is problematic because when flattening all tasks with the scheduler, you would loses the context of which task belongs to which pet. So I added a pet_name attribute to CareTask to address this issue.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers two things: how much time the owner has in the day, and how urgent each task is. Urgency is a combination of priority level (high, medium, low) and due date. Overdue tasks are also considered and always takes the highest priority. Tasks due sooner also rank higher.

- How did you decide which constraints mattered most?

I decided time and urgency mattered most because those felt like the most real constraints a pet owner would actually face. An owner can only drop off an pick up within a certain window, and some things genuinely can't wait (like medications or feeding). Things like personal preferences felt too hard to generalize cleanly without more user input, so I kept the model focused on what was concrete and actionable.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler only checks whether a task fits within the total time left in the day. It doesn't track actual start and end times. So if you had two 30-minute tasks and 60 minutes available, they'd both make the plan, but the scheduler has no idea when they'd actually happen or whether they'd would have scheduling conflicts.

- Why is that tradeoff reasonable for this scenario?

I think that's a reasonable tradeoff because pet care isn't really about booking exact calendar slots. You're not scheduling a meeting at 3pm you're just making sure the dog gets walked and the cat gets fed sometime today. Keeping it as a simple makes the logic a lot easier to follow and debug, and for most day-to-day pet care I think it would work fine.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used Ai to do all three of the above things, brainstorm, debug, and refactor. I used the AI to brainstorm an initial UML design and then polish it as new features were added. I also used AI to debug, especially when interacting with the streamlit UI itself and seeing behavior that wasn't normal. I also used AI to refactor that was complex and made it more simple and easier to understand for humans. 

- What kinds of prompts or questions were most helpful?

The most helpful prompts were the ones where I asked the AI to critique what I proposed. It definitely helped polish up some things like the UI for example or if my current method logic was sound or not. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

One moment where I didn't accept the AI suggestion for example was during the UI polishing phase where it suggested to change all the tables to st.dataframe. Making the tables a dataframe instead kind of destroys the purpose of all the sorting/filtering logic I implemented within the Scheduler because you can simply click the button on the df and it would sort.

- How did you evaluate or verify what the AI suggested?

I evaluated what the AI suggested by first looking at the suggested code and see if it made sense. If it did I would approve it. I then verified if the suggested changes caused any buggy behavior within the streamlit UI and also added test cases to see if the logic worked correctly.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I created 9 total tests for the core classes. The first four covered marking a task complete, confirming that task_count increments when a task is added, verifying that get_tasks_by_priority returns tasks in high → medium → low order, and checking that generate_plan never exceeds the owner's available time budget.

The remaining five tests targeted edge cases in the sorting and scheduling logic. I tested that overdue tasks were always prioritized before non-overdue tasks of the same priority. I also tested that tasks with no due date sort last within their priority group because they use float("inf") as a tiebreaker. I tested filter_tasks_by_pet with two pets to make sure tasks don't bleed across pets. I tested generate_plan to see if it completely ignores completed tasks, so they don't consume the time budget. And I tested that remove_task properly decrements task_count after a task is deleted.

- Why were these tests important?

The first four tests confirmed basic functionality that each class is supposed to fulfill. Kind of like a sanity check. The edge case tests mattered because they target logic that are likely to fail. Overall these test are important when trying to debug the code for expected functionality.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I'm confident in the core scheduling logic. The tests cover the main priority ordering rules, time allowed, and completed task exclusion. If I were to give it a rating it would be 4 stars.

- What edge cases would you test next if you had more time?

I'd test what happens when the owner has zero available minutes, when all tasks are already completed, and when two tasks have the exact same priority and due datetime.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm satisfied with the fact that I completed this project. The UI is somewhat clean and basic functionality was implemented.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would definitely address scheduling conflicts, and add more functionality to the scheduler like dealing with recurring tasks. I would also like to mess around with the streamlit app more to see if I can break it. I also did not connect one of the methods within the streamlit UI which was edit_task.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI is a good way to learn how to code. I am not the best with OOP so utilizing AI to ask clarifying questions and understand what is really going on helped out a lot.