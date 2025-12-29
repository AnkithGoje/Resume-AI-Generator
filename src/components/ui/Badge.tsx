import React from 'react';
import { cn } from '../../lib/utils';

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'outline' | 'secondary' | 'accent';
}

export const Badge: React.FC<BadgeProps> = ({ className, variant = 'default', ...props }) => {
    const variants = {
        default: 'bg-primary/10 text-primary hover:bg-primary/20 border-primary/20',
        secondary: 'bg-slate-100 text-slate-900 hover:bg-slate-200/80 border-slate-200',
        outline: 'text-slate-950 border border-slate-200',
        accent: 'bg-indigo-50 text-indigo-700 border-indigo-200'
    };

    return (
        <div
            className={cn(
                "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
                variants[variant],
                className
            )}
            {...props}
        />
    );
};
