# library
import customtkinter as ctk

# main class
from interface import UI

# pages
from ui_login import login_page

#create frame to add widgets to
# def front_page(app):
#     frame = ctk.CTkFrame(app)
#     frame.pack(padx=30, pady=20, fill="both", expand=True)

#     label1 = ctk.CTkLabel(frame, text="CodeVenture", font=("Helvetica Bold", 40))
#     label1.pack(padx=10, pady=50)

#     label2 = ctk.CTkLabel(frame, text="Welcome to CodeVenture, where your mom will pay us money to teach you coding!", font=("Helvetica", 18))
#     label2.pack(padx=10, pady=5)

#     button1 = ctk.CTkButton(frame, text="Login", font=("Helvetica", 14), width=120, height=50, command=lambda: login_page(frame))
#     button1.pack(padx=30, pady=70)

#     button2 = ctk.CTkButton(frame, text="Register", font=("Helvetica", 14), width=120, height=50, command=lambda: register_page(frame))
#     button2.pack(padx=30, pady=20)

if __name__ == "__main__":
    ui = UI()
    login_page(ui)
    ui.main.mainloop()