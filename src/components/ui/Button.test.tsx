import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
    it('renders children correctly', () => {
        render(<Button>Click Me</Button>);
        expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    it('handles click events', () => {
        const handleClick = vi.fn();
        render(<Button onClick={handleClick}>Click Me</Button>);
        fireEvent.click(screen.getByText('Click Me'));
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('shows loading spinner when isLoading is true', () => {
        render(<Button isLoading={true}>Click Me</Button>);
        // Loader usually has an SVG or specific class. 
        // Our Button implementation uses Loader2 from lucide-react. 
        // We can check for the svg or simply strict disabled check as loading usually disables.
        expect(screen.getByRole('button')).toBeDisabled();
        // Lucide icons render svgs.
        expect(document.querySelector('svg')).toBeInTheDocument();
    });

    it('is disabled when disabled prop is true', () => {
        render(<Button disabled>Click Me</Button>);
        expect(screen.getByRole('button')).toBeDisabled();
    });

    it('applies variant classes', () => {
        render(<Button variant="secondary">Secondary</Button>);
        // Secondary variant uses 'bg-secondary' class
        expect(screen.getByRole('button')).toHaveClass('bg-secondary');
    });

    it('applies size classes', () => {
        render(<Button size="sm">Small</Button>);
        // Sm size uses 'px-3 py-1.5'
        expect(screen.getByRole('button')).toHaveClass('px-3');
    });
});
