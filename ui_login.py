import customtkinter as ctk
from interface import UI

def login_page(ui: UI):
    ui.frame.pack_forget()

    def login_debug():
        print("Username: " + username1.get())
        print("Password: " + password1.get())

    ui.frame.pack(
                padx=30,
                pady=20,
                fill="both",
                expand=True
                )

    label1 = ctk.CTkLabel(ui.frame,
                        text="CodeVenture",
                        font=("Helvetica Bold", 30)
                        )
    label1.pack(
            padx=10,
            pady=10
            )

    label2 = ctk.CTkLabel(ui.frame,
                        text="LOGIN",
                        font=("Helvetica", 18, "bold")
                        )
    label2.pack(
            padx=10,
            pady=20
            )

    username1 = ctk.CTkEntry(ui.frame,
                            width=160,
                            height=20,
                            placeholder_text="Username", 
                            font=("Helvetica", 14)
                            )
    username1.pack(
                padx=10,
                pady=10
                )

    password1 = ctk.CTkEntry(ui.frame,
                            width=160,
                            height=20,
                            placeholder_text="Password",
                            show="•",
                            font=("Helvetica", 14)
                            )
    password1.pack(
                padx=10,
                pady=10
                )

    checkbox1_status = ctk.IntVar(value=0)
    def show_password():
        print(checkbox1_status.get())
        if checkbox1_status.get() == 1:
            password1.configure(show="")
        else:
            password1.configure(show="•")
        password1.update()

    checkbox1 = ctk.CTkCheckBox(ui.frame,
                            text="Show password",
                            font=("Helvetica", 14),
                            variable=checkbox1_status,
                            onvalue=1,
                            offvalue=0,
                            command= lambda: show_password()
                            )
    checkbox1.pack(
                padx=10,
                pady=20
                )

    login_button = ctk.CTkButton(ui.frame,
                                text="Login",
                                font=("Helvetica", 14),
                                width=120,
                                height=50,
                                command=login_debug
                                )
    login_button.pack(
                    padx=30,
                    pady=45
                    )

    register_button = ctk.CTkButton(ui.frame,
                                text="Register",
                                font=("Helvetica", 14),
                                width=120, height=50,
                                command=lambda: register_page(ui)
                                )
    register_button.pack(
                    padx=30,
                    pady=5
                    )