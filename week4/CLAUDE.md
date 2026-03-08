# Claude Code Configuration

This project demonstrates AI-assisted developer workflow automation using Claude Code.

Instead of performing repetitive development tasks manually, developers can use AI-powered commands that act as specialized agents.

## Available AI Commands

### 1. Generate Tests

Command: `generate-tests`

Purpose:
Automatically generate pytest tests for FastAPI endpoints that do not yet have test coverage.

Benefits:
- Improves test coverage
- Reduces manual work for developers

### 2. Improve Documentation

Command: `improve-docs`

Purpose:
Analyze backend code and improve documentation quality.

Benefits:
- Improves readability
- Ensures consistent documentation

## Project Structure

backend/
    app/
    tests/

frontend/

.claude/
    commands/

## Workflow

1. Developer writes or modifies code.
2. AI agent generates tests automatically.
3. AI agent improves documentation.
4. Developer reviews and commits improvements.

This approach demonstrates the concept of AI-assisted development workflows.