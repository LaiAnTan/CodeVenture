import customtkinter as ctk

def register_page(frame):
    frame.pack_forget()

    def register_debug():
        print("Username: " + username2.get())
        print("Password: " + password2.get())
        print("Confirm Password: " + password2_2.get())
        print("end debug\n")

    frame.pack(padx=30, pady=20, fill="both", expand=True)

    label1 = ctk.CTkLabel(frame, text="CodeVenture", font=("Helvetica Bold", 20))
    label1.pack(padx=10, pady=10)

    label2 = ctk.CTkLabel(frame, text="Register Menu", font=("Helvetica", 18))
    label2.pack(padx=10, pady=5)

    username2 = ctk.CTkEntry(frame, width=160, height=20, placeholder_text = "New Username", font=("Helvetica", 14))
    username2.pack(padx=10, pady=10)

    password2 = ctk.CTkEntry(frame, width=160, height=20, placeholder_text = "New Password",show = "•" ,font=("Helvetica", 14))
    password2.pack(padx=10, pady=10)

    password2_2 = ctk.CTkEntry(frame, width=160, height=20, placeholder_text = "Confirm Password",show = "•" ,font=("Helvetica", 14))
    password2_2.pack(padx=10, pady=10)

    register_button = ctk.CTkButton(frame, text="Register", font=("Helvetica", 14), width=120, height=50, command=register_debug)
    register_button.pack(padx=30, pady=45)

    login_button = ctk.CTkButton(frame, text="Already have an account? Login Instead!", font=("Helvetica", 14), width=120, height=50, command=lambda: login_page(frame))
    login_button.pack(padx=30, pady=10)
