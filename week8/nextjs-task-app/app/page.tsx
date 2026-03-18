"use client";

import { useEffect, useState } from "react";

type TaskStatus = "pending" | "completed";

type Task = {
  id: number;
  title: string;
  description: string | null;
  deadline: string | null;
  status: TaskStatus | string;
};

type TaskFormState = {
  title: string;
  description: string;
  deadline: string;
  status: TaskStatus;
};

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [form, setForm] = useState<TaskFormState>({
    title: "",
    description: "",
    deadline: "",
    status: "pending",
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function fetchTasks() {
    try {
      const res = await fetch("/api/tasks");
      if (!res.ok) {
        throw new Error("Failed to fetch tasks");
      }
      const data = (await res.json()) as Task[];
      setTasks(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load tasks.");
    }
  }

  useEffect(() => {
    fetchTasks();
  }, []);

  function resetForm() {
    setForm({ title: "", description: "", deadline: "", status: "pending" });
    setEditingId(null);
    setError(null);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      title: form.title.trim(),
      description: form.description.trim(),
      deadline: form.deadline.trim(),
      status: form.status,
    };

    if (!payload.title) {
      setError("Title is required.");
      setLoading(false);
      return;
    }

    try {
      const url = editingId ? `/api/tasks/${editingId}` : "/api/tasks";
      const method = editingId ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        const message = (data && data.error) || "Failed to save task.";
        throw new Error(message);
      }

      await fetchTasks();
      resetForm();
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleEdit(task: Task) {
    setEditingId(task.id);
    setForm({
      title: task.title ?? "",
      description: task.description ?? "",
      deadline: task.deadline ?? "",
      status: (task.status === "completed" ? "completed" : "pending") as TaskStatus,
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function handleDelete(id: number) {
    const confirmed = window.confirm("Are you sure you want to delete this task?");
    if (!confirmed) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/tasks/${id}`, { method: "DELETE" });
      const data = await res.json();
      if (!res.ok) {
        const message = (data && data.error) || "Failed to delete task.";
        throw new Error(message);
      }

      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function toggleStatus(task: Task) {
    const nextStatus: TaskStatus = task.status === "completed" ? "pending" : "completed";

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/api/tasks/${task.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: task.title,
          description: task.description,
          deadline: task.deadline,
          status: nextStatus,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        const message = (data && data.error) || "Failed to update status.";
        throw new Error(message);
      }

      setTasks((prev) =>
        prev.map((t) => (t.id === task.id ? { ...t, status: nextStatus } : t))
      );
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-4 py-8 md:px-8 md:py-10">
        <header className="flex flex-col justify-between gap-4 border-b border-slate-800 pb-6 md:flex-row md:items-end">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-400">
              Student Dashboard
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-50 md:text-4xl">
              Student Task Manager
            </h1>
            <p className="mt-2 max-w-xl text-sm text-slate-400">
              Keep track of your assignments, deadlines, and progress in one focused
              dashboard.
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-xl bg-slate-900/80 px-4 py-2 text-xs text-slate-400 ring-1 ring-slate-800">
            <span className="inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            Next.js 16 · SQLite · Tailwind CSS
          </div>
        </header>

        <main className="grid gap-6 md:grid-cols-[minmax(0,1.1fr)_minmax(0,1.4fr)]">
          <section className="space-y-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 shadow-lg shadow-slate-950/40">
              <div className="mb-4 flex items-center justify-between gap-2">
                <div>
                  <h2 className="text-sm font-semibold text-slate-100">
                    {editingId ? "Edit Task" : "Add New Task"}
                  </h2>
                  <p className="text-xs text-slate-400">
                    {editingId
                      ? "Update the fields and save your changes."
                      : "Create a new task with a clear title and deadline."}
                  </p>
                </div>
                {editingId && (
                  <button
                    type="button"
                    onClick={resetForm}
                    className="text-xs font-medium text-slate-400 hover:text-slate-200"
                  >
                    Cancel edit
                  </button>
                )}
              </div>

              {error && (
                <div className="mb-3 rounded-lg border border-red-500/40 bg-red-500/10 px-3 py-2 text-xs text-red-100">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-1">
                  <label className="block text-xs font-medium text-slate-200">
                    Title<span className="text-red-400">*</span>
                  </label>
                  <input
                    type="text"
                    value={form.title}
                    onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))}
                    placeholder="e.g. Finish algorithms assignment"
                    className="w-full rounded-lg border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm text-slate-50 outline-none ring-1 ring-slate-900 focus:border-sky-500 focus:ring-sky-500"
                  />
                </div>

                <div className="space-y-1">
                  <label className="block text-xs font-medium text-slate-200">
                    Description
                  </label>
                  <textarea
                    rows={3}
                    value={form.description}
                    onChange={(e) =>
                      setForm((prev) => ({ ...prev, description: e.target.value }))
                    }
                    placeholder="Optional details, links, or notes…"
                    className="w-full resize-none rounded-lg border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm text-slate-50 outline-none ring-1 ring-slate-900 focus:border-sky-500 focus:ring-sky-500"
                  />
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
                  <div className="flex-1 space-y-1">
                    <label className="block text-xs font-medium text-slate-200">
                      Deadline
                    </label>
                    <input
                      type="date"
                      value={form.deadline}
                      onChange={(e) =>
                        setForm((prev) => ({ ...prev, deadline: e.target.value }))
                      }
                      className="w-full rounded-lg border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm text-slate-50 outline-none ring-1 ring-slate-900 focus:border-sky-500 focus:ring-sky-500"
                    />
                  </div>

                  {editingId && (
                    <div className="space-y-1">
                      <label className="block text-xs font-medium text-slate-200">
                        Status
                      </label>
                      <select
                        value={form.status}
                        onChange={(e) =>
                          setForm((prev) => ({
                            ...prev,
                            status: e.target.value as TaskStatus,
                          }))
                        }
                        className="w-full rounded-lg border border-slate-800 bg-slate-950/60 px-3 py-2 text-xs text-slate-50 outline-none ring-1 ring-slate-900 focus:border-sky-500 focus:ring-sky-500"
                      >
                        <option value="pending">Pending</option>
                        <option value="completed">Completed</option>
                      </select>
                    </div>
                  )}

                  <button
                    type="submit"
                    disabled={loading}
                    className="mt-1 inline-flex items-center justify-center rounded-lg bg-sky-500 px-4 py-2 text-sm font-medium text-slate-950 shadow-sm shadow-sky-500/40 transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-60 sm:mt-5"
                  >
                    {editingId ? "Save Changes" : "Add Task"}
                  </button>
                </div>
              </form>
            </div>

            <div className="rounded-2xl border border-slate-900 bg-slate-950/80 p-4 text-xs text-slate-400">
              <p className="font-medium text-slate-200">Tips for students</p>
              <ul className="mt-2 list-disc space-y-1 pl-5">
                <li>Use clear, action-oriented titles for each task.</li>
                <li>Set realistic deadlines and keep them up to date.</li>
                <li>Mark tasks as completed as soon as you finish them.</li>
              </ul>
            </div>
          </section>

          <section className="space-y-3">
            <div className="flex items-center justify-between gap-2">
              <h2 className="text-sm font-semibold text-slate-100">Your Tasks</h2>
              <p className="text-xs text-slate-400">
                {tasks.length === 0
                  ? "No tasks yet – start by adding one."
                  : `${tasks.length} task${tasks.length > 1 ? "s" : ""} in your list`}
              </p>
            </div>

            <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 shadow-lg shadow-slate-950/40">
              <div className="max-h-[420px] overflow-y-auto">
                <table className="min-w-full divide-y divide-slate-800 text-sm">
                  <thead className="bg-slate-900/80 text-xs uppercase tracking-wide text-slate-400">
                    <tr>
                      <th className="px-4 py-3 text-left">Title</th>
                      <th className="px-4 py-3 text-left">Deadline</th>
                      <th className="px-4 py-3 text-left">Status</th>
                      <th className="px-4 py-3 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800 bg-slate-950/40">
                    {tasks.length === 0 ? (
                      <tr>
                        <td
                          colSpan={4}
                          className="px-4 py-8 text-center text-xs text-slate-500"
                        >
                          No tasks yet. Add your first task using the form on the left.
                        </td>
                      </tr>
                    ) : (
                      tasks.map((task) => {
                        const isCompleted = task.status === "completed";
                        return (
                          <tr
                            key={task.id}
                            className="hover:bg-slate-900/70 transition-colors"
                          >
                            <td className="px-4 py-3 align-top">
                              <div className="flex flex-col gap-1">
                                <p
                                  className={`text-sm font-medium ${
                                    isCompleted
                                      ? "text-slate-400 line-through"
                                      : "text-slate-50"
                                  }`}
                                >
                                  {task.title}
                                </p>
                                {task.description && (
                                  <p className="text-xs text-slate-400">
                                    {task.description}
                                  </p>
                                )}
                              </div>
                            </td>
                            <td className="px-4 py-3 align-top text-xs text-slate-300">
                              {task.deadline ? task.deadline : <span className="text-slate-500">—</span>}
                            </td>
                            <td className="px-4 py-3 align-top">
                              <button
                                type="button"
                                onClick={() => toggleStatus(task)}
                                className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ring-1 ring-inset ${
                                  isCompleted
                                    ? "bg-emerald-500/10 text-emerald-300 ring-emerald-500/40"
                                    : "bg-amber-500/10 text-amber-200 ring-amber-500/40"
                                }`}
                              >
                                {isCompleted ? "Completed" : "Pending"}
                              </button>
                            </td>
                            <td className="px-4 py-3 align-top">
                              <div className="flex justify-end gap-2 text-xs">
                                <button
                                  type="button"
                                  onClick={() => handleEdit(task)}
                                  className="rounded-lg border border-slate-700 px-2.5 py-1 font-medium text-slate-100 hover:bg-slate-800"
                                >
                                  Edit
                                </button>
                                <button
                                  type="button"
                                  onClick={() => handleDelete(task.id)}
                                  className="rounded-lg bg-red-500/90 px-2.5 py-1 font-medium text-slate-50 hover:bg-red-400"
                                >
                                  Delete
                                </button>
                              </div>
                            </td>
                          </tr>
                        );
                      })
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </main>

        <footer className="mt-auto border-t border-slate-900 pt-4 text-xs text-slate-500">
          <p>
            Student Task Manager · Built with Next.js App Router, SQLite, and Tailwind CSS.
          </p>
        </footer>
      </div>
    </div>
  );
}
