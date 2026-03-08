# Generate Backend Tests

You are an AI development assistant responsible for improving test coverage.

Your task is to analyze the FastAPI backend and generate pytest tests for endpoints that do not yet have test coverage.

Steps:
1. Identify API endpoints defined in the FastAPI router.
2. Compare them with existing tests in `backend/tests`.
3. Generate new pytest test cases for missing endpoints.
4. Follow the existing test style used in the repository.
5. Use FastAPI TestClient for API testing.

Constraints:
- Do not modify existing passing tests.
- Only add new test functions.

Output:
Provide the generated pytest test functions.