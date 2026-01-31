'use client';

import { ThemeProvider } from '@/contexts/ThemeContext';
import Navbar from '@/components/ui/Navbar';
import Footer from '@/components/ui/Footer';

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider>
      <Navbar />
      <div className="flex-grow">
        {children}
      </div>
      <Footer />
    </ThemeProvider>
  );
}
