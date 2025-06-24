# main.py

import tkinter as tk
from gui.widgets import Header, ControlPanel, TestCaseViewer


def run_app():
    root = tk.Tk()
    root.title("Test Management")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")

    Header(root).pack(pady=5, fill="x")
    ControlPanel(root).pack(pady=10)
    TestCaseViewer(root).pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_app()
