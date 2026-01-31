'use client';

import Link from 'next/link';

export default function FloatingActionButton() {
  return (
    <Link
      href="/tasks/new"
      className="fixed bottom-6 right-6 lg:hidden w-14 h-14 bg-gradient-to-r from-electric-600 to-purple-600 hover:from-electric-700 hover:to-purple-700 text-white rounded-full shadow-lg hover:shadow-xl flex items-center justify-center z-50 transform hover:scale-110 transition-all"
      aria-label="Create new task"
    >
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
      </svg>
    </Link>
  );
}
