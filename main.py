from tkinter import Tk
from gui.widgets import Header, ReleaseSelector, ReportActions

def run_app():
    root = Tk()
    root.title("Test Management")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")

    Header(root).pack(pady=10)
    ReleaseSelector(root).pack(pady=10)
    ReportActions(root).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_app()
