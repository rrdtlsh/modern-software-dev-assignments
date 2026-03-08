# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Raudatul Sholehah** \
SUNet ID: **Not applicable** \
Citations: **N/A**

This assignment took me about **5** hours to do. 


## YOUR RESPONSES

**Note to Grader:** Due to the Claude Code CLI requiring a paid Pro/Max subscription which I do not currently have access to, I implemented a hybrid approach. I created the required `.claude/commands/*.md` and `CLAUDE.md` files to demonstrate my understanding of Claude Code's architecture and slash commands. To actually execute the autonomous agent workflow, I used **Cursor Composer (Agent Mode)** and a `.cursorrules` file to act as the Agent Manager. This perfectly aligns with the learning goals of Agentic Workflows.

### Automation #1: Generate Tests Agent
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> The design of this automation was inspired by the concept of AI agents acting as specialized sub-agents (e.g., a "TestAgent") to assist developers in repetitive tasks. Based on the course material on becoming an Agent Manager, AI can support software engineering workflows such as testing to improve productivity and ensure reliable code deployments.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Automatically generate missing pytest functions for FastAPI endpoints to improve test coverage.
> **Inputs:** The `backend/app/routers/` directory and existing `backend/tests/`.
> **Outputs:** New pytest functions using FastAPI `TestClient` for uncovered endpoints.
> **Steps:** > 1. Scan the FastAPI routes in the backend. 
> 2. Compare them with existing tests. 
> 3. Generate missing tests without modifying existing ones.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:** In the Claude Code CLI, this would be executed via `/generate-tests`. In my hybrid setup, I ran the exact prompt template in Cursor Composer Agent mode.
> **Expected output:** New test files/functions appended to the `backend/tests/` directory.
> **Safety notes:** The automation is instructed to never alter existing passing tests. It is recommended to use a checkpoint-heavy workflow (commit before running the agent) to easily rollback if the generated tests fail.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Developers had to manually inspect routers, cross-reference them with the test folder, and write boilerplate code to test missing endpoints. 
> **After:** The AI autonomously analyzes the backend routes and proposes new tests, reducing mental overhead and guaranteeing comprehensive coverage.

e. How you used the automation to enhance the starter application
> I used this automation to scan the starter app's backend. The agent successfully identified that the `GET /notes/{note_id}` endpoint lacked direct test coverage. It autonomously generated `test_get_note_by_id` and `test_get_note_not_found` (to test the 404 error path) using the shared `client` fixture. I accepted the changes and verified them by running `pytest backend/tests`, which successfully passed.


### Automation #2: Improve Docs Agent
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> This automation was inspired by the need for AI-assisted code maintenance. Documentation is often neglected during fast-paced development. Anthropic's internal teams use Claude Code to synthesize documentation and explain complex codebases; this agent flips that concept by writing the documentation directly into the source code.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Enhance the documentation quality of the backend code without altering application logic.
> **Inputs:** Python source files in the `backend/app/` directory.
> **Outputs:** The same Python files updated with PEP-257 standard docstrings.
> **Steps:** > 1. Scan backend directory. 
> 2. Identify functions and classes lacking documentation. 
> 3. Add clear docstrings explaining purpose, parameters, and return types.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:** In Claude Code CLI, this is triggered via `/improve-docs`. In my setup, I executed the prompt template via Cursor Composer.
> **Expected output:** Python files updated with docstrings.
> **Safety notes:** The agent is strictly constrained to only add documentation and not touch application logic. Always run `black .` and `ruff check .` afterward to ensure the new comments do not break formatting rules.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Functions and classes lacked context, requiring developers to read through implementation logic to understand parameters and returns. 
> **After:** The AI scans the entire backend and standardizes documentation in one click, saving hours of manual typing and ensuring consistency.

e. How you used the automation to enhance the starter application
> I applied this automation to the starter app's backend. The agent effectively scanned files like `main.py`, `notes.py`, `action_items.py`, and the database models. It added concise, standard docstrings to all endpoints and classes (e.g., explaining that `Notes` returns a `NoteRead` model). I verified the changes visually and ensured formatting was maintained using `black` and `ruff`.


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> N/A

b. Design of each automation, including goals, inputs/outputs, steps
> N/A

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> N/A

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> N/A

e. How you used the automation to enhance the starter application
> N/A