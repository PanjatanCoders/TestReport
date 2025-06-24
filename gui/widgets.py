import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os

from gui.result_fetcher import fetch_all_releases, fetch_test_results_by_release
from utils.chart_generator import generate_pie_chart
from utils.pdf_generator import generate_pdf_report


class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        label = tk.Label(self, text="Test Management", font=("Arial", 22, "bold"), fg="white", bg=self["bg"])
        label.pack()


class ReleaseSelector(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        self.releases = fetch_all_releases()
        self.selected_release = tk.StringVar()

        label = tk.Label(self, text="Select Release:", fg="white", bg=self["bg"])
        label.grid(row=0, column=0, padx=10)

        self.dropdown = ttk.Combobox(self, textvariable=self.selected_release, values=self.releases, state="readonly")
        self.dropdown.grid(row=0, column=1)
        if self.releases:
            self.selected_release.set(self.releases[0])

        self.add_btn = tk.Button(self, text="+ Create Release", command=self.add_release)
        self.add_btn.grid(row=0, column=2, padx=10)

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
        win.geometry("400x200")  # Enlarged window
        win.configure(bg="white")

        tk.Label(win, text="Release Name:", bg="white", font=("Arial", 11)).pack(pady=10)
        entry = tk.Entry(win, font=("Arial", 11))
        entry.pack(pady=5, ipadx=10)
        tk.Button(win, text="Save", command=save, font=("Arial", 10)).pack(pady=10)


class ReportActions(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        self.parent = parent

        self.dark_mode = tk.BooleanVar(value=True)

        self.generate_btn = tk.Button(self, text="Generate Report", command=self.run_report)
        self.generate_btn.grid(row=0, column=0, padx=10)

        self.toggle_dark = tk.Checkbutton(self, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme)
        self.toggle_dark.grid(row=0, column=1, padx=10)

    def run_report(self):
        progress = ttk.Progressbar(self, mode="indeterminate", length=200)
        progress.grid(row=1, column=0, columnspan=2, pady=10)
        progress.start()

        def task():
            time.sleep(2)  # Simulated delay
            release = self.master.children['!releaseselector'].selected_release.get()
            df = fetch_test_results_by_release(release)
            generate_pie_chart(df)
            generate_pdf_report(df, chart_path="reports/charts/execution_summary.png")
            progress.stop()
            progress.destroy()
            messagebox.showinfo("Done", "Report generated successfully!")

        threading.Thread(target=task).start()

    def toggle_theme(self):
        bg = "#1e1e1e" if self.dark_mode.get() else "white"
        fg = "white" if self.dark_mode.get() else "black"
        self.parent.configure(bg=bg)
        for child in self.parent.winfo_children():
            if hasattr(child, "configure"):
                child.configure(bg=bg)
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.configure(bg=bg, fg=fg)
                    elif isinstance(sub, tk.Frame):
                        sub.configure(bg=bg)
