declare module 'html2pdf.js' {
    interface Html2PdfOptions {
        margin?: number | [number, number, number, number];
        filename?: string;
        image?: { type: string; quality: number };
        enableLinks?: boolean;
        html2canvas?: any;
        jsPDF?: any;
    }

    interface Html2PdfWorker {
        from(element: HTMLElement): Html2PdfWorker;
        set(options: Html2PdfOptions): Html2PdfWorker;
        save(): Promise<void>;
        toPdf(): Html2PdfWorker;
        getPdf(callback: (pdf: any) => void): Html2PdfWorker;
    }

    function html2pdf(): Html2PdfWorker;
    function html2pdf(element: HTMLElement, options?: Html2PdfOptions): Html2PdfWorker;

    export default html2pdf;
}
