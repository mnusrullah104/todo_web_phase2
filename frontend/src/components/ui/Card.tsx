'use client';

import { motion, HTMLMotionProps } from 'framer-motion';
import { ReactNode } from 'react';

interface CardProps extends Omit<HTMLMotionProps<'div'>, 'children'> {
  children: ReactNode;
  variant?: 'default' | 'glass' | 'gradient';
  hover?: boolean;
  className?: string;
}

/**
 * Reusable Card component with glassmorphic design and hover effects
 * Supports multiple variants and smooth animations
 */
export default function Card({
  children,
  variant = 'default',
  hover = true,
  className = '',
  ...props
}: CardProps) {
  const baseClasses = 'rounded-xl border transition-all duration-200';

  const variantClasses = {
    default: 'bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800',
    glass: 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-gray-200/50 dark:border-gray-800/50',
    gradient: 'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800 border-blue-200 dark:border-gray-700',
  };

  const hoverAnimation = hover
    ? {
        whileHover: {
          y: -4,
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
        },
        transition: { duration: 0.2 },
      }
    : {};

  return (
    <motion.div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      {...hoverAnimation}
      {...props}
    >
      {children}
    </motion.div>
  );
}
