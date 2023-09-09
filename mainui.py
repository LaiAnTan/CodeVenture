import customtkinter as ctk

#initiate window
app = ctk.CTk()

#set basic appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

#set window title and size
app.title("CodeVenture - Development Environment")
app.minsize(900, 600)

def login_page():
    global frame
    frame.pack_forget()
    remember_status = ctk.StringVar(value="False")
    
    def login_debug():
        print("Username: " + username1.get())
        print("Password: " + password1.get())
        print("Remember: " + remember_status.get())
        print("end debug\n")

    frame = ctk.CTkFrame(app)
    frame.pack(padx=30, pady=20, fill="both", expand=True)

    label1 = ctk.CTkLabel(frame, text="CodeVenture", font=("Helvetica Bold", 30))
    label1.pack(padx=10, pady=10)

    label2 = ctk.CTkLabel(frame, text="Login Menu", font=("Helvetica", 18))
    label2.pack(padx=10, pady=20)

    username1 = ctk.CTkEntry(frame, width=160, height=20, placeholder_text="Username", font=("Helvetica", 14))
    username1.pack(padx=10, pady=10)

    password1 = ctk.CTkEntry(frame, width=160, height=20, placeholder_text="Password",show = "•" ,font=("Helvetica", 14))
    password1.pack(padx=10, pady=10)

    checkbox1 = ctk.CTkCheckBox(frame, text="Remember who asked?", font=("Helvetica", 14), variable=remember_status, onvalue="True", offvalue="False")
    checkbox1.pack(padx=10, pady=20)

    login_button = ctk.CTkButton(frame, text="Login", font=("Helvetica", 14), width=120, height=50, command=login_debug)
    login_button.pack(padx=30, pady=45)

    register_button = ctk.CTkButton(frame, text="No account? Register Instead!", font=("Helvetica", 14), width=120, height=50, command=register_page)
    register_button.pack(padx=30, pady=5)

def register_page():
    global frame
    frame.pack_forget()

    def register_debug():
        print("Username: " + username2.get())
        print("Password: " + password2.get())
        print("Confirm Password: " + password2_2.get())
        print("end debug\n")

    frame = ctk.CTkFrame(app)
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

    login_button = ctk.CTkButton(frame, text="Already have an account? Login Instead!", font=("Helvetica", 14), width=120, height=50, command=login_page)
    login_button.pack(padx=30, pady=10)

#create frame to add widgets to
global frame
frame = ctk.CTkFrame(app)
frame.pack(padx=30, pady=20, fill="both", expand=True)

label1 = ctk.CTkLabel(frame, text="CodeVenture", font=("Helvetica Bold", 40))
label1.pack(padx=10, pady=50)

label2 = ctk.CTkLabel(frame, text="Welcome to CodeVenture, where your mom will pay us money to teach you coding!", font=("Helvetica", 18))
label2.pack(padx=10, pady=5)

button1 = ctk.CTkButton(frame, text="Login", font=("Helvetica", 14), width=120, height=50, command=login_page)
button1.pack(padx=30, pady=70)

button2 = ctk.CTkButton(frame, text="Register", font=("Helvetica", 14), width=120, height=50, command=register_page)
button2.pack(padx=30, pady=20)

app.mainloop()