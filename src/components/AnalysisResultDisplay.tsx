import React, { useRef } from 'react';
import type { AnalysisResult } from '../types';


import { ResumePreview } from './ResumePreview';
import { Card, CardContent } from './ui/Card';
import { Badge } from './ui/Badge';
import { CheckCircle2, XCircle, AlertTriangle, Lightbulb, Download, FileText } from 'lucide-react';
import { Button } from './ui/Button';

// Simple icon wrapper placed before usage or defined separately
const TargetIcon = ({ className }: { className?: string }) => (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" /></svg>
);

interface AnalysisResultProps {
    result: AnalysisResult;
    onReset: () => void;
}

export const AnalysisResultDisplay: React.FC<AnalysisResultProps> = ({ result, onReset }) => {
    const componentRef = useRef<HTMLDivElement>(null);

    const handleDownloadPDF = async () => {
        const element = componentRef.current;
        if (!element) return;

        const opt = {
            margin: 0,
            filename: `Optimized_Resume_${result.overall_score}.pdf`,
            image: { type: 'jpeg' as const, quality: 0.98 },
            html2canvas: { scale: 2, useCORS: true },
            jsPDF: { unit: 'mm' as const, format: 'a4' as const, orientation: 'portrait' as const }
        };

        try {
            // @ts-ignore
            const html2pdfModule = (await import('html2pdf.js')).default;
            await html2pdfModule().set(opt).from(element).save();
        } catch (error) {
            console.error('Error generating PDF:', error);
            alert('Failed to generate PDF. Please try again.');
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            {/* Overall Score Section */}
            <div className="text-center space-y-4">
                <div className="inline-flex items-center justify-center relative">
                    <svg className="w-40 h-40 transform -rotate-90">
                        <circle
                            className="text-slate-200"
                            strokeWidth="8"
                            stroke="currentColor"
                            fill="transparent"
                            r="70"
                            cx="80"
                            cy="80"
                        />
                        <circle
                            className="text-primary transition-all duration-1000 ease-out"
                            strokeWidth="8"
                            strokeDasharray={440}
                            strokeDashoffset={440 - (440 * result.overall_score) / 100}
                            strokeLinecap="round"
                            stroke="currentColor"
                            fill="transparent"
                            r="70"
                            cx="80"
                            cy="80"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-4xl font-bold text-slate-900">{result.overall_score}</span>
                        <span className="text-sm font-medium text-slate-500 uppercase tracking-widest">Score</span>
                    </div>
                </div>
                <h2 className="text-2xl font-bold text-slate-900">
                    {result.overall_score >= 80 ? "Excellent Job!" : result.overall_score >= 60 ? "Good Start!" : "Needs Improvement"}
                </h2>
                <p className="text-slate-600 max-w-xl mx-auto">{result.final_suggestions}</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                {/* Strengths */}
                <Card>
                    <CardContent className="pt-6">
                        <h3 className="flex items-center text-lg font-semibold text-slate-900 mb-4">
                            <CheckCircle2 className="w-5 h-5 text-green-500 mr-2" /> Strengths
                        </h3>
                        <ul className="space-y-3">
                            {result.strengths.map((strength, index) => (
                                <li key={index} className="flex items-start text-sm text-slate-600">
                                    <div className="mr-2 mt-1.5 w-1.5 h-1.5 rounded-full bg-green-500 shrink-0" />
                                    {strength}
                                </li>
                            ))}
                        </ul>
                    </CardContent>
                </Card>

                {/* Weaknesses */}
                <Card>
                    <CardContent className="pt-6">
                        <h3 className="flex items-center text-lg font-semibold text-slate-900 mb-4">
                            <XCircle className="w-5 h-5 text-red-500 mr-2" /> Areas for Improvement
                        </h3>
                        <ul className="space-y-3">
                            {result.weaknesses.map((weakness, index) => (
                                <li key={index} className="flex items-start text-sm text-slate-600">
                                    <div className="mr-2 mt-1.5 w-1.5 h-1.5 rounded-full bg-red-500 shrink-0" />
                                    {weakness}
                                </li>
                            ))}
                        </ul>
                    </CardContent>
                </Card>
            </div>

            {/* ATS Issues */}
            {result.ats_issues.length > 0 && (
                <Card className="border-orange-200 bg-orange-50/30">
                    <CardContent className="pt-6">
                        <h3 className="flex items-center text-lg font-semibold text-orange-800 mb-4">
                            <AlertTriangle className="w-5 h-5 mr-2" /> ATS Compatibility Issues
                        </h3>
                        <div className="space-y-2">
                            {result.ats_issues.map((issue, index) => (
                                <div key={index} className="flex items-start bg-white p-3 rounded-lg border border-orange-100 text-sm text-slate-700">
                                    <AlertTriangle className="w-4 h-4 text-orange-500 mr-3 mt-0.5 shrink-0" />
                                    {issue}
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Role Alignment */}
            <Card className="bg-gradient-to-br from-slate-900 to-slate-800 text-white border-0">
                <CardContent className="pt-6">
                    <h3 className="text-lg font-semibold mb-4 flex items-center">
                        <TargetIcon className="w-5 h-5 mr-2 text-blue-400" />
                        Role Alignment
                    </h3>
                    <p className="text-slate-300 leading-relaxed">
                        {result.role_alignment_feedback}
                    </p>
                </CardContent>
            </Card>

            {/* Missing Skills */}
            {result.missing_skills.length > 0 && (
                <div className="space-y-3">
                    <h3 className="text-lg font-semibold text-slate-900">Missing Critical Skills</h3>
                    <div className="flex flex-wrap gap-2">
                        {result.missing_skills.map((skill, index) => (
                            <Badge key={index} variant="secondary" className="px-3 py-1.5 text-sm bg-slate-200">
                                {skill}
                            </Badge>
                        ))}
                    </div>
                </div>
            )}

            {/* Optimized Bullets */}
            <div className="space-y-4">
                <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                    <Lightbulb className="w-5 h-5 text-yellow-500 mr-2" /> AI Suggested Improvements
                </h3>
                <div className="grid gap-4">
                    {result.optimized_bullets.map((bullet, index) => (
                        <div key={index} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                            <div className="flex gap-4">
                                <div className="shrink-0 w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm">
                                    {index + 1}
                                </div>
                                <p className="text-slate-700 text-sm leading-relaxed pt-1.5">{bullet}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Full Optimized Resume Section */}
            {result.optimized_resume_content && (
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-lg font-semibold text-slate-900 flex items-center">
                            <FileText className="w-5 h-5 text-indigo-600 mr-2" />
                            Optimized Resume Preview
                        </h3>
                        <div className="flex gap-2">
                            <Button
                                variant="secondary"
                                size="sm"
                                onClick={() => navigator.clipboard.writeText(result.optimized_resume_content)}
                                className="h-8 text-xs"
                            >
                                Copy Markdown
                            </Button>
                            <Button
                                variant="primary"
                                size="sm"
                                onClick={handleDownloadPDF}
                                className="h-8 text-xs bg-indigo-600 hover:bg-indigo-700"
                            >
                                <Download className="w-3 h-3 mr-1.5" /> Save as PDF
                            </Button>
                        </div>
                    </div>

                    {/* Visual Preview Container */}
                    <div className="bg-slate-100 p-8 rounded-xl border border-slate-200 overflow-hidden shadow-inner flex justify-center">
                        <div className="scale-[0.8] origin-top text-left">
                            <ResumePreview ref={componentRef} content={result.optimized_resume_content} />
                        </div>
                    </div>
                </div>
            )}

            <div className="pt-8 flex justify-center gap-4">
                <Button variant="outline" onClick={onReset}>
                    Analyze Another Resume
                </Button>
            </div>
        </div>
    );
};
