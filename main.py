from utils.pdf_generator import generate_pdf_report
from utils.result_fetcher import fetch_test_results
from utils.chart_generator import generate_pie_chart


def main():
    print("[*] Fetching test results...")
    df = fetch_test_results()
    print("[*] Generating pie chart...")
    chart_path = "reports/charts/execution_summary.png"
    generate_pie_chart(df, output_dir="reports/charts")

    print("[*] Generating PDF report...")
    generate_pdf_report(df, chart_path)


if __name__ == "__main__":
    main()
