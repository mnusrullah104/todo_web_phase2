# Tailwind CSS Best Practices

## Responsive Design

### Breakpoints
```css
/* Default (Mobile First) */
.className {
  /* Mobile styles */
}

/* Small devices (sm: 640px and up) */
@media (min-width: 640px) {
  .sm:className {}
}

/* Medium devices (md: 768px and up) */
@media (min-width: 768px) {
  .md:className {}
}

/* Large devices (lg: 1024px and up) */
@media (min-width: 1024px) {
  .lg:className {}
}

/* Extra large devices (xl: 1280px and up) */
@media (min-width: 1280px) {
  .xl:className {}
}

/* 2x large devices (2xl: 1536px and up) */
@media (min-width: 1536px) {
  .2xl:className {}
}
```

### Responsive Classes Example
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  <div className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
    Card 1
  </div>
  <div className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
    Card 2
  </div>
</div>
```

## Component Styling Patterns

### Button Component
```tsx
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick
}: ButtonProps) {
  const baseClasses = "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50";

  const variantClasses = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    outline: "border border-gray-300 bg-transparent hover:bg-gray-100",
    ghost: "hover:bg-gray-100 hover:text-gray-800"
  };

  const sizeClasses = {
    sm: "h-8 px-3 text-xs",
    md: "h-10 px-4 py-2 text-sm",
    lg: "h-12 px-6 text-base"
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${
        disabled ? 'opacity-50 cursor-not-allowed' : ''
      }`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### Card Component
```tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div className={`rounded-xl border bg-card text-card-foreground shadow ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '' }: CardProps) {
  return <div className={`flex flex-col space-y-1.5 p-6 ${className}`}>{children}</div>;
}

export function CardTitle({ children, className = '' }: CardProps) {
  return <h3 className={`font-semibold leading-none tracking-tight ${className}`}>{children}</h3>;
}

export function CardDescription({ children, className = '' }: CardProps) {
  return <p className={`text-sm text-muted-foreground ${className}`}>{children}</p>;
}

export function CardContent({ children, className = '' }: CardProps) {
  return <div className={`p-6 pt-0 ${className}`}>{children}</div>;
}

export function CardFooter({ children, className = '' }: CardProps) {
  return <div className={`flex items-center p-6 pt-0 ${className}`}>{children}</div>;
}
```

## Flexbox and Grid Layouts

### Flexbox Example
```tsx
<div className="flex flex-col md:flex-row gap-4 items-center justify-between">
  <div className="flex items-center space-x-4">
    <Logo />
    <nav className="hidden md:flex space-x-6">
      <a href="#" className="text-gray-600 hover:text-gray-900">Home</a>
      <a href="#" className="text-gray-600 hover:text-gray-900">About</a>
    </nav>
  </div>
  <Button>Sign In</Button>
</div>
```

### Grid Example
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map((item) => (
    <div key={item.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <h3 className="font-semibold">{item.title}</h3>
      <p className="text-gray-600 mt-2">{item.description}</p>
    </div>
  ))}
</div>
```

## Dark Mode Support

### Enable in tailwind.config.js
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // or 'media'
  // ...other config
}
```

### Usage
```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h1 className="text-2xl font-bold">Dark Mode Supported</h1>
  <p className="text-gray-600 dark:text-gray-300">This text adapts to dark mode</p>
</div>
```

## Utility Classes Organization

### Typography
```tsx
<h1 className="text-4xl font-bold tracking-tight">Heading</h1>
<p className="text-lg text-gray-600 leading-relaxed">Paragraph text</p>
<span className="text-sm font-medium text-blue-600">Badge text</span>
```

### Spacing
```tsx
<div className="p-4 m-2 space-y-4">
  <div className="mt-4 mb-2 ml-0 mr-0">Individual margins</div>
  <div className="pt-4 pb-2 pl-0 pr-0">Individual padding</div>
</div>
```

### Colors (using Tailwind's default palette)
```tsx
<div className="bg-blue-500 text-white">Blue background</div>
<div className="bg-green-100 text-green-800">Green accent</div>
<div className="bg-red-50 border-l-4 border-red-500">Alert box</div>
```

## Animations and Transitions

### Hover Effects
```tsx
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors duration-200">
  Hover me
</button>

<div className="transform hover:scale-105 transition-transform duration-200">
  Scale on hover
</div>
```

### Loading States
```tsx
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
  <div className="h-4 bg-gray-200 rounded"></div>
  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
</div>
```