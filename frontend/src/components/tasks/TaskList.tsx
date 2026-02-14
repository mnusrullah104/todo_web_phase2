'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Task } from '@/lib/types';
import { taskApi } from '@/lib/api';
import { useTaskMetadata, Priority } from '@/hooks/useTaskMetadata';
import { useToast } from '@/contexts/ToastContext';
import Badge from '@/components/ui/Badge';
import EmptyState from '@/components/ui/EmptyState';
import ConfirmModal from '@/components/ui/ConfirmModal';
import KanbanBoard from './KanbanBoard';

interface TaskListProps {
  userId: string;
}

export default function TaskList({ userId }: TaskListProps) {
  const toast = useToast();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState<'table' | 'list' | 'kanban'>('table');
  const [priorityFilter, setPriorityFilter] = useState<'all' | Priority>('all');
  const { taskPriorities, setPriority } = useTaskMetadata();

  // Delete confirmation modal
  const [deleteModal, setDeleteModal] = useState<{
    isOpen: boolean;
    taskId: string | null;
    taskTitle: string;
  }>({
    isOpen: false,
    taskId: null,
    taskTitle: ''
  });

  useEffect(() => {
    loadTasks();
  }, [userId]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await taskApi.getTasks(userId);
      setTasks(Array.isArray(data) ? data : []);
    } catch (err: any) {
      toast.error(err.message || 'Failed to load tasks');
      setTasks([]);
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskToggle = async (taskId: string, completed: boolean) => {
    try {
      setActionLoading(taskId);
      await taskApi.toggleTaskCompletion(userId, taskId, completed);

      // Optimistic update
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed, updated_at: new Date() } : task
      ));

      toast.success(completed ? 'Task marked as complete!' : 'Task marked as incomplete');
    } catch (err: any) {
      toast.error(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
    } finally {
      setActionLoading(null);
    }
  };

  const openDeleteModal = (taskId: string, taskTitle: string) => {
    setDeleteModal({
      isOpen: true,
      taskId,
      taskTitle
    });
  };

  const closeDeleteModal = () => {
    setDeleteModal({
      isOpen: false,
      taskId: null,
      taskTitle: ''
    });
  };

  const handleTaskDelete = async () => {
    if (!deleteModal.taskId) return;

    try {
      setActionLoading('delete');
      await taskApi.deleteTask(userId, deleteModal.taskId);
      setTasks(tasks.filter(task => task.id !== deleteModal.taskId));
      toast.success('Task deleted successfully!');
      closeDeleteModal();
    } catch (err: any) {
      toast.error(err.message || 'Failed to delete task');
      console.error('Error deleting task:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Statistics - with safety checks
  const totalTasks = tasks?.length || 0;
  const completedTasks = tasks?.filter(t => t.completed).length || 0;
  const activeTasks = totalTasks - completedTasks;

  // Filtered and searched tasks
  const filteredTasks = tasks?.filter(task => {
    const matchesFilter =
      filter === 'all' ? true :
      filter === 'active' ? !task.completed :
      task.completed;

    const matchesSearch =
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (task.description?.toLowerCase().includes(searchQuery.toLowerCase()) ?? false);

    const taskPriority = taskPriorities[task.id] || 'medium';
    const matchesPriority = priorityFilter === 'all' || taskPriority === priorityFilter;

    return matchesFilter && matchesSearch && matchesPriority;
  }) || [];

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 border-4 border-blue-200 dark:border-blue-900 border-t-blue-600 dark:border-t-blue-500 rounded-full animate-spin"></div>
          <p className="text-gray-600 dark:text-gray-400 font-medium">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Tasks</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            {totalTasks} total • {activeTasks} active • {completedTasks} completed
          </p>
        </div>
        <Link
          href="/tasks/new"
          className="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-sm hover:shadow-md transition-all font-medium"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          New Task
        </Link>
      </div>

      {/* Filters and Search */}
      <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search tasks..."
              className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm text-gray-900 dark:text-white placeholder-gray-500"
            />
          </div>

          {/* Filter Tabs */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                filter === 'all'
                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              All ({totalTasks})
            </button>
            <button
              onClick={() => setFilter('active')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                filter === 'active'
                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              Active ({activeTasks})
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                filter === 'completed'
                  ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              Completed ({completedTasks})
            </button>
          </div>

          {/* Priority Filter */}
          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value as 'all' | Priority)}
            className="px-4 py-2 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Priorities</option>
            <option value="high">High Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="low">Low Priority</option>
          </select>

          {/* View Toggle */}
          <div className="flex items-center space-x-2 border border-gray-300 dark:border-gray-700 rounded-lg p-1">
            <button
              onClick={() => setViewMode('table')}
              className={`p-2 rounded transition-colors ${
                viewMode === 'table'
                  ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
              title="Table view"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded transition-colors ${
                viewMode === 'list'
                  ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
              title="List view"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('kanban')}
              className={`p-2 rounded transition-colors ${
                viewMode === 'kanban'
                  ? 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
              title="Kanban view"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Task Table/List/Kanban */}
      {filteredTasks.length === 0 ? (
        <EmptyState
          icon={
            <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          }
          title={searchQuery ? 'No tasks found' : 'No tasks yet'}
          description={searchQuery ? 'Try adjusting your search or filters' : 'Create your first task to get started'}
          action={!searchQuery ? (
            <Link
              href="/tasks/new"
              className="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-sm hover:shadow-md transition-all font-medium"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Create Task
            </Link>
          ) : undefined}
        />
      ) : viewMode === 'kanban' ? (
        <KanbanBoard
          tasks={filteredTasks}
          onTaskUpdate={handleTaskToggle}
          onTaskDelete={handleTaskDelete}
          openDeleteModal={openDeleteModal}
          taskPriorities={taskPriorities}
        />
      ) : viewMode === 'table' ? (
        <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider w-12">
                    <input type="checkbox" className="rounded border-gray-300 dark:border-gray-600" disabled />
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Task
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Priority
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {filteredTasks.map((task) => (
                  <tr key={task.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                    <td className="px-6 py-4">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={(e) => handleTaskToggle(task.id, e.target.checked)}
                        className="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
                      />
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <Link
                          href={`/tasks/${task.id}`}
                          className={`text-sm font-medium hover:text-blue-600 dark:hover:text-blue-400 transition-colors ${
                            task.completed
                              ? 'text-gray-500 dark:text-gray-600 line-through'
                              : 'text-gray-900 dark:text-white'
                          }`}
                        >
                          {task.title}
                        </Link>
                        {task.description && (
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-1">
                            {task.description}
                          </p>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        task.completed
                          ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
                          : 'bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-400'
                      }`}>
                        {task.completed ? 'Completed' : 'In Progress'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <select
                        value={taskPriorities[task.id] || 'medium'}
                        onChange={(e) => setPriority(task.id, e.target.value as Priority)}
                        className="text-xs font-medium rounded-full px-2.5 py-1 border-0 focus:ring-2 focus:ring-blue-500 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white cursor-pointer"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <option value="low">🟢 Low</option>
                        <option value="medium">🟡 Medium</option>
                        <option value="high">🔴 High</option>
                      </select>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <Link
                          href={`/tasks/${task.id}`}
                          className="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                          title="Edit"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </Link>
                        <button
                          onClick={() => openDeleteModal(task.id, task.title)}
                          disabled={actionLoading !== null}
                          className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors disabled:opacity-50"
                          title="Delete"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredTasks.map((task) => (
            <div
              key={task.id}
              className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start space-x-4">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={(e) => handleTaskToggle(task.id, e.target.checked)}
                  className="mt-1 rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
                />
                <div className="flex-1 min-w-0">
                  <Link
                    href={`/tasks/${task.id}`}
                    className={`text-sm font-medium hover:text-blue-600 dark:hover:text-blue-400 transition-colors ${
                      task.completed
                        ? 'text-gray-500 dark:text-gray-600 line-through'
                        : 'text-gray-900 dark:text-white'
                    }`}
                  >
                    {task.title}
                  </Link>
                  {task.description && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {task.description}
                    </p>
                  )}
                  <div className="flex items-center space-x-2 mt-2">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                      task.completed
                        ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-400'
                        : 'bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-400'
                    }`}>
                      {task.completed ? 'Completed' : 'In Progress'}
                    </span>
                    <Badge variant={taskPriorities[task.id] || 'medium'}>
                      {(taskPriorities[task.id] || 'medium').charAt(0).toUpperCase() + (taskPriorities[task.id] || 'medium').slice(1)}
                    </Badge>
                  </div>
                </div>
                <button
                  onClick={() => openDeleteModal(task.id, task.title)}
                  disabled={actionLoading !== null}
                  className="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors disabled:opacity-50"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      <ConfirmModal
        isOpen={deleteModal.isOpen}
        onClose={closeDeleteModal}
        onConfirm={handleTaskDelete}
        title="Delete Task"
        message={`Are you sure you want to delete "${deleteModal.taskTitle}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        isLoading={actionLoading === 'delete'}
        variant="danger"
      />
    </div>
  );
}
