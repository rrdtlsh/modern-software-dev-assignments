import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function PUT(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const resolvedParams = await params;
    const id = Number(resolvedParams.id);
    if (Number.isNaN(id)) {
      return NextResponse.json({ error: "Invalid id" }, { status: 400 });
    }

    const body = await request.json();
    const title = (body.title ?? "").trim();
    const description = (body.description ?? "").trim();
    const deadline = (body.deadline ?? "").trim();
    const status = (body.status ?? "pending").trim() || "pending";

    if (!title) {
      return NextResponse.json({ error: "Title is required" }, { status: 400 });
    }

    const db = await getDb();

    const existing = await db.get("SELECT * FROM tasks WHERE id = ?", id);
    if (!existing) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 });
    }

    await db.run(
      "UPDATE tasks SET title = ?, description = ?, deadline = ?, status = ? WHERE id = ?",
      title,
      description || null,
      deadline || null,
      status || "pending",
      id
    );

    const updated = await db.get("SELECT * FROM tasks WHERE id = ?", id);
    return NextResponse.json(updated);
  } catch (error) {
    console.error("Error updating task", error);
    return NextResponse.json({ error: "Failed to update task" }, { status: 500 });
  }
}

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const resolvedParams = await params;
    const id = Number(resolvedParams.id);
    if (Number.isNaN(id)) {
      return NextResponse.json({ error: "Invalid id" }, { status: 400 });
    }

    const db = await getDb();

    const existing = await db.get("SELECT * FROM tasks WHERE id = ?", id);
    if (!existing) {
      return NextResponse.json({ error: "Task not found" }, { status: 404 });
    }

    await db.run("DELETE FROM tasks WHERE id = ?", id);

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Error deleting task", error);
    return NextResponse.json({ error: "Failed to delete task" }, { status: 500 });
  }
}

