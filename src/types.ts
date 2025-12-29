export interface AnalysisResult {
    overall_score: number;
    strengths: string[];
    weaknesses: string[];
    ats_issues: string[];
    role_alignment_feedback: string;
    optimized_bullets: string[];
    missing_skills: string[];
    final_suggestions: string;
    optimized_resume_content: string;
}
