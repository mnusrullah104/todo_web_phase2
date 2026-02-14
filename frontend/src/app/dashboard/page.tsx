/**
 * Modern Dashboard - Production Ready
 * Inspired by Notion and Linear design systems
 */
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { authUtils } from '@/lib/auth';
import { taskApi } from '@/lib/api';
import { Task } from '@/lib/types';
import {
  CheckCircle2,
  Clock,
  TrendingUp,
  Plus,
  ArrowRight,
  Sparkles,
  Target,
  Zap
} from 'lucide-react';

export default function DashboardPage() {
  const [userId, setUserId] = useState<string | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [tasks, setTasks] = useState<Task[]>([]);
  const router = useRouter();

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
  }, [router]);

  const loadTasks = async (uid: string) => {
    try {
      setLoading(true);
      const data = await taskApi.getTasks(uid);
      setTasks(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error loading tasks:', err);
      setTasks([]); // Ensure tasks is always an array
    } finally {
      setLoading(false);
    }
  };

  // Statistics - with safety checks
  const totalTasks = tasks?.length || 0;
  const completedTasks = tasks?.filter(t => t.completed).length || 0;
  const activeTasks = totalTasks - completedTasks;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0;
  const recentTasks = tasks?.filter(t => !t.completed).slice(0, 5) || [];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 border-4 border-blue-200 dark:border-blue-900 border-t-blue-600 dark:border-t-blue-500 rounded-full animate-spin"></div>
          <p className="text-slate-600 dark:text-slate-400 font-medium">Loading your workspace...</p>
        </div>
      </div>
    );
  }

  if (!userId) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-950">
      <main className="pt-20 pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8"
          >
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                Welcome back
              </span>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-900 dark:from-white dark:via-blue-100 dark:to-indigo-100 bg-clip-text text-transparent mb-2">
              {userName?.split('@')[0]}'s Workspace
            </h1>
            <p className="text-slate-600 dark:text-slate-400 text-lg">
              Here's what's happening with your tasks today
            </p>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="flex flex-wrap gap-3 mb-8"
          >
            <Link
              href="/tasks"
              className="group inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 font-medium"
            >
              <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" />
              New Task
            </Link>
            <button className="inline-flex items-center gap-2 px-6 py-3 bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:bg-white dark:hover:bg-slate-800 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 font-medium">
              <Zap className="w-5 h-5" />
              Focus Mode
            </button>
          </motion.div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* Total Tasks Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="group relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25">
                    <Target className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xs font-medium text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-700/50 px-3 py-1 rounded-full">
                    Total
                  </span>
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900 dark:text-white mb-1">
                    {totalTasks}
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">All Tasks</p>
                </div>
              </div>
            </motion.div>

            {/* Completed Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="group relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-green-500/25">
                    <CheckCircle2 className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex items-center gap-1 text-green-600 dark:text-green-400">
                    <TrendingUp className="w-4 h-4" />
                    <span className="text-xs font-medium">+12%</span>
                  </div>
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900 dark:text-white mb-1">
                    {completedTasks}
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">Completed</p>
                </div>
              </div>
            </motion.div>

            {/* Active Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="group relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg shadow-amber-500/25">
                    <Clock className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xs font-medium text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-3 py-1 rounded-full">
                    Active
                  </span>
                </div>
                <div>
                  <p className="text-3xl font-bold text-slate-900 dark:text-white mb-1">
                    {activeTasks}
                  </p>
                  <p className="text-sm text-slate-600 dark:text-slate-400">In Progress</p>
                </div>
              </div>
            </motion.div>

            {/* Productivity Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="relative bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 rounded-2xl p-6 shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 overflow-hidden group"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-white/20 backdrop-blur-xl rounded-xl flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xs font-medium text-white bg-white/20 backdrop-blur-xl px-3 py-1 rounded-full">
                    Score
                  </span>
                </div>
                <div>
                  <p className="text-3xl font-bold text-white mb-1">
                    {completionRate}%
                  </p>
                  <p className="text-sm text-blue-100">Productivity</p>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Progress Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-2xl p-6 border border-slate-200 dark:border-slate-700 shadow-lg mb-8"
          >
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-1">
                  Overall Progress
                </h3>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  {completedTasks} of {totalTasks} tasks completed
                </p>
              </div>
              <span className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                {completionRate}%
              </span>
            </div>

            <div className="relative w-full h-3 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
              <motion.div
                className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${completionRate}%` }}
                transition={{ duration: 1, ease: 'easeOut', delay: 0.7 }}
              >
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent"
                  animate={{ x: ['-100%', '200%'] }}
                  transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                />
              </motion.div>
            </div>
          </motion.div>

          {/* Recent Tasks */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
            className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-2xl border border-slate-200 dark:border-slate-700 shadow-lg overflow-hidden"
          >
            <div className="p-6 border-b border-slate-200 dark:border-slate-700">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-1">
                    Recent Tasks
                  </h2>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {recentTasks.length} active tasks
                  </p>
                </div>
                <Link
                  href="/tasks"
                  className="group inline-flex items-center gap-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
                >
                  View all
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </div>

            <div className="divide-y divide-slate-200 dark:divide-slate-700">
              {recentTasks.length === 0 ? (
                <div className="p-12 text-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500/20 to-indigo-600/20 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <CheckCircle2 className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                    All caught up!
                  </h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
                    No pending tasks. Great job!
                  </p>
                  <Link
                    href="/tasks"
                    className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 transition-all duration-300 font-medium"
                  >
                    <Plus className="w-5 h-5" />
                    Create New Task
                  </Link>
                </div>
              ) : (
                recentTasks.map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.8 + index * 0.05 }}
                    className="group p-4 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <button className="flex-shrink-0 w-5 h-5 rounded-md border-2 border-slate-300 dark:border-slate-600 hover:border-blue-600 dark:hover:border-blue-400 transition-colors">
                        {task.completed && (
                          <CheckCircle2 className="w-full h-full text-blue-600" />
                        )}
                      </button>

                      <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium ${task.completed ? 'text-slate-500 dark:text-slate-600 line-through' : 'text-slate-900 dark:text-white'}`}>
                          {task.title}
                        </p>
                        {task.description && (
                          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 truncate">
                            {task.description}
                          </p>
                        )}
                      </div>

                      <Link
                        href={`/tasks/${task.id}`}
                        className="opacity-0 group-hover:opacity-100 transition-opacity text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                      >
                        <ArrowRight className="w-5 h-5" />
                      </Link>
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}
