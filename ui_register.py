# library
import customtkinter as ctk

# main class
from interface import UI

# pages
from ui_login import login_page

from ui_loading import loading_page

def register_page(ui: UI):

    ui.frame.destroy()
    ui.frame = ctk.CTkFrame(ui.main)

    # def register_debug():
    #     print("Username: " + username.get())
    #     print("Password: " + password.get())
    #     print("Confirm Password: " + confirm_password.get())
    #     print("end debug\n")

    ui.frame.pack(
                padx=30,
                pady=20,
                fill="both",
                expand=True
                )

    label1 = ctk.CTkLabel(ui.frame,
                        text="CodeVenture",
                        font=("Helvetica Bold", 20)
                        )
    label1.pack(
            padx=10,
            pady=10
            )

    label2 = ctk.CTkLabel(ui.frame,
                text="REGISTER",
                font=("Helvetica", 18)
                )
    label2.pack(
            padx=10,
            pady=5
            )

    username = ctk.CTkEntry(ui.frame,
                        width=160,
                        height=20,
                        placeholder_text = "New Username",
                        font=("Helvetica", 14)
                        )
    username.pack(
                padx=10,
                pady=10
                )
    
    checkbox1_status = ctk.IntVar(value=0)
    def show_password():
        print(checkbox1_status.get())
        if checkbox1_status.get() == 1:
            password.configure(show="")
            confirm_password.configure(show="")
        else:
            password.configure(show="•")
            confirm_password.configure(show="•")
        password.update()
        confirm_password.update()

    password = ctk.CTkEntry(ui.frame,
                        width=160,
                        height=20,
                        placeholder_text = "New Password",
                        show = "•" ,
                        font=("Helvetica", 14)
                        )
    password.pack(
                padx=10,
                pady=10
                )

    confirm_password = ctk.CTkEntry(ui.frame,
                            width=160,
                            height=20,
                            placeholder_text = "Confirm Password",
                            show = "•" ,
                            font=("Helvetica", 14)
                            )
    confirm_password.pack(padx=10, pady=10)

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

    register_button = ctk.CTkButton(ui.frame,
                                text="Register",
                                font=("Helvetica", 14),
                                width=120,
                                height=50,
                                command=lambda: loading_page(ui)
                                )
    register_button.pack(
                        padx=30,
                        pady=45
                        )
    

    login_button = ctk.CTkButton(ui.frame, 
                                text="Already have an account? Login Instead!",
                                font=("Helvetica", 14),
                                width=120, height=50,
                                command=lambda: login_page(ui)
                                )
    
    login_button.pack(
                    padx=30,
                    pady=10
                    )
