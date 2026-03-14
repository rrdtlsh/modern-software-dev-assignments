# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Raudatul Sholehah** \
SUNet ID: **Not applicable** \
Citations: **Semgrep documentation, ChatGPT AI coding assistant**

This assignment took me about **3–4 hours** to do. 


## Brief findings overview 
> Static analysis was performed using the Semgrep CLI (`semgrep scan --config auto week6`) on the application. The initial scan reported 6 blocking security issues categorized under Static Application Security Testing (SAST). The detected vulnerabilities included SQL Injection in the backend, Cross-Site Scripting (XSS) in the frontend, and an insecure CORS configuration.
>
> **False Positives/Noisy Rules Ignored:** Out of the 6 findings, I chose to ignore 3 rules (`eval()` detection, `subprocess` with `shell=True`, and dynamic `urllib` usage). These were flagged inside `week6/backend/app/routers/notes.py` under the `/debug/` endpoints. I ignored them because these are intentionally unsafe dummy routes meant for debugging/testing, not part of the actual user-facing application logic. I focused my mitigation efforts on the 3 critical vulnerabilities affecting the core features.

## Fix #1
a. File and line(s)
> `week6/backend/app/routers/notes.py` (Lines 71-79) - unsafe search endpoint using raw SQL query.

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.audit.avoid-sqlalchemy-text` (SQL Injection risk)

c. Brief risk description
> The query used string interpolation to insert user input directly into a SQL statement. This can allow attackers to inject malicious SQL commands that modify, drop, or expose database data.

d. Your change (short code diff or explanation, AI coding tool usage)
> **AI coding tool used:** ChatGPT.
> The raw SQL string interpolation was replaced with a parameterized query using SQLAlchemy parameter binding.
> 
> **Before:**
> ```python
> sql = text(f"""
> SELECT id, title, content, created_at, updated_at
> FROM notes
> WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'
> ORDER BY created_at DESC LIMIT 50
> """)
> rows = db.execute(sql).all()
> ```
> 
> **After:**
> ```python
> sql = text("""
> SELECT id, title, content, created_at, updated_at
> FROM notes
> WHERE title LIKE :q OR content LIKE :q
> ORDER BY created_at DESC LIMIT 50
> """)
> rows = db.execute(sql, {"q": f"%{q}%"}).all()
> ```

e. Why this mitigates the issue
> Parameterized queries prevent user input from being interpreted as part of the executable SQL command. Instead, the database engine treats the input strictly as literal string data, effectively mitigating SQL Injection attacks.

## Fix #2
a. File and line(s)
> `week6/frontend/app.js` (Line 14) - note rendering logic in the notes list.

b. Rule/category Semgrep flagged
> `javascript.browser.security.insecure-document-method.insecure-document-method` (potential Cross-Site Scripting / XSS)

c. Brief risk description
> The application used `.innerHTML` to render note content directly from user input. If malicious HTML or JavaScript (e.g., `<script>`) is stored in a note's title, it would execute in the browser of any user viewing the notes.

d. Your change (short code diff or explanation, AI coding tool usage)
> **AI coding tool used:** ChatGPT.
> The unsafe `.innerHTML` usage was replaced with safe DOM manipulation using `textContent` and `createTextNode`.
> 
> **Before:**
> ```javascript
> li.innerHTML = `<strong>${n.title}</strong>: ${n.content}`;
> ```
> 
> **After:**
> ```javascript
> const strong = document.createElement("strong");
> strong.textContent = n.title;
> 
> li.appendChild(strong);
> li.appendChild(document.createTextNode(": " + n.content));
> ```

e. Why this mitigates the issue
> Using `textContent` ensures that user input is treated purely as raw text rather than executable HTML nodes. The browser automatically escapes any injected scripts, completely protecting the application from DOM-based XSS attacks.

## Fix #3
a. File and line(s)
> `week6/backend/app/main.py` (Line 24) - CORS middleware configuration.

b. Rule/category Semgrep flagged
> `python.fastapi.security.wildcard-cors.wildcard-cors` (Security Misconfiguration)

c. Brief risk description
> Allowing all origins using the wildcard `"*"` in the CORS configuration exposes the API to cross-origin requests from untrusted or malicious domains, potentially leading to unauthorized data access.

d. Your change (short code diff or explanation, AI coding tool usage)
> **AI coding tool used:** ChatGPT.
> The wildcard origin was replaced with a restricted list of trusted local development origins.
> 
> **Before:**
> ```python
> allow_origins=["*"],
> ```
> 
> **After:**
> ```python
> allow_origins=[
>     "http://localhost:3000",
>     "[http://127.0.0.1:3000](http://127.0.0.1:3000)"
> ],
> ```

e. Why this mitigates the issue
> Restricting CORS to specific, trusted local origins ensures that modern web browsers will block unauthorized cross-origin requests coming from unapproved frontend applications, significantly reducing the API's attack surface.