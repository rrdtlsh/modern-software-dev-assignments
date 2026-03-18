# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Raudatul Sholehah** \
SUNet ID: **Not applicable** \
Citations: **Cursor AI Assistant, Graphite Diamond AI Documentation**

This assignment took me about **3** hours to do. 


## App Concept 
The application built for this assignment is called "Student Task Manager". It is a productivity tool designed to help students organize and manage their academic tasks, such as assignments and study plans. The main resource is a "Task", and users can Create, Read, Update, and Delete tasks. Each task contains a title, description, deadline, and a status indicator (pending or completed). A simple, modern UI is used to surface these main flows clearly.


## Version #1 Description
APP DETAILS:
===============
Folder name: bolt-task-app
AI app generation platform: Bolt.new
Tech Stack: React (Frontend) + Node.js (Backend)
Persistence: Supabase (PostgreSQL - Backend as a Service)
Frameworks/Libraries Used: Vite, React, Tailwind CSS, Supabase JS Client
(Optional but recommended) Screenshots of core flows: [You can attach screenshot image_16c6cd.png here if needed]

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
The primary issue was an architectural deviation by the AI. Despite instructing Bolt.new to use a local SQLite database, the AI insisted on using Supabase because it evaluated it as a better fit for the Vite/React ecosystem. I resolved this by manually creating a Supabase project, setting up the `tasks` table using the SQL Editor, and configuring the `.env` file locally so the downloaded code could properly connect to the database.

b. Prompting (e.g. what required additional guidance; what worked poorly/well): 
The initial "zero-shot" comprehensive prompt worked extremely well for generating the full UI and CRUD logic. However, prompting for specific local database technologies (like SQLite inside a browser-based container) worked poorly as Bolt preferred cloud-based BaaS solutions.

c. Approximate time-to-first-run and time-to-feature metrics: 
Time-to-first-run: ~2 minutes (Bolt generated the preview instantly).
Time-to-feature: ~15 minutes (after downloading the ZIP, fixing the .env, and configuring Supabase manually).

## Version #2 Description
APP DETAILS:
===============
Folder name: flask-task-app
AI app generation platform: Cursor AI (Composer)
Tech Stack: Python (Backend) + HTML/CSS (Frontend) - Fulfills Non-JS requirement
Persistence: SQLite (Local database.db)
Frameworks/Libraries Used: Flask, sqlite3, Tailwind CSS (via CDN)
(Optional but recommended) Screenshots of core flows: [You can attach screenshot image_08cd77.png here if needed]

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
After generating the code, I encountered a `jinja2.exceptions.TemplateNotFound: index.html` error. This happened because Flask couldn't locate the `templates` directory depending on where the `python app.py` command was executed. I also faced an issue where the initial UI was plain text. I resolved the first issue by prompting Cursor to use `os.path.abspath` to strictly define the template and static folder paths. I resolved the UI issue by prompting Cursor to inject Tailwind CSS via CDN.

b. Prompting (e.g. what required additional guidance; what worked poorly/well): 
Prompting Cursor to generate the Python backend logic worked flawlessly on the first try. However, it required additional critical prompting to fix the pathing issue to make it environment-agnostic. Asking the AI to "add Tailwind classes to the raw HTML to make it look clean" worked exceptionally well.

c. Approximate time-to-first-run and time-to-feature metrics: 
Time-to-first-run: ~5 minutes.
Time-to-feature: ~15 minutes (after debugging the TemplateNotFound error and iterating on the CSS styling).

## Version #3 Description
APP DETAILS:
===============
Folder name: nextjs-task-app
AI app generation platform: Cursor AI (Composer)
Tech Stack: Next.js 16 (App Router) + Node.js
Persistence: SQLite (Local tasks.db)
Frameworks/Libraries Used: Next.js, React, Tailwind CSS, sqlite, sqlite3
(Optional but recommended) Screenshots of core flows: [You can attach screenshot image_061738.png here if needed]

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
Because I initialized the project with the latest Next.js 16 version, I encountered a sync dynamic API error: `params is a Promise and must be unwrapped with await or React.use()`. The AI generated older Next.js 14 code syntax for the `PUT` and `DELETE` route handlers (`/api/tasks/[id]`). I resolved this by prompting Cursor specifically to await the params Promise before reading `params.id`. 

b. Prompting (e.g. what required additional guidance; what worked poorly/well): 
The "God-tier" prompt creating the App Router structure and a dark-mode UI worked wonderfully. However, the initial generation lacked a smooth way to toggle a task's status. I provided additional guidance prompting the AI to make the "Status Badge" directly clickable to trigger a `PUT` request, which resulted in a highly interactive and modern UX.

c. Approximate time-to-first-run and time-to-feature metrics: 
Time-to-first-run: ~5 minutes.
Time-to-feature: ~20 minutes (including fixing the Next.js 16 Promise error and iterating on the interactive status toggle feature).