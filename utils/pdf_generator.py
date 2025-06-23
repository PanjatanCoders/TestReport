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
        page_width = self.w - 20  # full width minus margins
        col_widths = [0.20, 0.25, 0.20, 0.15, 0.20]
        col_widths = [page_width * w for w in col_widths]

        headers = ["Test Case", "Module", "Product", "Status", "Executed By"]

        status_colors = {
            "Pass": (144, 238, 144),
            "Fail": (255, 99, 71),
            "Skipped": (255, 215, 0),
            "Blocked": (211, 211, 211),
            "Retest": (173, 216, 230),
        }

        grouped = df.groupby("module_name")

        for module_name, group in grouped:
            # Add page if not enough space for section heading
            if self.get_y() + 20 > self.page_break_trigger:
                self.add_page()

            # 📌 Section Header (no emoji)
            self.set_font("Arial", "BU", 11)
            self.cell(0, 10, f"Module: {safe(module_name)}", ln=True)

            # Table Header
            self.set_font("Arial", "B", 10)
            for i, header in enumerate(headers):
                self.cell(col_widths[i], 8, header, border='B', ln=0, align="C")
            self.ln()
            self.set_font("Arial", "", 9)

            for _, row in group.iterrows():
                cell_data = [
                    safe(row["test_case_name"]),
                    safe(row["module_name"]),
                    safe(row["product_name"]),
                    safe(row["status"]),
                    safe(row["executed_by"]),
                ]

                # Estimate row height (wrap handling)
                line_counts = [
                    len(self.multi_cell(col_widths[i], 4, text, border=0, align='L', split_only=True))
                    for i, text in enumerate(cell_data)
                ]
                row_height = max(6, max(line_counts) * 4)

                # Page break if needed
                if self.get_y() + row_height + 6 > self.page_break_trigger:
                    self.add_page()
                    # Repeat module header and table header
                    self.set_font("Arial", "BU", 11)
                    self.cell(0, 10, f"Module: {safe(module_name)}", ln=True)
                    self.set_font("Arial", "B", 10)
                    for i, header in enumerate(headers):
                        self.cell(col_widths[i], 8, header, border='B', ln=0, align="C")
                    self.ln()
                    self.set_font("Arial", "", 9)

                x_start = self.get_x()
                y_start = self.get_y()

                # Print each cell
                for i in range(len(cell_data)):
                    self.set_xy(x_start + sum(col_widths[:i]), y_start)

                    if headers[i] == "Status":
                        color = status_colors.get(cell_data[i], (255, 255, 255))
                        self.set_fill_color(*color)
                        self.multi_cell(col_widths[i], 4, cell_data[i], border=0, align='L', fill=True)
                    else:
                        self.multi_cell(col_widths[i], 4, cell_data[i], border=0, align='L')

                # Add bottom line under the row
                self.set_xy(x_start, y_start + row_height)
                self.set_draw_color(200, 200, 200)
                self.line(x_start, self.get_y(), x_start + sum(col_widths), self.get_y())

                self.ln(3)  # Add spacing between rows


def generate_pdf_report(df, chart_path, output_path="reports/pdfs/execution_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_pie_chart(chart_path)
    pdf.add_table(df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"[✓] PDF report generated at: {output_path}")
