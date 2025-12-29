import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ResumePreview } from './ResumePreview';

// Mock react-markdown
vi.mock('react-markdown', () => ({
    default: ({ children }: { children: string }) => <div data-testid="markdown-preview">{children}</div>
}));

describe('ResumePreview', () => {
    const mockContent = "# Optimized Resume\n## Experience\n* Achieved X";

    it('renders markdown content', () => {
        render(<ResumePreview content={mockContent} />);
        expect(screen.getByTestId('markdown-preview')).toHaveTextContent("Optimized Resume");
    });

    it('handles empty content', () => {
        render(<ResumePreview content="" />);
        expect(screen.getByTestId('markdown-preview')).toHaveTextContent("");
    });

    it('applies print styles', () => {
        const { container } = render(<ResumePreview content={mockContent} />);
        expect(container.firstChild).toHaveClass('bg-white');
    });
});
