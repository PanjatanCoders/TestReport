import tkinter as tk
from tkinter import ttk, messagebox

from gui.result_fetcher import fetch_test_results_by_release, get_db_connection
from utils.chart_generator import generate_pie_chart
from utils.pdf_generator import generate_pdf_report
import threading
import os

def run_gui():
    def generate_report():
        release_name = release_var.get()
        if not release_name:
            messagebox.showerror("Input Error", "Please select a release name.")
            return

        def task():
            try:
                status_label.config(text="Generating report...", foreground="blue")
                df = fetch_test_results_by_release(release_name)
                if df.empty:
                    status_label.config(text="No data found for the selected release.", foreground="red")
                    return

                chart_dir = "reports/charts"
                chart_path = os.path.join(chart_dir, "execution_summary.png")
                generate_pie_chart(df, output_dir=chart_dir)
                generate_pdf_report(df, chart_path)

                status_label.config(text="✔ Report generated successfully!", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                status_label.config(text="Failed to generate report.", foreground="red")

        threading.Thread(target=task).start()

    # ----- UI Starts Here -----
    root = tk.Tk()
    root.title("Test Management Dashboard")
    root.geometry("600x400")
    root.configure(bg="#f0f4f8")

    header = tk.Label(root, text="⚙️ Test Management", font=("Segoe UI", 20, "bold"), bg="#f0f4f8", fg="#34495e")
    header.pack(pady=20)

    frame = tk.Frame(root, bg="#f0f4f8")
    frame.pack(pady=10)

    release_label = tk.Label(frame, text="Select Release:", font=("Segoe UI", 12), bg="#f0f4f8", fg="#2c3e50")
    release_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    release_var = tk.StringVar()
    release_dropdown = ttk.Combobox(frame, textvariable=release_var, font=("Segoe UI", 11), width=30)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT release_name FROM releases ORDER BY release_date DESC")
    releases = [row[0] for row in cursor.fetchall()]
    release_dropdown['values'] = releases
    release_dropdown.grid(row=0, column=1, padx=10, pady=5)

    generate_btn = tk.Button(
        root, text="✍️ Generate Report", font=("Segoe UI", 12, "bold"), bg="#2980b9", fg="white",
        padx=20, pady=10, bd=0, relief="ridge", command=generate_report, activebackground="#3498db"
    )
    generate_btn.pack(pady=15)

    status_label = tk.Label(root, text="", font=("Segoe UI", 11), bg="#f0f4f8")
    status_label.pack(pady=10)

    root.mainloop()
