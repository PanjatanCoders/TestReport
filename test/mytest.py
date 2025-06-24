import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("300x150")

def on_click():
    print("Button clicked!")

button = customtkinter.CTkButton(app, text="Modern Button", command=on_click)
button.pack(pady=40)

app.mainloop()