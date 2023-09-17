import customtkinter as ctk

from App import App

from ui_window_gen import registerPage, studentMenuPage, subscribePage

from ui_window_gen import studentMenuPage, registerPage, studentProfileSetupPage
from user.user_base import User
from user.user_student import Student

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

        full_width = 450
        half_width = full_width / 2

        # title frame

        title_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=40,
            fg_color="transparent"
        )

        title_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        title_frame.rowconfigure((0,1), weight=1)
        title_frame.columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            title_frame,
            text="CodeVenture",
            font=("Helvetica Bold", 30),
            anchor=ctk.CENTER,
        )

        title_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky=""
        )

        login_label = ctk.CTkLabel(
            title_frame,
            text="LOGIN",
            font=("Helvetica", 18, "bold"),
            justify=ctk.CENTER,
        )
        
        login_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=20,
            sticky=""
        )
        
        # entry frame

        entry_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=100,
            fg_color="transparent"
        )

        entry_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        entry_frame.rowconfigure((0, 1, 2), weight=1)
        entry_frame.columnconfigure(0, weight=1)

        username1 = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Username", 
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        username1.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        password1 = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Password",
            show="•",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        password1.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        # show password checkbox

        checkbox1_status = ctk.IntVar(value=0)

        def eventShowPassword():
            if checkbox1_status.get() == 1:
                password1.configure(show="")
            else:
                password1.configure(show="•")
            password1.update()

        checkbox1 = ctk.CTkCheckBox(
            entry_frame,
            text="Show password",
            font=("Helvetica", 14),
            variable=checkbox1_status,
            onvalue=1,
            offvalue=0,
            command= lambda: eventShowPassword()
        )

        checkbox1.grid(
            row=2,
            column=0,
            padx=10,
            pady=20
        )

        wrong_password_label = ctk.CTkLabel(
            entry_frame,
            text="Invalid username or password, Try again.",
            font=("Helvetica", 14),
            text_color="#FF0000",
            anchor=ctk.CENTER
        )

        # buttons frame

        button_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=20,
            fg_color="transparent"
        )

        button_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        def loginButtonEvent():
            """
            Handles login event when button is pressed
            """
            self.username = username1.get()
            self.user.setUsername(self.username)
            if self.user.login(password1.get()) == True:
                print(f"Logged in {self.username}")

                from user.user_student import Student

                print(f"Type: {self.user.getUserType()}")
                
                match self.user.getUserType():

                    case "student":
                        
                        s = Student(self.user.getUsername())

                        if s.getProfileSetupStatus() == True:
                            print("hehe")
                            studentProfileSetupPage(attach, s)
                        elif s.isSubscribed() == False:
                            subscribePage(attach, s)
                        else:
                            studentMenuPage(attach, s)

                    case "educator":
                        return
                    case "admin":
                        return
                    case _:
                        raise AssertionError("Unknown user type")
            
            else:
                print("Login failed, Incorrect username or password")
                wrong_password_label.grid(
                    row=3,
                    column=0,
                    padx=5,
                    pady=5
                )

        login_button = ctk.CTkButton(
            button_frame,
            text="Login",
            font=("Helvetica", 14),
            width=120,
            height=50,
            command=lambda: loginButtonEvent()
            )

        login_button.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        def registerButtonEvent():
            registerPage(attach)

        register_button = ctk.CTkButton(
            button_frame,
            text="Register",
            font=("Helvetica", 14),
            width=120, height=50,
            command=lambda: registerButtonEvent()
            )

        register_button.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )


if __name__ == "__main__":
    test = App()
    l = LoginWindow()
    l.FillFrames(test)
    test.mainloop()