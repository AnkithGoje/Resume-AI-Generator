import React from 'react';
import { ShieldCheck, Target, FileText } from 'lucide-react';
import { Badge } from './ui/Badge';

export const Header: React.FC = () => {
    return (
        <div className="text-center space-y-6 max-w-3xl mx-auto mb-12">
            <div className="flex justify-center gap-3 mb-6">
                <Badge variant="accent" className="px-3 py-1 text-sm bg-blue-50 text-blue-700 border-blue-200">
                    <ShieldCheck className="w-3.5 h-3.5 mr-1.5" />
                    Expert Review
                </Badge>
                <Badge variant="accent" className="px-3 py-1 text-sm bg-indigo-50 text-indigo-700 border-indigo-200">
                    <Target className="w-3.5 h-3.5 mr-1.5" />
                    Role-Specific
                </Badge>
                <Badge variant="accent" className="px-3 py-1 text-sm bg-purple-50 text-purple-700 border-purple-200">
                    <FileText className="w-3.5 h-3.5 mr-1.5" />
                    ATS Optimized
                </Badge>
            </div>

            <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-slate-900 bg-clip-text">
                Land Your Dream Job with a <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Winning Resume</span>
            </h1>

            <p className="text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto">
                Get your resume optimized and improved by expert insights, tailored to your target role, optimized for ATS, and designed to impress recruiters.
            </p>
        </div>
    );
};
