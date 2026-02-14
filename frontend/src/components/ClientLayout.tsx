'use client';

import { useState, useEffect } from 'react';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { ToastProvider } from '@/contexts/ToastContext';
import Navbar from '@/components/ui/Navbar';
import Footer from '@/components/ui/Footer';
import ChatWidget from '@/components/ChatWidget';
import { authUtils } from '@/lib/auth';
import { createTestToken } from '@/lib/test-auth';

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  const [userId, setUserId] = useState<string>('');

  // Handle client-side mounting to prevent hydration errors
  useEffect(() => {
    setMounted(true);
    const storedUserId = localStorage.getItem('userId') || '';
    setUserId(storedUserId);

    // Auto-setup test authentication when userId is present but no token exists
    if (storedUserId) {
      const hasToken = authUtils.isAuthenticated();
      if (!hasToken) {
        const token = createTestToken(storedUserId, 'test@example.com');
        authUtils.setToken(token);
        console.log('✅ Test authentication auto-configured for userId:', storedUserId);
      }
    }
  }, []);

  return (
    <ThemeProvider>
      <ToastProvider>
        <Navbar />
        <div className="flex-grow">
          {children}
        </div>
        <Footer />
        {/* Phase III - AI Chatbot Widget - Only render after mount to prevent hydration errors */}
        {mounted && userId && <ChatWidget userId={userId} />}
      </ToastProvider>
    </ThemeProvider>
  );
}
