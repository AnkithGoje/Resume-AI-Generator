import React from 'react';
import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline';
    size?: 'sm' | 'default';
    isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
    className,
    variant = 'primary',
    size = 'default',
    isLoading,
    children,
    ...props
}) => {
    const variants = {
        primary: 'bg-primary hover:bg-blue-700 text-white shadow-lg shadow-blue-500/30',
        secondary: 'bg-secondary hover:bg-indigo-700 text-white shadow-lg shadow-indigo-500/30',
        outline: 'border-2 border-slate-200 hover:border-primary/50 hover:bg-slate-50 text-slate-700'
    };

    const sizes = {
        default: 'px-6 py-3',
        sm: 'px-3 py-1.5'
    };

    return (
        <button
            className={cn(
                'inline-flex items-center justify-center rounded-xl font-semibold transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:pointer-events-none',
                variants[variant],
                sizes[size],
                className
            )}
            disabled={isLoading || props.disabled}
            {...props}
        >
            {isLoading && <Loader2 className="mr-2 h-5 w-5 animate-spin" />}
            {children}
        </button>
    );
};
