'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authUtils } from '@/lib/auth';
import { taskApi } from '@/lib/api';

export default function NewTaskPage() {
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  useEffect(() => {
    if (!authUtils.isAuthenticated()) {
      router.push('/login');
      return;
    }

    const userInfo = authUtils.getUserInfo();
    if (userInfo && userInfo.sub) {
      setUserId(userInfo.sub);
    } else {
      router.push('/login');
    }

    setLoading(false);
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Task title is required');
      return;
    }

    if (!userId) {
      setError('User not authenticated');
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      await taskApi.createTask(userId, {
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Redirect to tasks page on success
      router.push('/tasks');
    } catch (err) {
      console.error('Error creating task:', err);
      setError('Failed to create task. Please try again.');
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-dark-950">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-electric-200 dark:border-electric-900 border-t-electric-600 dark:border-t-electric-500 rounded-full animate-spin"></div>
          </div>
          <p className="text-gray-600 dark:text-gray-400 font-medium">Loading...</p>
        </div>
      </div>
    );
  }

  if (!userId) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-950">
      {/* Main Content */}
      <main className="pt-20 sm:pt-24 pb-12">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Back Button */}
          <Link
            href="/tasks"
            className="inline-flex items-center text-gray-600 dark:text-gray-400 hover:text-electric-600 dark:hover:text-electric-400 mb-8 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Tasks
          </Link>

          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Create New Task
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Add a new task to your productivity workflow
            </p>
          </div>

          {/* Task Creation Form */}
          <div className="bg-white dark:bg-dark-900 rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft border border-gray-200 dark:border-dark-800">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Error Message */}
              {error && (
                <div className="p-4 bg-danger-50 dark:bg-danger-900/20 border border-danger-200 dark:border-danger-800 rounded-xl">
                  <p className="text-sm text-danger-600 dark:text-danger-400">{error}</p>
                </div>
              )}

              {/* Title Field */}
              <div>
                <label htmlFor="title" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Task Title <span className="text-danger-500">*</span>
                </label>
                <input
                  type="text"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-dark-700 rounded-xl focus:ring-2 focus:ring-electric-500 dark:focus:ring-electric-600 focus:border-transparent transition-all text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                  placeholder="Enter task title..."
                  maxLength={255}
                  required
                  autoFocus
                />
                <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
                  {title.length}/255 characters
                </p>
              </div>

              {/* Description Field */}
              <div>
                <label htmlFor="description" className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                  Description (Optional)
                </label>
                <textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-dark-700 rounded-xl focus:ring-2 focus:ring-electric-500 dark:focus:ring-electric-600 focus:border-transparent transition-all resize-none text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                  placeholder="Add more details about this task..."
                  rows={6}
                  maxLength={1000}
                />
                <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
                  {description.length}/1000 characters
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3 pt-4">
                <button
                  type="submit"
                  disabled={submitting || !title.trim()}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-electric-600 to-purple-600 hover:from-electric-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-xl shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all font-semibold disabled:cursor-not-allowed disabled:transform-none"
                >
                  {submitting ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Creating...
                    </span>
                  ) : (
                    'Create Task'
                  )}
                </button>
                <Link
                  href="/tasks"
                  className="flex-1 px-6 py-3 bg-white dark:bg-dark-800 text-gray-700 dark:text-gray-300 rounded-xl shadow-md hover:shadow-lg border border-gray-200 dark:border-dark-700 hover:border-electric-500 dark:hover:border-electric-500 transform hover:-translate-y-0.5 transition-all font-semibold text-center"
                >
                  Cancel
                </Link>
              </div>
            </form>
          </div>

          {/* Tips Section */}
          <div className="mt-8 bg-electric-50 dark:bg-electric-900/20 rounded-xl p-6 border border-electric-200 dark:border-electric-800">
            <h3 className="text-sm font-semibold text-electric-900 dark:text-electric-300 mb-3">
              💡 Tips for Better Tasks
            </h3>
            <ul className="space-y-2 text-sm text-electric-800 dark:text-electric-400">
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Use clear, action-oriented titles (e.g., "Review Q4 report")</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Add context in the description to remember details later</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Break large tasks into smaller, manageable pieces</span>
              </li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
