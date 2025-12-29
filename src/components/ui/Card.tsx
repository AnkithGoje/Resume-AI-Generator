import React from 'react';
import { cn } from '../../lib/utils';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => {
    return (
        <div
            className={cn(
                "rounded-2xl border border-slate-100 bg-white text-slate-950 shadow-xl shadow-slate-200/50",
                className
            )}
            {...props}
        >
            {children}
        </div>
    );
};

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => {
    return (
        <div className={cn("p-6 pt-0 first:pt-6", className)} {...props}>
            {children}
        </div>
    );
};
