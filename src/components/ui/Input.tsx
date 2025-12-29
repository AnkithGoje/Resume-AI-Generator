import React from 'react';
import { cn } from '../../lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
}

export const Input: React.FC<InputProps> = ({ className, label, id, ...props }) => {
    return (
        <div className="space-y-2">
            {label && (
                <label htmlFor={id} className="text-sm font-medium text-slate-700">
                    {label}
                </label>
            )}
            <input
                id={id}
                className={cn(
                    "flex h-12 w-full rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-slate-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20 focus-visible:border-primary disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200",
                    className
                )}
                {...props}
            />
        </div>
    );
};
