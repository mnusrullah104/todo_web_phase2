'use client';

import { ThemeProvider } from '@/contexts/ThemeContext';
import Navbar from '@/components/ui/Navbar';
import Footer from '@/components/ui/Footer';
import ChatWidget from '@/components/ChatWidget';

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  // TODO: Replace with actual authenticated user ID from Better Auth
  // For now, using a placeholder. In production, this should come from auth context
  const userId = typeof window !== 'undefined' ? localStorage.getItem('userId') || '' : '';

  return (
    <ThemeProvider>
      <Navbar />
      <div className="flex-grow">
        {children}
      </div>
      <Footer />
      {/* Phase III - AI Chatbot Widget */}
      {userId && <ChatWidget userId={userId} />}
    </ThemeProvider>
  );
}
