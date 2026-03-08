# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Raudatul Sholehah** \
SUNet ID: **Not applicable** \
Citations: **N/A**

This assignment took me about **4** hours to do. 

## YOUR RESPONSES

### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> **Design:** A unified QA Workflow named "QA Check".
> **Goal:** Automate code formatting, linting, and testing to ensure code quality before commits.
> **Inputs:** Python source files in `backend/` and test files in `tests/`.
> **Outputs:** Formatted code (Black), fixed linting (Ruff), and test results (Pytest).
> **Steps:** 1. Set PYTHONPATH; 2. Run `black .`; 3. Run `ruff check . --fix`; 4. Run `pytest backend/tests`.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** I had to remember and manually type three separate commands. On Windows, I frequently encountered errors because I forgot to set the environment variable (`$env:PYTHONPATH`) for each new terminal session.
> **After:** I just trigger the "QA Check" from Warp Drive. It handles the environment setup and runs all tools in a single, error-free sequence.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> **Autonomy Level:** Execution Autonomy.
> **Permissions:** Full terminal access to run scripts and modify files.
> **Supervision:** I supervised the output logs. Since the command uses `;` as a separator, I checked each section's output to ensure Black, Ruff, and Pytest all finished successfully.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A for this specific automation.

e. How you used the automation (what pain point it resolves or accelerates)
> It resolves "command fatigue" and environment configuration errors on Windows. It accelerates the "Inner Loop" of development by making it effortless to verify code after every small change.


### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> **Design:** Concurrent feature development using Warp AI Agents.
> **Goal:** To implement Task 3 (Notes CRUD – medium difficulty) and Task 4 (Action Items Bulk Ops – medium difficulty)
> **Inputs:** Inputs:
- TASKS.md specifications
- existing FastAPI backend code
- natural language prompts given to Warp agents
> **Outputs:** Completed API endpoints, Pydantic schemas, and corresponding unit tests.
> **Steps:** 1. Open Tab 1 for Agent 1 (Notes); 2. Open Tab 2 for Agent 2 (Action Items); 3. Review and "Accept" diffs from both agents.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** I would have to code Task 3 manually, then move to Task 4. This is a linear process.
> **After:** Both tasks were handled by AI agents in parallel. I only acted as the "Manager" reviewing the logic, effectively cutting development time in half.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> **Autonomy Level:** High Autonomy ("Agent-take-the-wheel").
> **Permissions:** Permission to read the codebase, create/edit files, and run tests.
> **Supervision:** I used Warp's built-in diff viewer to inspect every code change. I only clicked "Accept" after ensuring the logic met the requirements in `TASKS.md`.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> **Roles:** Agent 1 (Notes Backend Specialist), Agent 2 (Tasks Backend Specialist).
> **Strategy:** Domain Separation. I explicitly told Agent 1 to stay within `notes.py` and Agent 2 to stay within `action_items.py` to prevent merge conflicts.
> **Concurrency Wins:** Both agents finished their respective tasks and tests in under 10 minutes.
> **Risks:** Concurrent edits to `main.py` or `schemas.py`. I mitigated this by accepting changes one by one.

e. How you used the automation (what pain point it resolves or accelerates)
> It resolves the bottleneck of manual boilerplate creation. It accelerates feature delivery by allowing parallel workflows, proving that a single developer can manage multiple "Agentic" workers to scale output.