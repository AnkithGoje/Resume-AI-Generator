import React from 'react';
import { cn } from '../../lib/utils';
import { ChevronDown } from 'lucide-react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
    label?: string;
    options: { label: string; value: string }[];
}

export const Select: React.FC<SelectProps> = ({ className, label, id, options, ...props }) => {
    return (
        <div className="space-y-2">
            {label && (
                <label htmlFor={id} className="text-sm font-medium text-slate-700">
                    {label}
                </label>
            )}
            <div className="relative">
                <select
                    id={id}
                    className={cn(
                        "flex h-12 w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-2 pr-10 text-sm ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20 focus-visible:border-primary disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-200",
                        className
                    )}
                    {...props}
                >
                    {options.map((opt) => (
                        <option key={opt.value} value={opt.value}>
                            {opt.label}
                        </option>
                    ))}
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
                    <ChevronDown className="h-4 w-4" />
                </div>
            </div>
        </div>
    );
};
