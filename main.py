# main.py

import tkinter as tk
from tkinter import ttk
from gui.widgets import Header, ControlPanel, TestCaseViewer

def run_app():
    root = tk.Tk()
    root.title("Test Management")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    Header(root).grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
    ttk.Separator(root, orient='horizontal').grid(row=1, column=0, sticky="ew", padx=10)
    ControlPanel(root).grid(row=2, column=0, sticky="ew", padx=10, pady=(10, 10))
    TestCaseViewer(root).grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    run_app()
