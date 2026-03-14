# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Raudatul Sholehah** \
SUNet ID: **Not applicable** \
Citations: **Cursor AI Assistant, Graphite Diamond AI Documentation**

This assignment took me about **4-5** hours to do. 

---

# Task 1: Add more endpoints and validations

### a. Links to relevant commits/issues
> https://github.com/rrdtlsh/modern-software-dev-assignments/pull/1

### b. PR Description
> **Problem & Approach:** Needed to add a `/notes/search` and `/action-items/status/{status}` endpoint. Used FastAPI and SQLAlchemy `select()` with `.where()` clauses to implement this safely. Added Pydantic validations.
> **Summary of Testing:** Ran command `pytest backend/tests`. Result: 3 passed. The existing endpoints were not broken.
> **Tradeoffs, Limitations, or Follow-ups:** The PR only added GET endpoints. A follow-up is needed to implement full DELETE operations as those are still missing from the CRUD lifecycle.

### c. Graphite Diamond generated code review
> Graphite Diamond executed successfully ("Graphite found no issues" for the code itself). However, the Graphite Chat AI provided a highly insightful critique regarding documentation drift. It astutely noted: *"The description lists CRUD endpoints, but the diff only shows new GET/search... DELETE endpoints are missing for both Notes and Action Items."*

---

# Task 2: Extend extraction logic

### a. Links to relevant commits/issues
> https://github.com/rrdtlsh/modern-software-dev-assignments/pull/2

### b. PR Description
> **Problem & Approach:** The `extract_action_items` function needed to detect more complex patterns without breaking existing tests. Used string parsing methods (`startswith`, `endswith`) to strip bullet points gracefully via a new `_remove_bullet` helper, and preserved the original text casing.
> **Summary of Testing:** Ran command `pytest backend/tests`. Result: 7 passed. The new logic passed both old and new test coverage.
> **Tradeoffs, Limitations, or Follow-ups:** The string manipulation is simple and deterministic, but a limitation is that it might fail on highly irregular edge cases (e.g., misspelled "TO-DO:"). A follow-up could involve replacing this with a more robust regex or NLP model.

### c. Graphite Diamond generated code review
> Graphite Diamond reviewed the logic and returned "Graphite found no issues." The AI approved the refactoring, effectively validating that the pattern matching was structurally sound and that the `_remove_bullet` helper function improved code readability.

---

# Task 3: Try adding a new model and relationships

### a. Links to relevant commits/issues
> https://github.com/rrdtlsh/modern-software-dev-assignments/pull/3

### b. PR Description
> **Problem & Approach:** Required a One-to-Many relationship between `Note` and `ActionItem`. Updated SQLAlchemy models with `ForeignKey` (`note_id`) and `relationship()` mappings. Updated Pydantic schemas to include `note_id: int | None = None`. 
> **Summary of Testing:** Ran command `pytest backend/tests`. Result: 3 passed. Data relationships worked correctly.
> **Tradeoffs, Limitations, or Follow-ups:** Kept the foreign key as `nullable=True`. The tradeoff here is weaker database strictness, but this limitation was necessary to ensure backward compatibility and prevent existing seed data/tests from breaking.

### c. Graphite Diamond generated code review
> Graphite Diamond generated a clean review ("Graphite found no issues"). The AI correctly identified that the structural changes to the SQLAlchemy models and Pydantic schemas were safe and properly isolated, validating the decision to use a nullable foreign key.

---

# Task 4: Improve tests for pagination and sorting

### a. Links to relevant commits/issues
> https://github.com/rrdtlsh/modern-software-dev-assignments/pull/4

### b. PR Description
> **Problem & Approach:** Added explicit test coverage for pagination (`skip`, `limit`) and sorting (`sort`) query parameters. Appended new test functions in `test_notes.py` and `test_action_items.py`. Seeded dummy data and asserted the length and alphabetical sorting of the JSON responses using Python's `sorted()`.
> **Summary of Testing:** Ran command `pytest backend/tests`. Result: Coverage increased, 7 total tests passed seamlessly.
> **Tradeoffs, Limitations, or Follow-ups:** The tradeoff is that these tests only cover the "happy path" (positive testing). A follow-up is needed to test boundary conditions (e.g., negative limits like `limit=-5` or sorting by non-existent fields).

### c. Graphite Diamond generated code review
> Graphite Diamond approved the PR with "Graphite found no issues." The AI recognized the test additions as structurally sound and compliant with pytest standards, acknowledging that adding isolated tests is a safe operation.

---

# Brief Reflection 

### a. The types of comments you typically made in your manual reviews
> In my manual reviews, my primary focus was on **correctness, test execution, and preventing regressions**. I heavily checked local terminal outputs to ensure `pytest` stayed green. I also checked Python syntax, FastAPI route structures, and ensured that existing endpoints or tests were not accidentally modified or deleted by the AI coding assistant (Cursor).

### b. A comparison of your comments vs. Graphite’s AI-generated comments for each PR
> While my manual review focused on local functionality and syntax execution ("Does the code run without crashing?"), Graphite's AI operated with a much broader, context-aware perspective. In Task 1, I verified the search endpoints worked perfectly in the terminal, but Graphite cross-referenced my PR description metadata with the code diff. Graphite acted as a semantic checker, whereas I acted as an execution checker. 

### c. When the AI reviews were better/worse than yours (cite specific examples)
> **Better:** Graphite was vastly superior at catching "documentation drift." For example, in Task 1, it caught that my PR description exaggerated the changes (claiming full CRUD) and astutely pointed out that DELETE endpoints were completely missing. I missed this because I was too focused on the GET endpoints functioning correctly in the terminal.
> **Worse:** The AI review was somewhat generic for simple structural additions. For example, in Task 4 (adding test functions), Graphite simply stated "no issues." A human Senior Engineer might have suggested deeper edge-case testing, such as testing pagination with negative limits (`limit=-1`), which the AI failed to suggest.

### d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them
> This exercise significantly increased my comfort level with AI code reviews, but it shifted my perspective: AI is a tireless "second pair of eyes," not an ultimate authority. 
> **Heuristics for relying on AI:**
> 1. Always rely on AI to catch structural inconsistencies, naming convention violations, missing type hints, and documentation-to-code mismatches (like the Task 1 PR description).
> 2. Never rely solely on AI to validate deep domain business logic, complex security architectures, or boundary test definitions. Human oversight and a robust automated testing pipeline (CI/CD) remain strictly necessary.