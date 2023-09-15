import customtkinter as ctk
from App import App
from user.user_base import User

class LoginWindow():

    def __init__(self):
        self.username = None
        self.password = None
        self.user = User(None)

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def	FillFrames(self, attach: App):

        attach.main_frame.grid(
            row=0,
            column=0
        )

        label1 = ctk.CTkLabel(
            attach.main_frame,
            text="CodeVenture",
            font=("Helvetica Bold", 30)
            )

        label1.pack(
            padx=10,
            pady=10
            )

        label2 = ctk.CTkLabel(
            attach.main_frame,
            text="LOGIN",
            font=("Helvetica", 18, "bold")
            )
        
        label2.pack(
                padx=10,
                pady=20
                )

        username1 = ctk.CTkEntry(
            attach.main_frame,
            width=160,
            height=20,
            placeholder_text="Username", 
            font=("Helvetica", 14)
            )

        username1.pack(
                    padx=10,
                    pady=10
                    )

        password1 = ctk.CTkEntry(
            attach.main_frame,
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

        def eventShowPassword():
            if checkbox1_status.get() == 1:
                password1.configure(show="")
            else:
                password1.configure(show="•")
            password1.update()

        checkbox1 = ctk.CTkCheckBox(
            attach.main_frame,
            text="Show password",
            font=("Helvetica", 14),
            variable=checkbox1_status,
            onvalue=1,
            offvalue=0,
            command= lambda: eventShowPassword()
            )

        checkbox1.pack(
            padx=10,
            pady=20
            )

        def loginButtonEvent():
            """
            Handles login event when button is pressed
            """
            self.username = username1.get()
            self.user.setUsername(self.username)
            if self.user.login(password1.get()) == True:
                print(f"Logged in {self.username}")

                import ui_window_gen as wingen
                from user.user_student import Student

                match self.user.getUserType():
                    
                    case "student":
                        wingen.studentMenuPage(attach, Student(self.user.getUsername()))
                    case "educator":
                        return
                    case "admin":
                        return
                    case _:
                        raise AssertionError("Unknown user type")
            
            else:
                pass
                print("Login failed, Incorrect username or password")
                # show login failed

        login_button = ctk.CTkButton(
            attach.main_frame,
            text="Login",
            font=("Helvetica", 14),
            width=120,
            height=50,
            command=lambda: loginButtonEvent()
            )

        login_button.pack(
            padx=30,
            pady=45
            )

        def registerButtonEvent():
            exit()


        register_button = ctk.CTkButton(
            attach.main_frame,
            text="Register",
            font=("Helvetica", 14),
            width=120, height=50,
            command=lambda: registerButtonEvent()
            )

        register_button.pack(
            padx=30,
            pady=5
            )

if __name__ == "__main__":
    test = App()
    l = LoginWindow()
    l.FillFrames(test)
    test.mainloop()
