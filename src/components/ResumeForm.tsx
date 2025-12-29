import React, { useState, useRef } from 'react';
import { UploadCloud, File as FileIcon, X } from 'lucide-react';
import { Input } from './ui/Input';
import { Textarea } from './ui/Textarea';
import { Select } from './ui/Select';
import { Button } from './ui/Button';
import { Card, CardContent } from './ui/Card';
import { cn } from '../lib/utils';

interface ResumeFormProps {
    onSubmit: (formData: FormData) => void;
    isLoading: boolean;
}

export const ResumeForm: React.FC<ResumeFormProps> = ({ onSubmit, isLoading }) => {
    const [file, setFile] = useState<File | null>(null);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            validateAndSetFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            validateAndSetFile(e.target.files[0]);
        }
    };

    const validateAndSetFile = (file: File) => {
        if (file.size > 10 * 1024 * 1024) { // 10MB
            alert("File too large. Max 10MB.");
            return;
        }
        if (!['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'].includes(file.type)) {
            alert("Invalid file type. Please upload PDF, DOC, or DOCX.");
            return;
        }
        setFile(file);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData(e.currentTarget);
        formData.append('resume_file', file);
        onSubmit(formData);
    };

    return (
        <Card className="max-w-xl mx-auto border-0 shadow-2xl shadow-blue-900/5 ring-1 ring-slate-200">
            <CardContent className="pt-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <Input
                        id="target_role"
                        name="target_role"
                        label="Tell us about your target role"
                        placeholder="e.g. Software Developer, Data Analyst, Marketing Head"
                        required
                    />

                    <Textarea
                        id="job_description"
                        name="job_description"
                        label="Share the job description (Optional)"
                        placeholder="Paste the job description so we can tailor your resume perfectly"
                    />

                    <Select
                        id="experience_level"
                        name="experience_level"
                        label="Your experience level (Optional)"
                        options={[
                            { label: "Student / Fresher", value: "fresher" },
                            { label: "0–2 Years", value: "junior" },
                            { label: "2–5 Years", value: "mid" },
                            { label: "5+ Years", value: "senior" }
                        ]}
                    />

                    <div className="space-y-2">
                        <label className="text-sm font-medium text-slate-700">Upload your current resume</label>
                        <div
                            className={cn(
                                "relative flex flex-col items-center justify-center w-full h-32 rounded-xl border-2 border-dashed transition-all duration-200 bg-slate-50",
                                dragActive ? "border-primary bg-blue-50/50" : "border-slate-300 hover:border-slate-400 hover:bg-slate-100/50",
                                file ? "border-green-500 bg-green-50/30" : ""
                            )}
                            onDragEnter={handleDrag}
                            onDragLeave={handleDrag}
                            onDragOver={handleDrag}
                            onDrop={handleDrop}
                            onClick={() => fileInputRef.current?.click()}
                        >
                            <input
                                ref={fileInputRef}
                                type="file"
                                className="hidden"
                                onChange={handleChange}
                                accept=".pdf,.doc,.docx"
                            />

                            {file ? (
                                <div className="flex items-center gap-3 text-sm text-slate-700">
                                    <div className="p-2 bg-green-100 rounded-lg text-green-600">
                                        <FileIcon className="w-5 h-5" />
                                    </div>
                                    <div className="text-left">
                                        <p className="font-medium text-slate-900 truncate max-w-[200px]">{file.name}</p>
                                        <p className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                    </div>
                                    <button
                                        type="button"
                                        onClick={(e) => { e.stopPropagation(); setFile(null); }}
                                        className="p-1 hover:bg-slate-200 rounded-full transition-colors ml-2"
                                    >
                                        <X className="w-4 h-4 text-slate-500" />
                                    </button>
                                </div>
                            ) : (
                                <div className="text-center">
                                    <UploadCloud className="w-8 h-8 text-primary mx-auto mb-2 opacity-50" />
                                    <p className="text-sm font-medium text-slate-700">
                                        <span className="text-primary hover:underline cursor-pointer">Click to upload</span> or drag and drop
                                    </p>
                                    <p className="text-xs text-slate-500 mt-1">PDF, DOC, DOCX (Max 10MB)</p>
                                </div>
                            )}
                        </div>
                    </div>

                    <Button type="submit" className="w-full h-12 text-base" isLoading={isLoading} disabled={!file}>
                        Submit for Review
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
};
