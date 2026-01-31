'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { authUtils } from '@/lib/auth';

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check authentication status
    const authenticated = authUtils.isAuthenticated();
    setIsAuthenticated(authenticated);
    setLoading(false);

    // Redirect to dashboard if authenticated
    if (authenticated) {
      router.push('/dashboard');
    }
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white dark:bg-dark-950">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-electric-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-dark-950">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-electric-500/10 via-transparent to-electric-700/10 dark:from-electric-500/5 dark:via-transparent dark:to-electric-700/5"></div>

        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 sm:w-96 h-72 sm:h-96 bg-electric-500/20 dark:bg-electric-500/10 rounded-full mix-blend-multiply dark:mix-blend-screen filter blur-3xl animate-pulse-slow"></div>
          <div className="absolute bottom-20 right-10 w-72 sm:w-96 h-72 sm:h-96 bg-electric-700/20 dark:bg-electric-700/10 rounded-full mix-blend-multiply dark:mix-blend-screen filter blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-16 sm:pt-16 sm:pb-20 lg:pt-28 lg:pb-32">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center px-3 sm:px-4 py-1.5 sm:py-2 rounded-full bg-electric-100 dark:bg-electric-900/30 border border-electric-200 dark:border-electric-700/50 mb-6 sm:mb-8 animate-fade-in">
              <span className="relative flex h-2 w-2 mr-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-electric-500 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-electric-600"></span>
              </span>
              <span className="text-xs sm:text-sm font-semibold text-electric-700 dark:text-electric-400">
                Smart Task Evaluation Platform
              </span>
            </div>

            {/* Main Heading */}
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold text-gray-900 dark:text-white tracking-tight mb-4 sm:mb-6 animate-slide-up px-4 leading-tight">
              Transform Your Productivity
              <br />
              <span className="bg-gradient-to-r from-electric-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                Achieve More Every Day
              </span>
            </h1>

            {/* Subtitle */}
            <p className="max-w-3xl mx-auto text-base sm:text-lg md:text-xl lg:text-2xl text-gray-600 dark:text-gray-400 mb-8 sm:mb-10 animate-slide-up leading-relaxed px-4">
              The intelligent task management platform that helps you evaluate quality, track progress, and reach your goals faster.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 mb-8 sm:mb-12 animate-slide-up px-4">
              <Link
                href="/signup"
                className="group relative w-full sm:w-auto px-8 sm:px-10 py-4 sm:py-5 text-base sm:text-lg font-bold text-white bg-gradient-to-r from-electric-600 via-purple-600 to-pink-600 hover:from-electric-700 hover:via-purple-700 hover:to-pink-700 rounded-xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all overflow-hidden"
              >
                <span className="relative z-10 flex items-center justify-center space-x-2">
                  <span>Start Free Today</span>
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </Link>
              <Link
                href="/login"
                className="w-full sm:w-auto px-8 sm:px-10 py-4 sm:py-5 text-base sm:text-lg font-bold text-gray-700 dark:text-gray-300 bg-white dark:bg-dark-800 hover:bg-gray-50 dark:hover:bg-dark-700 rounded-xl border-2 border-gray-200 dark:border-dark-700 hover:border-electric-500 dark:hover:border-electric-500 shadow-md hover:shadow-lg transition-all"
              >
                Sign In
              </Link>
            </div>

            {/* Trust Badge */}
            <p className="text-sm sm:text-base text-gray-500 dark:text-gray-500 px-4 animate-fade-in">
              ✓ No credit card required  •  ✓ Free forever  •  ✓ 2-minute setup
            </p>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="relative py-12 sm:py-16 lg:py-24 bg-gray-50 dark:bg-dark-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10 sm:mb-12 lg:mb-16">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-3 sm:mb-4">
              Beyond Basic Task Management
            </h2>
            <p className="text-sm sm:text-base lg:text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto px-4">
              Evaluation-focused features designed for high-performing individuals and teams
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 lg:gap-8">
            {/* Feature 1 - Task Evaluation */}
            <div className="group bg-white dark:bg-dark-900 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft hover:shadow-large dark:hover:shadow-dark-large border border-gray-200 dark:border-dark-800 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-electric-500 to-electric-700 rounded-xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Task Evaluation</h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                Rate and evaluate every task with custom scoring. Track quality, not just completion.
              </p>
            </div>

            {/* Feature 2 - Progress Insights */}
            <div className="group bg-white dark:bg-dark-900 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft hover:shadow-large dark:hover:shadow-dark-large border border-gray-200 dark:border-dark-800 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-success-500 to-success-700 rounded-xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Progress Analytics</h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                Visualize your productivity trends with detailed charts and performance metrics.
              </p>
            </div>

            {/* Feature 3 - Smart Prioritization */}
            <div className="group bg-white dark:bg-dark-900 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft hover:shadow-large dark:hover:shadow-dark-large border border-gray-200 dark:border-dark-800 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-warning-500 to-warning-700 rounded-xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Smart Prioritization</h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                AI-powered priority suggestions based on deadlines, importance, and your work patterns.
              </p>
            </div>

            {/* Feature 4 - Team Collaboration */}
            <div className="group bg-white dark:bg-dark-900 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft hover:shadow-large dark:hover:shadow-dark-large border border-gray-200 dark:border-dark-800 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-electric-600 to-electric-800 rounded-xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Team Accountability</h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                Share evaluations, track team progress, and maintain accountability across projects.
              </p>
            </div>

            {/* Feature 5 - Dark Mode */}
            <div className="group bg-white dark:bg-dark-900 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft hover:shadow-large dark:hover:shadow-dark-large border border-gray-200 dark:border-dark-800 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-gray-700 to-gray-900 rounded-xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Premium Dark Mode</h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                Beautiful black theme optimized for focus and reduced eye strain during long sessions.
              </p>
            </div>

            {/* Feature 6 - Security */}
            <div className="group bg-white dark:bg-dark-900 rounded-xl sm:rounded-2xl p-6 sm:p-8 shadow-soft dark:shadow-dark-soft hover:shadow-large dark:hover:shadow-dark-large border border-gray-200 dark:border-dark-800 transition-all hover:-translate-y-1">
              <div className="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-danger-500 to-danger-700 rounded-xl flex items-center justify-center mb-4 sm:mb-6 group-hover:scale-110 transition-transform shadow-lg">
                <svg className="w-6 h-6 sm:w-7 sm:h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Enterprise Security</h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed">
                Bank-level encryption, JWT authentication, and complete data privacy for your tasks.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="relative py-16 sm:py-20 lg:py-24">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative bg-gradient-to-br from-electric-600 to-electric-800 rounded-2xl sm:rounded-3xl p-8 sm:p-10 lg:p-12 text-center shadow-2xl overflow-hidden">
            {/* Background Pattern */}
            <div className="absolute inset-0 opacity-10">
              <div className="absolute inset-0" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)', backgroundSize: '40px 40px' }}></div>
            </div>

            <div className="relative z-10">
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                Ready to Transform Your Productivity?
              </h2>
              <p className="text-xl text-electric-100 mb-8 max-w-2xl mx-auto">
                Join thousands of professionals who evaluate, track, and excel with Evaluation Todo.
              </p>
              <Link
                href="/signup"
                className="inline-flex items-center space-x-2 px-8 py-4 text-base font-semibold text-electric-600 bg-white hover:bg-gray-50 rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all"
              >
                <span>Start Free Today</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}