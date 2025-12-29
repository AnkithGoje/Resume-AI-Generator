import React from 'react';
import { cn } from '../../lib/utils';

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
}

export const Textarea: React.FC<TextareaProps> = ({ className, label, id, ...props }) => {
    return (
        <div className="space-y-2">
            {label && (
                <label htmlFor={id} className="text-sm font-medium text-slate-700">
                    {label}
                </label>
            )}
            <textarea
                id={id}
                className={cn(
                    "flex min-h-[120px] w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm ring-offset-white placeholder:text-slate-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20 focus-visible:border-primary disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200 resize-y",
                    className
                )}
                {...props}
            />
        </div>
    );
};
