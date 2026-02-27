# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Raudatul Sholehah** \
SUNet ID: **Not applicable** \
Citations: **N/A**

This assignment took me about **six (6)** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
Analyze the existing extract_action_items() function in week2/app/services/extract.py.

Scaffold a new function extract_action_items_llm(text: str) -> List[str]
that uses Ollama to extract action items using an LLM.

Requirements:
- Use a small Ollama model
- Force structured output as a JSON array of strings
- Include basic error handling and fallback to heuristic extraction
- Do not remove the existing extract_action_items() function

Generated Code Snippets:
Modified file:
- app/services/extract.py

Changes:
- Added extract_action_items_llm() function (approx. lines 55–95)
- Introduced OLLAMA_EXTRACT_MODEL environment variable for model  configurability
- Used Pydantic schema to enforce structured JSON output
- Implemented graceful fallback to extract_action_items() on error

Notes:
The LLM-based extraction complements the existing heuristic approach by handling
free-form and less structured inputs. Structured output ensures reliability, while
fallback logic guarantees system robustness if the LLM fails or is unavailable.

### Exercise 2: Add Unit Tests
Prompt:
Extend week2/tests/test_extract.py with unit tests for extract_action_items_llm().

Requirements:
- Use pytest
- Do NOT remove existing tests for extract_action_items()
- Mock the Ollama chat() function so tests do not require a running LLM
- Add tests for:
  1. Successful extraction when the LLM returns valid JSON
  2. Empty input (should return an empty list)
  3. Invalid or malformed JSON returned by the LLM (should gracefully fall back)
- Keep tests minimal, readable, and well-structured

Generated Code Snippets:
File: week2/tests/test_extract.py

Lines 27-57:
Added 3 new test functions using unittest.mock.patch:
1. test_extract_action_items_llm_success: Mocks a valid JSON response from Ollama and asserts correct parsing.
2. test_extract_action_items_llm_empty_input: Ensures empty input returns empty list without calling the LLM.
3. test_extract_action_items_llm_malformed_json_fallback: Mocks a malformed response and ensures the function falls back to heuristic extraction.

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
Refactor the backend code in week2/app/services/extract.py to improve clarity
and maintainability without changing existing behavior.

Refactor goals:
- Define clear and reusable API contracts/schemas for LLM responses
- Move Pydantic models out of function scope
- Improve error handling (avoid overly broad exception handling where possible)
- Clean up unused imports
- Improve configuration clarity for the Ollama model
- Add concise comments explaining responsibilities of key components

Constraints:
- Do NOT remove existing functionality
- Do NOT change function signatures
- Keep both heuristic and LLM-based extractors
- Ensure all existing tests still pass

Generated/Modified Code Snippets:
File: week2/app/services/extract.py

1. Configuration cleanup and clarity
   - Added a clear configuration section for the Ollama model.
   - Updated the default model to `llama3.1:8b` to match the locally available model.
   - Lines ~15–20

   OLLAMA_EXTRACT_MODEL = os.getenv("OLLAMA_EXTRACT_MODEL", "llama3.1:8b")

2. Defined reusable API contract for LLM responses
   - Introduced a top-level Pydantic model `ActionItemsOutput`
     to represent the structured JSON response expected from the LLM.
   - This model is reused for validation and schema generation.
   - Lines ~27–36

   class ActionItemsOutput(BaseModel):
       items: list[str]

3. Refactored LLM extraction to use structured output and explicit validation
   - Updated `extract_action_items_llm` to request structured output
     using `model_json_schema()`.
   - Parsed and validated the LLM response using `model_validate_json`.
   - Lines ~88–123

4. Improved error handling
   - Replaced a single broad exception handler with more specific exceptions:
     - `ValidationError` for malformed or schema-invalid LLM responses
     - `OSError` for Ollama connectivity issues
     - A final catch-all fallback for unexpected runtime errors
   - All error cases fall back to heuristic extraction to preserve behavior.
   - Lines ~110–123

5. Code organization and readability improvements
   - Grouped logic into clear sections:
     - Configuration
     - LLM response schemas
     - Heuristic extraction helpers
     - LLM-based extraction
   - Added concise docstrings and comments describing responsibilities.
   - Removed unused imports and kept only required dependencies.
   - Lines throughout the file

No function signatures were changed, both heuristic and LLM-based extractors
remain intact, and all existing tests continue to pass.


### Exercise 4: Use Agentic Mode to Automate a Small Task
Implement Exercise 4 using Agentic Mode.

Backend:
Implement Exercise 4(backend only):

1. In week2/app/routers/action_items.py:
   - Add a new POST endpoint /action-items/extract-llm
   - Use extract_action_items_llm from week2.app.services.extract
   - Behavior should match the existing extraction endpoint
2. In week2/app/routers/notes.py:
   - Add a new GET /notes endpoint
   - Return all notes using db.list_notes()

Constraints:
- Do not break existing endpoints
- Follow existing FastAPI patterns


Frontend:
Implement Exercise 4 (frontend only):

1. In frontend/index.html:
   - Add a button "Extract with LLM" next to the existing Extract button
   - Add a button "List All Notes"
2. In frontend JavaScript:
   - Wire "Extract with LLM" to POST /action-items/extract-llm
   - Wire "List All Notes" to GET /notes
   - Display returned notes dynamically below the main container

Ensure UI style matches existing design.

Generated Code Snippets:
Modified Files:
1. week2/app/routers/action_items.py
- Added import: extract_action_items_llm
- Added POST endpoint: /action-items/extract-llm
- Lines modified/added:
  - Import section (top of file)
  - New function extract_llm(...) below existing extract endpoint
2. week2/app/routers/notes.py
- Added GET endpoint: /notes
- Uses db.list_notes() to return all notes
- Lines modified/added:
  - New function list_notes() at router level
3. frontend/index.html
- Added button "Extract with LLM" next to existing Extract button
- Added button "List All Notes"
- Added notes display section below main container
- Added JavaScript handlers:
  - POST /action-items/extract-llm
  - GET /notes
- Lines modified/added:
  - HTML button section
  - Notes section markup
  - JavaScript fetch handlers and DOM rendering logic

### Exercise 5: Generate a README from the Codebase
Prompt: 
Analyze the entire codebase and generate a well-structured README.md.

The README must include:
- Project overview
- Tech stack
- Setup and run instructions
- API endpoints and their functionality
- Frontend usage
- Instructions for running tests (if available)

Assume this is a FastAPI backend with a minimal HTML frontend.


Generated Code Snippets:
Modified file:
- README.md

Summary of generated content:
- Project overview explaining the Action Item Extractor application
- Description of heuristic-based and LLM-based extraction
- Tech stack table (FastAPI, SQLite, Ollama, HTML/JS)
- Setup and run instructions using Poetry and Uvicorn
- API endpoint documentation for /action-items and /notes
- Frontend usage instructions for Extract, Extract with LLM, and List All Notes
- Instructions for running the pytest test suite

Note:
No backend or frontend source files were modified in this exercise.
The only generated artifact is documentation (README.md).

## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 

Tooling Note:
Cursor Student Pro was not available for my university email domain.
All features were implemented using Cursor Free + local Ollama models.