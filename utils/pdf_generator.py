from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Test Execution Report", border=False, ln=True, align="C")
        self.ln(5)

    def add_pie_chart(self, chart_path):
        if os.path.exists(chart_path):
            self.image(chart_path, x=50, w=100)
            self.ln(10)

    def add_table(self, df):
        self.set_font("Arial", "B", 10)
        col_widths = [30, 45, 30, 25, 25]
        headers = ["Test Case", "Module", "Product", "Status", "Executed By"]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, "C")
        self.ln()

        self.set_font("Arial", "", 9)
        for _, row in df.iterrows():
            self.cell(col_widths[0], 8, str(row["test_case_name"])[:25], 1)
            self.cell(col_widths[1], 8, str(row["module_name"])[:30], 1)
            self.cell(col_widths[2], 8, str(row["product_name"])[:20], 1)
            self.cell(col_widths[3], 8, str(row["status"]), 1)
            self.cell(col_widths[4], 8, str(row["executed_by"]), 1)
            self.ln()

def generate_pdf_report(df, chart_path, output_path="reports/pdfs/execution_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_pie_chart(chart_path)
    pdf.add_table(df.head(20))  # Show top 20 entries
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"[✓] PDF report generated at: {output_path}")
