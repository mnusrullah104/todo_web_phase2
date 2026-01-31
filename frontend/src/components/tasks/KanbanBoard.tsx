'use client';

import { useState } from 'react';
import { DndContext, DragEndEvent, DragOverlay, closestCorners, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Task } from '@/lib/types';
import { Priority } from '@/hooks/useTaskMetadata';
import Badge from '@/components/ui/Badge';
import Card from '@/components/ui/Card';

interface KanbanBoardProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, completed: boolean) => void;
  onTaskDelete: (taskId: string) => void;
  taskPriorities: Record<string, Priority>;
}

interface KanbanTaskCardProps {
  task: Task;
  priority: Priority;
  onDelete: (taskId: string) => void;
}

function KanbanTaskCard({ task, priority, onDelete }: KanbanTaskCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: task.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-3 cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-2">
        <Link
          href={`/tasks/${task.id}`}
          className="text-sm font-medium text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex-1"
          onClick={(e) => e.stopPropagation()}
        >
          {task.title}
        </Link>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(task.id);
          }}
          className="ml-2 p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {task.description && (
        <p className="text-xs text-gray-500 dark:text-gray-400 mb-3 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="flex items-center justify-between">
        <Badge variant={priority} className="text-xs">
          {priority.charAt(0).toUpperCase() + priority.slice(1)}
        </Badge>
        <span className="text-xs text-gray-400">
          {new Date(task.created_at).toLocaleDateString()}
        </span>
      </div>
    </motion.div>
  );
}

interface KanbanColumnProps {
  id: string;
  title: string;
  tasks: Task[];
  taskPriorities: Record<string, Priority>;
  onTaskDelete: (taskId: string) => void;
  count: number;
  color: string;
}

function KanbanColumn({ id, title, tasks, taskPriorities, onTaskDelete, count, color }: KanbanColumnProps) {
  return (
    <div className="flex-1 min-w-[280px] md:min-w-[300px]">
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white flex items-center">
            <span className={`w-2 h-2 rounded-full ${color} mr-2`}></span>
            {title}
          </h3>
          <span className="text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded-full">
            {count}
          </span>
        </div>
      </div>

      <SortableContext items={tasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
        <div className="space-y-3 min-h-[200px] bg-gray-50 dark:bg-gray-900/50 rounded-lg p-3">
          {tasks.length === 0 ? (
            <div className="flex items-center justify-center h-32 text-gray-400 dark:text-gray-600 text-sm">
              Drop tasks here
            </div>
          ) : (
            tasks.map((task) => (
              <KanbanTaskCard
                key={task.id}
                task={task}
                priority={taskPriorities[task.id] || 'medium'}
                onDelete={onTaskDelete}
              />
            ))
          )}
        </div>
      </SortableContext>
    </div>
  );
}

export default function KanbanBoard({ tasks, onTaskUpdate, onTaskDelete, taskPriorities }: KanbanBoardProps) {
  const [activeId, setActiveId] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const todoTasks = tasks.filter(t => !t.completed);
  const doneTasks = tasks.filter(t => t.completed);

  const handleDragStart = (event: DragEndEvent) => {
    setActiveId(event.active.id as string);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveId(null);

    if (!over) return;

    const taskId = active.id as string;
    const overId = over.id as string;

    // Determine if we're dropping on a column or another task
    const isOverColumn = overId === 'todo' || overId === 'done';

    if (isOverColumn) {
      const newCompleted = overId === 'done';
      const task = tasks.find(t => t.id === taskId);

      if (task && task.completed !== newCompleted) {
        onTaskUpdate(taskId, newCompleted);
      }
    } else {
      // Dropped on another task - determine which column it's in
      const overTask = tasks.find(t => t.id === overId);
      if (overTask) {
        const task = tasks.find(t => t.id === taskId);
        if (task && task.completed !== overTask.completed) {
          onTaskUpdate(taskId, overTask.completed);
        }
      }
    }
  };

  const handleDragCancel = () => {
    setActiveId(null);
  };

  const activeTask = activeId ? tasks.find(t => t.id === activeId) : null;

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      onDragCancel={handleDragCancel}
    >
      <div className="flex flex-col md:flex-row gap-6 overflow-x-auto pb-4">
        <div id="todo" className="flex-1 min-w-[280px] md:min-w-[300px]">
          <KanbanColumn
            id="todo"
            title="To Do"
            tasks={todoTasks}
            taskPriorities={taskPriorities}
            onTaskDelete={onTaskDelete}
            count={todoTasks.length}
            color="bg-amber-500"
          />
        </div>

        <div id="done" className="flex-1 min-w-[280px] md:min-w-[300px]">
          <KanbanColumn
            id="done"
            title="Done"
            tasks={doneTasks}
            taskPriorities={taskPriorities}
            onTaskDelete={onTaskDelete}
            count={doneTasks.length}
            color="bg-green-500"
          />
        </div>
      </div>

      <DragOverlay>
        {activeTask ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg border-2 border-blue-500 p-4 shadow-xl rotate-3">
            <p className="text-sm font-medium text-gray-900 dark:text-white">
              {activeTask.title}
            </p>
          </div>
        ) : null}
      </DragOverlay>
    </DndContext>
  );
}
