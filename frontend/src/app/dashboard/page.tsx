'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion, useSpring, useTransform } from 'framer-motion';
import { authUtils } from '@/lib/auth';
import { taskApi } from '@/lib/api';
import { Task } from '@/lib/types';
import { useTaskMetadata } from '@/hooks/useTaskMetadata';
import Card from '@/components/ui/Card';
import Badge from '@/components/ui/Badge';
import EmptyState from '@/components/ui/EmptyState';

// Animated number component for count-up effect
function AnimatedNumber({ value }: { value: number }) {
  const spring = useSpring(0, { duration: 1000 });
  const display = useTransform(spring, (latest) => Math.round(latest));

  useEffect(() => {
    spring.set(value);
  }, [value, spring]);

  return <motion.span>{display}</motion.span>;
}

export default function DashboardPage() {
  const [userId, setUserId] = useState<string | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [tasks, setTasks] = useState<Task[]>([]);
  const router = useRouter();
  const { taskPriorities } = useTaskMetadata();

  useEffect(() => {
    if (!authUtils.isAuthenticated()) {
      router.push('/login');
      return;
    }

    const userInfo = authUtils.getUserInfo();
    if (userInfo && userInfo.sub) {
      setUserId(userInfo.sub);
      setUserName(userInfo.email || 'User');
      loadTasks(userInfo.sub);
    } else {
      router.push('/login');
    }

    setLoading(false);
  }, [router]);

  const loadTasks = async (uid: string) => {
    try {
      const response = await taskApi.getTasks(uid);
      setTasks(response.data);
    } catch (err) {
      console.error('Error loading tasks:', err);
    }
  };

  // Statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.completed).length;
  const activeTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;

  // Get today's tasks (for demo, showing all incomplete tasks)
  const todayTasks = tasks.filter(t => !t.completed).slice(0, 5);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <div className="w-12 h-12 border-4 border-blue-200 dark:border-blue-900 border-t-blue-600 dark:border-t-blue-500 rounded-full animate-spin"></div>
          </div>
          <p className="text-gray-600 dark:text-gray-400 font-medium">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!userId) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen bg-gray-50 dark:bg-gray-950"
    >
      <main className="pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Welcome back, {userName?.split('@')[0]} 👋
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Here's what's happening with your tasks today
            </p>
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap gap-3 mb-8">
            <Link
              href="/tasks/new"
              className="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-sm hover:shadow-md transition-all font-medium"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Create Task
            </Link>
            <button className="inline-flex items-center px-5 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg shadow-sm hover:shadow-md transition-all font-medium">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              Focus Mode
            </button>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* Total Tasks */}
            <Card className="p-6">
              <div className="flex items-center justify-between mb-4">
                <motion.div
                  className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  transition={{ type: 'spring', stiffness: 400 }}
                >
                  <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </motion.div>
                <span className="text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">All time</span>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                  <AnimatedNumber value={totalTasks} />
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</p>
              </div>
            </Card>

            {/* Completed Tasks */}
            <Card className="p-6">
              <div className="flex items-center justify-between mb-4">
                <motion.div
                  className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  transition={{ type: 'spring', stiffness: 400 }}
                >
                  <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </motion.div>
                <div className="flex items-center space-x-1">
                  <svg className="w-3 h-3 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                  <span className="text-xs font-medium text-green-600 dark:text-green-400">+12%</span>
                </div>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                  <AnimatedNumber value={completedTasks} />
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Completed</p>
              </div>
            </Card>

            {/* In Progress */}
            <Card className="p-6">
              <div className="flex items-center justify-between mb-4">
                <motion.div
                  className="w-12 h-12 bg-amber-100 dark:bg-amber-900/30 rounded-lg flex items-center justify-center"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  transition={{ type: 'spring', stiffness: 400 }}
                >
                  <svg className="w-6 h-6 text-amber-600 dark:text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </motion.div>
                <span className="text-xs font-medium text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-2 py-1 rounded">Active</span>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                  <AnimatedNumber value={activeTasks} />
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">In Progress</p>
              </div>
            </Card>

            {/* Productivity */}
            <motion.div
              className="bg-gradient-to-br from-blue-600 to-purple-600 dark:from-blue-700 dark:to-purple-700 rounded-xl p-6 border border-blue-700 dark:border-blue-800 relative overflow-hidden"
              whileHover={{ y: -4, boxShadow: '0 20px 40px rgba(0, 0, 0, 0.2)' }}
              transition={{ duration: 0.2 }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
              <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                  <motion.div
                    className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center"
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    transition={{ type: 'spring', stiffness: 400 }}
                  >
                    <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                  </motion.div>
                  <span className="text-xs font-medium text-white bg-white/20 px-2 py-1 rounded">Score</span>
                </div>
                <div>
                  <p className="text-2xl font-bold text-white mb-1">
                    <AnimatedNumber value={completionRate} />%
                  </p>
                  <p className="text-sm text-blue-100">Productivity</p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Progress Bar */}
          <Card className="p-6 mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Overall Progress</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {completedTasks} of {totalTasks} tasks completed
                </p>
              </div>
              <motion.span
                className="text-2xl font-bold text-blue-600 dark:text-blue-400"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
              >
                <AnimatedNumber value={completionRate} />%
              </motion.span>
            </div>
            <div className="relative w-full h-4 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
              {/* Milestone markers */}
              <div className="absolute inset-0 flex items-center justify-between px-1">
                {[25, 50, 75].map((milestone) => (
                  <div
                    key={milestone}
                    className="w-0.5 h-full bg-gray-300 dark:bg-gray-700 z-10"
                    style={{ marginLeft: `${milestone}%` }}
                  />
                ))}
              </div>

              {/* Animated progress fill */}
              <motion.div
                className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-600 to-purple-600 rounded-full relative overflow-hidden"
                initial={{ width: 0 }}
                animate={{ width: `${completionRate}%` }}
                transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
              >
                {/* Shimmer effect */}
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
                  animate={{
                    x: ['-100%', '200%'],
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: 'linear',
                  }}
                />

                {/* Percentage label inside bar */}
                {completionRate > 10 && (
                  <span className="absolute right-2 top-1/2 -translate-y-1/2 text-xs font-bold text-white">
                    {completionRate}%
                  </span>
                )}
              </motion.div>
            </div>

            {/* Milestone labels */}
            <div className="flex justify-between mt-2 px-1">
              <span className="text-xs text-gray-500 dark:text-gray-400">0%</span>
              <span className="text-xs text-gray-500 dark:text-gray-400">25%</span>
              <span className="text-xs text-gray-500 dark:text-gray-400">50%</span>
              <span className="text-xs text-gray-500 dark:text-gray-400">75%</span>
              <span className="text-xs text-gray-500 dark:text-gray-400">100%</span>
            </div>
          </Card>

          {/* Today's Tasks */}
          <Card className="overflow-hidden" hover={false}>
            <div className="p-6 border-b border-gray-200 dark:border-gray-800">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Today's Tasks</h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {todayTasks.length} tasks to complete
                  </p>
                </div>
                <Link
                  href="/tasks"
                  className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
                >
                  View all →
                </Link>
              </div>
            </div>

            <div className="divide-y divide-gray-200 dark:divide-gray-800">
              {todayTasks.length === 0 ? (
                <EmptyState
                  icon={
                    <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center">
                      <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  }
                  title="All caught up!"
                  description="No pending tasks for today. Great job!"
                  action={
                    <Link
                      href="/tasks/new"
                      className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-sm hover:shadow-md transition-all font-medium"
                    >
                      <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                      Create New Task
                    </Link>
                  }
                />
              ) : (
                todayTasks.map((task, index) => {
                  const priority = taskPriorities[task.id] || 'medium';
                  const priorityColors = {
                    low: 'bg-green-500',
                    medium: 'bg-yellow-500',
                    high: 'bg-red-500',
                  };

                  return (
                    <motion.div
                      key={task.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors group"
                    >
                      <div className="flex items-center space-x-4">
                        <motion.button
                          className="flex-shrink-0 w-5 h-5 rounded border-2 border-gray-300 dark:border-gray-600 hover:border-blue-600 dark:hover:border-blue-400 transition-colors"
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          {task.completed && (
                            <svg className="w-full h-full text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          )}
                        </motion.button>

                        {/* Priority indicator dot */}
                        <div className={`w-2 h-2 rounded-full ${priorityColors[priority]} flex-shrink-0`} />

                        <div className="flex-1 min-w-0">
                          <div className="flex items-center space-x-2">
                            <p className={`text-sm font-medium ${task.completed ? 'text-gray-500 dark:text-gray-600 line-through' : 'text-gray-900 dark:text-white'}`}>
                              {task.title}
                            </p>
                            <Badge variant={priority} className="text-xs">
                              {priority}
                            </Badge>
                          </div>
                          {task.description && (
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 truncate">
                              {task.description}
                            </p>
                          )}
                        </div>
                        <Link
                          href={`/tasks/${task.id}`}
                          className="opacity-0 group-hover:opacity-100 transition-opacity text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                        >
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                          </svg>
                        </Link>
                      </div>
                    </motion.div>
                  );
                })
              )}
            </div>
          </Card>
        </div>
      </main>
    </motion.div>
  );
}
