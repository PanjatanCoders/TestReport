import matplotlib.pyplot as plt
import os

def generate_pie_chart(df, output_dir="reports/charts"):
    status_counts = df['status'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Test Execution Summary")
    os.makedirs(output_dir, exist_ok=True)
    chart_path = os.path.join(output_dir, "execution_summary.png")
    plt.savefig(chart_path)
    plt.show()
    print(f"[✓] Pie chart saved to: {chart_path}")
