from fpdf import FPDF
import os

def safe(text):
    s = str(text)
    return (s.replace("—", "-")
              .replace("’", "'")
              .encode("latin1", "ignore")
              .decode("latin1"))

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "E2OPEN", border=False, ln=True, align="C")
        self.ln(5)

    def add_horizontal_line(self, y_position):
        self.set_draw_color(169, 169, 169)  # Light gray
        self.set_line_width(0.3)
        self.line(10, y_position, 200, y_position)

    def add_pie_chart(self, chart_path):
        # Add line above pie chart
        self.add_horizontal_line(self.get_y())

        if os.path.exists(chart_path):
            self.image(chart_path, x=30, w=150)  # Wider image for better spacing

        # Add line below pie chart
        self.add_horizontal_line(self.get_y() + 5)
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
            self.cell(col_widths[0], 8, safe(row["test_case_name"])[:25], 1)
            self.cell(col_widths[1], 8, safe(row["module_name"])[:30], 1)
            self.cell(col_widths[2], 8, safe(row["product_name"])[:20], 1)
            self.cell(col_widths[3], 8, safe(row["status"]), 1)
            self.cell(col_widths[4], 8, safe(row["executed_by"]), 1)
            self.ln()

def generate_pdf_report(df, chart_path, output_path="reports/pdfs/execution_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_pie_chart(chart_path)
    pdf.add_table(df.head(20))  # Show top 20 entries
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"[✓] PDF report generated at: {output_path}")
