from tkinter import Tk, Frame
from gui.widgets import Header, ReleaseSelector, ReportActions, TestCaseViewer


def run_app():
    root = Tk()
    root.title("Test Management")
    root.geometry("1100x700")
    root.configure(bg="#1e1e1e")  # Start in dark mode

    # Theme toggle handler
    def toggle_theme():
        current_bg = root["bg"]
        new_bg = "white" if current_bg == "#1e1e1e" else "#1e1e1e"
        fg = "black" if new_bg == "white" else "white"

        root.configure(bg=new_bg)
        for widget in root.winfo_children():
            if hasattr(widget, "configure"):
                widget.configure(bg=new_bg)
                for sub in widget.winfo_children():
                    if hasattr(sub, "configure"):
                        if isinstance(sub, (Frame,)):
                            sub.configure(bg=new_bg)
                        elif hasattr(sub, "cget") and sub.cget("fg"):
                            sub.configure(bg=new_bg, fg=fg)

    # Pass the toggle_theme function to Header
    Header(root, toggle_theme_callback=toggle_theme).pack(pady=10, fill="x")

    # Rest of the layout
    ReleaseSelector(root).pack(pady=10, fill="x")
    ReportActions(root).pack(pady=20, fill="x")

    main_frame = Frame(root, bg=root["bg"])
    main_frame.pack(fill="both", expand=True)

    TestCaseViewer(main_frame).pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    run_app()
