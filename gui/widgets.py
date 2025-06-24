# gui/widgets.py

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import pandas as pd

from gui.result_fetcher import (
    fetch_all_releases,
    fetch_test_results_by_release,
    insert_release,
)
from utils.chart_generator import generate_pie_chart
from utils.pdf_generator import generate_pdf_report
from utils.result_fetcher import fetch_all_test_cases, get_release_id_by_name
from utils.update_results import update_test_result


class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        label = tk.Label(
            self,
            text="Test Management",
            font=("Arial", 22, "bold"),
            bg=parent["bg"],
            fg="white",
        )
        label.pack(pady=10)


class ControlPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])

        self.releases = fetch_all_releases()
        self.selected_release = tk.StringVar()

        label = tk.Label(self, text="Select Release:", fg="white", bg=self["bg"])
        label.grid(row=0, column=0, padx=10, pady=5)

        self.dropdown = ttk.Combobox(
            self,
            textvariable=self.selected_release,
            values=self.releases,
            state="readonly",
            width=30,
        )
        self.dropdown.grid(row=0, column=1, padx=5)
        if self.releases:
            self.selected_release.set(self.releases[0])

        self.create_btn = ttk.Button(self, text="➕ Create Release", command=self.add_release)
        self.create_btn.grid(row=0, column=2, padx=10)

        self.generate_btn = ttk.Button(self, text="📄 Generate Report", command=self.generate_report)
        self.generate_btn.grid(row=0, column=3, padx=10)

        self.progress = ttk.Progressbar(self, mode="indeterminate", length=200)
        self.progress.grid(row=1, column=0, columnspan=4, pady=10)

    def add_release(self):
        win = tk.Toplevel(self)
        win.title("Create Release")
        win.geometry("400x200")
        win.config(bg="white")

        tk.Label(win, text="Release Name:").pack(pady=10)
        entry = tk.Entry(win, width=40)
        entry.pack(pady=5)

        def save():
            name = entry.get().strip()
            if name:
                insert_release(name)
                self.releases = fetch_all_releases()
                self.dropdown["values"] = self.releases
                self.selected_release.set(name)
                win.destroy()
            else:
                messagebox.showerror("Validation Error", "Release name cannot be empty")

        tk.Button(win, text="Save", command=save, bg="#4CAF50", fg="white").pack(pady=10)

    def generate_report(self):
        def task():
            self.progress.start()
            time.sleep(2)
            release = self.selected_release.get()
            df = fetch_test_results_by_release(release)
            generate_pie_chart(df)
            generate_pdf_report(df, chart_path="reports/charts/execution_summary.png")
            self.progress.stop()
            messagebox.showinfo("Done", "Report generated successfully!")

        threading.Thread(target=task).start()


class TestCaseViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])

        tk.Label(self, text="📋 Test Cases", font=("Arial", 14, "bold"), fg="white", bg=self["bg"]).pack(pady=10)

        columns = ("ID", "Name", "Product", "Module", "Status", "Executed By", "Date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor=tk.CENTER)
        self.tree.pack(fill="both", expand=True, padx=20)

        # Update section
        form = tk.Frame(self, bg=self["bg"])
        form.pack(pady=10)

        tk.Label(form, text="Status:", fg="white", bg=self["bg"]).grid(row=0, column=0)
        self.status_cb = ttk.Combobox(form, values=["Pass", "Fail", "Skipped", "Blocked", "Retest"])
        self.status_cb.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Release:", fg="white", bg=self["bg"]).grid(row=0, column=2)
        self.release_entry = ttk.Entry(form)
        self.release_entry.grid(row=0, column=3, padx=5)

        ttk.Button(form, text="Update Selected", command=self.update_selected).grid(row=0, column=4, padx=10)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = fetch_all_test_cases()
        for _, row in df.iterrows():
            self.tree.insert(
                "",
                "end",
                values=(
                    row["test_case_id"],
                    row["test_case_name"],
                    row["product_name"],
                    row["module_name"],
                    row.get("status", ""),
                    row.get("executed_by", ""),
                    row.get("execution_date", ""),
                ),
            )

    def update_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a test case.")
            return

        status = self.status_cb.get()
        release_name = self.release_entry.get()
        if not status or not release_name:
            messagebox.showerror("Input Error", "Please provide status and release.")
            return

        release_id = get_release_id_by_name(release_name)
        if not release_id:
            messagebox.showerror("Invalid Release", "Release not found.")
            return

        for item in selected:
            test_case_id = self.tree.item(item, "values")[0]
            update_test_result(test_case_id, release_id, status)

        messagebox.showinfo("Success", "Test results updated.")
        self.refresh()
