import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Input } from './Input';

describe('Input', () => {
    it('renders with label', () => {
        render(<Input id="test-lbl" name="test" label="Test Label" />);
        expect(screen.getByLabelText('Test Label')).toBeInTheDocument();
    });

    it('handles text input', () => {
        const handleChange = vi.fn();
        render(<Input id="test-chg" name="test" label="Test" onChange={handleChange} />);

        const input = screen.getByLabelText('Test');
        fireEvent.change(input, { target: { value: 'Hello' } });

        expect(handleChange).toHaveBeenCalled();
        expect(input).toHaveValue('Hello');
    });

    it('renders required asterisk if required', () => {
        render(<Input id="test-req" name="test" label="Test" required />);
        expect(screen.getByLabelText('Test')).toBeRequired();
    });

    it('handles placeholder', () => {
        render(<Input name="test" placeholder="Enter text" />);
        expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
    });
});
