import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ResumeForm } from './ResumeForm';

describe('ResumeForm', () => {
    it('renders input fields correctly', () => {
        render(<ResumeForm isLoading={false} onSubmit={vi.fn()} />);

        expect(screen.getByLabelText(/Tell us about your target role/i)).toBeInTheDocument();
        expect(screen.getByText(/Upload your current resume/i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Submit for Review/i })).toBeInTheDocument();
    });

    it('disables button initially (no file)', () => {
        render(<ResumeForm isLoading={false} onSubmit={vi.fn()} />);
        const button = screen.getByRole('button', { name: /Submit for Review/i });
        expect(button).toBeDisabled();
    });

    it('disables button when loading', () => {
        render(<ResumeForm isLoading={true} onSubmit={vi.fn()} />);
        const button = screen.getByRole('button', { name: /Submit for Review/i });
        expect(button).toBeDisabled();
    });

    it('enables button after file upload', async () => {
        render(<ResumeForm isLoading={false} onSubmit={vi.fn()} />);

        const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' });
        const input = document.querySelector('input[type="file"]');

        if (input) {
            fireEvent.change(input, { target: { files: [file] } });
            const button = screen.getByRole('button', { name: /Submit for Review/i });
            expect(button).toBeEnabled();
        } else {
            throw new Error("File input not found");
        }
    });

    it('validates file size (>10MB)', () => {
        const alertMock = vi.spyOn(window, 'alert').mockImplementation(() => { });
        render(<ResumeForm isLoading={false} onSubmit={vi.fn()} />);

        // Create a file larger than 10MB
        const largeFile = new File([''], 'large.pdf', { type: 'application/pdf' });
        Object.defineProperty(largeFile, 'size', { value: 1024 * 1024 * 11 }); // 11MB

        const input = document.querySelector('input[type="file"]');
        if (input) {
            fireEvent.change(input, { target: { files: [largeFile] } });
            // Alert should be called
            expect(alertMock).toHaveBeenCalledWith("File too large. Max 10MB.");
            // Button should still be disabled as file wasn't set
            const button = screen.getByRole('button', { name: /Submit for Review/i });
            expect(button).toBeDisabled();
        }
        alertMock.mockRestore();
    });

    it('validates file type', () => {
        const alertMock = vi.spyOn(window, 'alert').mockImplementation(() => { });
        render(<ResumeForm isLoading={false} onSubmit={vi.fn()} />);

        const invalidFile = new File(['dummy'], 'test.txt', { type: 'text/plain' });

        const input = document.querySelector('input[type="file"]');
        if (input) {
            fireEvent.change(input, { target: { files: [invalidFile] } });
            expect(alertMock).toHaveBeenCalledWith("Invalid file type. Please upload PDF, DOC, or DOCX.");
            const button = screen.getByRole('button', { name: /Submit for Review/i });
            expect(button).toBeDisabled();
        }
        alertMock.mockRestore();
    });
});
