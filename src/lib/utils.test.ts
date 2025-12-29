import { describe, it, expect } from 'vitest';
import { cn } from './utils';

describe('cn utility', () => {
    it('merges class names', () => {
        expect(cn('class1', 'class2')).toBe('class1 class2');
    });

    it('handles conditional classes', () => {
        expect(cn('class1', true && 'class2', false && 'class3')).toBe('class1 class2');
    });

    it('merges tailwind classes (overrides)', () => {
        // Assuming twMerge is used
        expect(cn('p-2', 'p-4')).toBe('p-4');
        expect(cn('text-red-500', 'text-blue-500')).toBe('text-blue-500');
    });

    it('handles arrays and objects if supported', () => {
        expect(cn(['a', 'b'])).toBe('a b');
    });
});
