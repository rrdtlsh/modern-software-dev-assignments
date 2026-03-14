/*
  # Create tasks table for Student Task Manager

  1. New Tables
    - `tasks`
      - `id` (uuid, primary key) - Unique identifier for each task
      - `title` (text, required) - Task title
      - `description` (text) - Task description
      - `deadline` (timestamptz) - Task deadline
      - `status` (text, default 'pending') - Task status (pending or completed)
      - `created_at` (timestamptz, default now()) - Timestamp when task was created

  2. Security
    - Enable RLS on `tasks` table
    - Add policy for users to read all tasks (public access for this demo)
    - Add policy for users to insert tasks
    - Add policy for users to update tasks
    - Add policy for users to delete tasks
*/

CREATE TABLE IF NOT EXISTS tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text DEFAULT '',
  deadline timestamptz,
  status text DEFAULT 'pending',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view tasks"
  ON tasks FOR SELECT
  USING (true);

CREATE POLICY "Anyone can insert tasks"
  ON tasks FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Anyone can update tasks"
  ON tasks FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete tasks"
  ON tasks FOR DELETE
  USING (true);