import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Select } from './Select';

describe('Select', () => {
    const options = [
        { label: 'Option 1', value: 'opt1' },
        { label: 'Option 2', value: 'opt2' }
    ];

    it('renders label correctly', () => {
        render(<Select id="sel-lbl" name="test" label="Select Label" options={options} />);
        expect(screen.getByLabelText('Select Label')).toBeInTheDocument();
    });

    it('renders parameters as options', () => {
        render(<Select id="sel-opt" name="test" label="Select" options={options} />);
        expect(screen.getByRole('option', { name: 'Option 1' })).toBeInTheDocument();
        expect(screen.getByRole('option', { name: 'Option 2' })).toBeInTheDocument();
    });

    it('handles selection change', () => {
        const handleChange = vi.fn();
        render(<Select id="sel-chg" name="test" label="Select" options={options} onChange={handleChange} />);

        const select = screen.getByLabelText('Select');
        fireEvent.change(select, { target: { value: 'opt2' } });

        expect(handleChange).toHaveBeenCalled();
        expect(select).toHaveValue('opt2');
    });
});
