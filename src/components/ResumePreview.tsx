import { forwardRef } from 'react';
import Markdown from 'react-markdown';

interface ResumePreviewProps {
    content: string;
}

export const ResumePreview = forwardRef<HTMLDivElement, ResumePreviewProps>(({ content }, ref) => {
    return (
        <div ref={ref} className="bg-white text-black p-[50px] max-w-[800px] mx-auto min-h-[1100px] shadow-lg print:shadow-none print:m-0 print:p-[40px] font-sans">
            <style>
                {`
                    @page { size: auto; margin: 0mm; }
                    @media print {
                         body { -webkit-print-color-adjust: exact; }
                    }
                    /* Center the subtitle (first P after H1) */
                    h1 + p {
                        text-align: center;
                        margin-bottom: 1.5rem;
                    }
                `}
            </style>
            <div className="prose pro max-w-none prose-headings:text-black prose-p:text-black prose-li:text-black">
                <Markdown
                    components={{
                        h1: ({ node, ...props }) => <h1 className="text-3xl font-bold text-center uppercase mb-2 border-b-0" {...props} />,
                        h2: ({ node, ...props }) => <h2 className="text-lg font-bold uppercase border-b-2 border-black mb-2 mt-4 pb-1" {...props} />,
                        h3: ({ node, ...props }) => <h3 className="text-md font-bold mt-2 mb-1" {...props} />,
                        p: ({ node, ...props }) => <p className="mb-2 text-sm leading-relaxed" {...props} />,
                        ul: ({ node, ...props }) => <ul className="list-disc ml-5 mb-2 text-sm space-y-0.5" {...props} />,
                        li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                        strong: ({ node, ...props }) => <strong className="font-bold text-black" {...props} />,
                        hr: ({ node, ...props }) => <hr className="border-black my-4" {...props} />
                    }}
                >
                    {content}
                </Markdown>
            </div>
        </div>
    );
});

ResumePreview.displayName = 'ResumePreview';
