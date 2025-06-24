from utils.result_fetcher import fetch_test_results
from utils.chart_generator import generate_pie_chart
from utils.pdf_generator import generate_pdf_report
from gui.main_window import launch_gui


def main():
    mode = input("Enter mode (gui/cli): ").strip().lower()

    if mode == "gui":
        launch_gui()
    else:
        print("[*] CLI Mode: Generating report...")
        df = fetch_test_results()
        chart_path = "reports/charts/execution_summary.png"
        generate_pie_chart(df, output_dir="reports/charts")
        generate_pdf_report(df, chart_path)


if __name__ == "__main__":
    main()
