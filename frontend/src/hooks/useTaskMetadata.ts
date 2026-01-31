'use client';

import { useState, useEffect } from 'react';

export type Priority = 'low' | 'medium' | 'high';

export interface TaskMetadata {
  taskDueDates: Record<string, string>;
  taskPriorities: Record<string, Priority>;
  setDueDate: (taskId: string, date: string) => void;
  setPriority: (taskId: string, priority: Priority) => void;
  removeDueDate: (taskId: string) => void;
  removePriority: (taskId: string) => void;
}

/**
 * Custom hook to manage task metadata (priorities and due dates) in localStorage
 * Shared across Dashboard, Tasks, and Calendar components
 */
export function useTaskMetadata(): TaskMetadata {
  const [taskDueDates, setTaskDueDates] = useState<Record<string, string>>({});
  const [taskPriorities, setTaskPriorities] = useState<Record<string, Priority>>({});

  // Load from localStorage on mount
  useEffect(() => {
    const dates = localStorage.getItem('task_due_dates');
    const priorities = localStorage.getItem('task_priorities');

    if (dates) {
      try {
        setTaskDueDates(JSON.parse(dates));
      } catch (error) {
        console.error('Failed to parse task due dates:', error);
      }
    }

    if (priorities) {
      try {
        setTaskPriorities(JSON.parse(priorities));
      } catch (error) {
        console.error('Failed to parse task priorities:', error);
      }
    }
  }, []);

  const setDueDate = (taskId: string, date: string) => {
    const updated = { ...taskDueDates, [taskId]: date };
    setTaskDueDates(updated);
    localStorage.setItem('task_due_dates', JSON.stringify(updated));
  };

  const setPriority = (taskId: string, priority: Priority) => {
    const updated = { ...taskPriorities, [taskId]: priority };
    setTaskPriorities(updated);
    localStorage.setItem('task_priorities', JSON.stringify(updated));
  };

  const removeDueDate = (taskId: string) => {
    const updated = { ...taskDueDates };
    delete updated[taskId];
    setTaskDueDates(updated);
    localStorage.setItem('task_due_dates', JSON.stringify(updated));
  };

  const removePriority = (taskId: string) => {
    const updated = { ...taskPriorities };
    delete updated[taskId];
    setTaskPriorities(updated);
    localStorage.setItem('task_priorities', JSON.stringify(updated));
  };

  return {
    taskDueDates,
    taskPriorities,
    setDueDate,
    setPriority,
    removeDueDate,
    removePriority,
  };
}
