import { Task } from '../types/task';
import { CreditCard as Edit, Trash2, Calendar, CheckCircle, Circle } from 'lucide-react';

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  onToggleStatus: (task: Task) => void;
}

export function TaskList({ tasks, onEdit, onDelete, onToggleStatus }: TaskListProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'No deadline';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No tasks yet. Create your first task to get started!
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2">
                <button
                  onClick={() => onToggleStatus(task)}
                  className="flex-shrink-0 text-gray-400 hover:text-blue-600 transition-colors"
                  aria-label={task.status === 'completed' ? 'Mark as pending' : 'Mark as completed'}
                >
                  {task.status === 'completed' ? (
                    <CheckCircle className="w-6 h-6 text-green-600" />
                  ) : (
                    <Circle className="w-6 h-6" />
                  )}
                </button>
                <h3 className={`text-lg font-semibold ${task.status === 'completed' ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {task.title}
                </h3>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  task.status === 'completed'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-yellow-100 text-yellow-700'
                }`}>
                  {task.status}
                </span>
              </div>
              {task.description && (
                <p className="text-gray-600 mb-2 ml-9">{task.description}</p>
              )}
              <div className="flex items-center gap-2 text-sm text-gray-500 ml-9">
                <Calendar className="w-4 h-4" />
                <span>{formatDate(task.deadline)}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <button
                onClick={() => onEdit(task)}
                className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                aria-label="Edit task"
              >
                <Edit className="w-5 h-5" />
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                aria-label="Delete task"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
