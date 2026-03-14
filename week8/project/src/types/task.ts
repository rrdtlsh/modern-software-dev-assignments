export interface Task {
  id: string;
  title: string;
  description: string | null;
  deadline: string | null;
  status: 'pending' | 'completed';
  created_at: string;
}

export type NewTask = Omit<Task, 'id' | 'created_at'>;
