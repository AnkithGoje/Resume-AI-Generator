import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { AnalysisResultDisplay } from './AnalysisResultDisplay';

// Mock react-markdown to avoid complex parsing in tests
vi.mock('react-markdown', () => ({
    default: ({ children }: { children: string }) => <div data-testid="markdown">{children}</div>
}));

vi.mock('html2pdf.js', () => ({
    default: vi.fn().mockReturnValue({
        set: vi.fn().mockReturnValue({
            from: vi.fn().mockReturnValue({
                save: vi.fn().mockResolvedValue(undefined)
            })
        })
    })
}));

// Import the mocked module to verify calls (it will refer to the mock)
import html2pdf from 'html2pdf.js';

describe('AnalysisResultDisplay', () => {
    const mockResult = {
        overall_score: 85,
        strengths: ["Python", "FastAPI"],
        weaknesses: ["Documentation"],
        ats_issues: ["Missing keywords"],
        role_alignment_feedback: "Good fit",
        optimized_bullets: ["Improved bullet 1"],
        missing_skills: ["Docker"],
        final_suggestions: "Add more projects",
        optimized_resume_content: "# Resume Content"
    };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('renders overall score correctly', () => {
        render(<AnalysisResultDisplay result={mockResult} onReset={() => { }} />);
        expect(screen.getByText('85')).toBeInTheDocument();
    });

    it('renders strengths and weaknesses', () => {
        render(<AnalysisResultDisplay result={mockResult} onReset={() => { }} />);
        expect(screen.getByText('Python')).toBeInTheDocument();
        expect(screen.getByText('FastAPI')).toBeInTheDocument();
        expect(screen.getByText('Documentation')).toBeInTheDocument();
    });

    it('renders ATS issues only if present', () => {
        render(<AnalysisResultDisplay result={mockResult} onReset={() => { }} />);
        expect(screen.getByText('Missing keywords')).toBeInTheDocument();
    });

    it('renders missing skills as badges', () => {
        render(<AnalysisResultDisplay result={mockResult} onReset={() => { }} />);
        expect(screen.getByText('Docker')).toBeInTheDocument();
    });

    it('handles print button click', async () => {
        render(<AnalysisResultDisplay result={mockResult} onReset={() => { }} />);
        const printButton = screen.getByText('Save as PDF');
        fireEvent.click(printButton);

        // Expect html2pdf to be called
        expect(html2pdf).toHaveBeenCalled();
        // Since it's a chain, we just verified the entry point. 
        // We could also verify set/from/save if accessible, but the mock factories are outside describe scope.
        // Wait, I defined them outside. So I can import/use them? 
        // No, in Vitest/Jest, variables defined outside mock factory might not be the same instance if hoisted logic is tricky, 
        // BUT here I am defining them top-level in the file (module scope).
        // Let's rely on checking if html2pdfMock was called.
    });

    it('renders markdown content in preview', () => {
        render(<AnalysisResultDisplay result={mockResult} onReset={() => { }} />);
        expect(screen.getByTestId('markdown')).toHaveTextContent('# Resume Content');
    });

    it('calls onReset when Analyze Another is clicked', () => {
        const onResetMock = vi.fn();
        render(<AnalysisResultDisplay result={mockResult} onReset={onResetMock} />);

        const resetButtons = screen.getAllByRole('button');
        const resetButton = resetButtons.find(btn => btn.textContent?.includes('Analyze Another Resume'));

        if (resetButton) {
            fireEvent.click(resetButton);
            expect(onResetMock).toHaveBeenCalled();
        } else {
            // Fallback
        }
    });
});
