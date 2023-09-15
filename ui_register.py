import customtkinter as ctk
from App import App
import ui_window_gen as wingen

class RegisterWindow:

    def	FillFrames(self, attach: App):

        attach.main_frame.grid(
                    row=0,
                    column=0
                )

        label1 = ctk.CTkLabel(
        attach.main_frame,
        text="CodeVenture",
        font=("Helvetica Bold", 20)
        )

        label1.pack(
        padx=10,
        pady=10
        )

        label2 = ctk.CTkLabel(
            attach.main_frame,
            text="REGISTER",
            font=("Helvetica", 18)
        )

        label2.pack(
            padx=10,
            pady=5
        )

        username = ctk.CTkEntry(
            attach.main_frame,
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

        password = ctk.CTkEntry(
            attach.main_frame,
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

        confirm_password = ctk.CTkEntry(
            attach.main_frame,
            width=160,
            height=20,
            placeholder_text = "Confirm Password",
            show = "•" ,
            font=("Helvetica", 14)
        )

        confirm_password.pack(padx=10, pady=10)

        checkbox1 = ctk.CTkCheckBox(
            attach.main_frame,
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

        def registerButtonEvent():
            pass

        register_button = ctk.CTkButton(
            attach.main_frame,
            text="Register",
            font=("Helvetica", 14),
            width=120,
            height=50,
            command=lambda: exit()
        )
        register_button.pack(
                            padx=30,
                            pady=45
                            )
        
        def loginButtonEvent():
            wingen.loginPage(attach)

        login_button = ctk.CTkButton(
            attach.main_frame, 
            text="Already have an account? Login Instead!",
            font=("Helvetica", 14),
            width=120, height=50,
            command=lambda: loginButtonEvent()
        )
        
        login_button.pack(
            padx=30,
            pady=10
        )
