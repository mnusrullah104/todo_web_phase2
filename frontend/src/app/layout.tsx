import { Inter } from 'next/font/google';
import ClientLayout from '@/components/ClientLayout';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata = {
  title: 'Evaluation Todo - Smart Task Management & Productivity',
  description: 'A premium SaaS productivity platform focused on task evaluation, progress measurement, and productivity insights. Track, evaluate, and optimize your workflow.',
  keywords: 'task management, productivity, evaluation, progress tracking, team collaboration, SaaS',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen antialiased flex flex-col`}>
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  );
}