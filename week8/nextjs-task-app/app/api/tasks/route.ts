import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  try {
    const db = await getDb();
    const tasks = await db.all("SELECT * FROM tasks ORDER BY id DESC");
    return NextResponse.json(tasks);
  } catch (error) {
    console.error("Error fetching tasks", error);
    return NextResponse.json({ error: "Failed to fetch tasks" }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const title = (body.title ?? "").trim();
    const description = (body.description ?? "").trim();
    const deadline = (body.deadline ?? "").trim();

    if (!title) {
      return NextResponse.json({ error: "Title is required" }, { status: 400 });
    }

    const db = await getDb();
    const result = await db.run(
      "INSERT INTO tasks (title, description, deadline, status) VALUES (?, ?, ?, ?)",
      title,
      description || null,
      deadline || null,
      "pending"
    );

    const task = await db.get("SELECT * FROM tasks WHERE id = ?", result.lastID);

    return NextResponse.json(task, { status: 201 });
  } catch (error) {
    console.error("Error creating task", error);
    return NextResponse.json({ error: "Failed to create task" }, { status: 500 });
  }
}

