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

The scheduler considers two main things: how much time the owner has in the day, and how urgent each task is. Urgency is a combination of priority level (high, medium, low) and due date — overdue tasks always bubble to the top, and within the same priority, tasks due sooner rank higher.

I decided time and urgency mattered most because those felt like the most real constraints a pet owner actually faces. You only have so many hours in the day, and some things genuinely can't wait (like medications or feeding). Things like personal preferences felt too hard to generalize cleanly without more user input, so I kept the model focused on what was concrete and actionable.

**b. Tradeoffs**

The scheduler only checks whether a task fits within the total time left in the day — it doesn't track actual start and end times. So if you had two 30-minute tasks and 60 minutes available, they'd both make the plan, but the scheduler has no idea *when* they'd actually happen or whether they'd bump into each other in real life.

I think that's a reasonable tradeoff here because pet care isn't really about booking exact calendar slots. You're not scheduling a meeting at 3pm — you're just making sure the dog gets walked and the cat gets fed sometime today. Keeping it as a simple budget model makes the logic a lot easier to follow and debug, and for most day-to-day pet care it works fine.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
