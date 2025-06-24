# gui/widgets.py (Updated with dark/light mode icon, view tests, and update results)

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
from PIL import Image, ImageTk

from gui.result_fetcher import fetch_all_releases, fetch_test_results_by_release
from utils.chart_generator import generate_pie_chart
from utils.pdf_generator import generate_pdf_report
from utils.result_fetcher import fetch_all_test_cases, get_release_id_by_name
from utils.update_results import update_test_result


class Header(tk.Frame):
    def __init__(self, parent, toggle_theme_callback):
        super().__init__(parent, bg=parent["bg"])
        self.parent = parent

        title = tk.Label(self, text="Test Management", font=("Arial", 22, "bold"), fg="white", bg=self["bg"])
        title.pack(side=tk.LEFT, padx=10)

        # Theme toggle icon button (top right)
        self.theme_icon = ImageTk.PhotoImage(Image.open("assets/moon.png").resize((24, 24)))
        self.theme_btn = tk.Button(self, image=self.theme_icon, command=toggle_theme_callback, bd=0, bg=self["bg"])
        self.theme_btn.pack(side=tk.RIGHT, padx=10)


class ReleaseSelector(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        self.releases = fetch_all_releases()
        self.selected_release = tk.StringVar()

        tk.Label(self, text="Select Release:", fg="white", bg=self["bg"]).grid(row=0, column=0, padx=10)
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_release, values=self.releases, state="readonly")
        self.dropdown.grid(row=0, column=1)
        if self.releases:
            self.selected_release.set(self.releases[0])

        tk.Button(self, text="+ Create Release", command=self.add_release).grid(row=0, column=2, padx=10)

    def add_release(self):
        def save():
            name = entry.get()
            if name:
                from utils.result_fetcher import insert_release
                insert_release(name)
                self.releases = fetch_all_releases()
                self.dropdown["values"] = self.releases
                self.selected_release.set(name)
                win.destroy()

        win = tk.Toplevel(self)
        win.title("Create Release")
        win.geometry("400x200")
        tk.Label(win, text="Release Name:").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)
        tk.Button(win, text="Save", command=save).pack(pady=5)


class ReportActions(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        self.parent = parent

        tk.Button(self, text="Generate Report", command=self.run_report).pack(pady=10)

    def run_report(self):
        progress = ttk.Progressbar(self, mode="indeterminate", length=250)
        progress.pack(pady=5)
        progress.start()

        def task():
            time.sleep(2)
            release = self.master.children['!releaseselector'].selected_release.get()
            df = fetch_test_results_by_release(release)
            generate_pie_chart(df)
            generate_pdf_report(df, chart_path="reports/charts/execution_summary.png")
            progress.stop()
            progress.destroy()
            messagebox.showinfo("Done", "Report generated successfully!")

        threading.Thread(target=task).start()


class TestCaseViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])

        self.label = tk.Label(self, text="Test Case List", font=("Arial", 14, "bold"), fg="white", bg=self["bg"])
        self.label.pack(pady=10)

        columns = ("ID", "Name", "Product", "Module", "Status", "Date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=20)

        self.update_frame = tk.Frame(self, bg=self["bg"])
        self.update_frame.pack(pady=10)

        tk.Label(self.update_frame, text="Status:", fg="white", bg=self["bg"]).grid(row=0, column=0)
        self.status = ttk.Combobox(self.update_frame, values=["Pass", "Fail", "Skipped", "Blocked", "Retest"])
        self.status.grid(row=0, column=1, padx=5)

        tk.Label(self.update_frame, text="Release:", fg="white", bg=self["bg"]).grid(row=0, column=2)
        self.release_entry = ttk.Entry(self.update_frame)
        self.release_entry.grid(row=0, column=3, padx=5)

        tk.Button(self.update_frame, text="Update Selected", command=self.update_selected).grid(row=0, column=4, padx=10)

        self.refresh()

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df = fetch_all_test_cases()
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row["test_case_id"], row["test_case_name"], row["product_name"], row["module_name"], row["status"], row["execution_date"]))

    def update_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a test case to update.")
            return

        status = self.status.get()
        release_name = self.release_entry.get()
        if not status or not release_name:
            messagebox.showerror("Missing Fields", "Please provide both status and release.")
            return

        release_id = get_release_id_by_name(release_name)
        if release_id is None:
            messagebox.showerror("Invalid Release", "Release not found. Please create the release first.")
            return

        for item in selected:
            test_case_id = self.tree.item(item, "values")[0]
            update_test_result(test_case_id, release_id, status)

        messagebox.showinfo("Success", "Test result(s) updated successfully!")
        self.refresh()
