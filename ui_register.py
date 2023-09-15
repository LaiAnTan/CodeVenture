import customtkinter as ctk
from App import App
import ui_window_gen as wingen
from database.database_user import UserDB

def registerHandler(username: str, password: str, confirm_pw: str, user_type: str):
    """
    Handles registration of new user.

    returns a 2-tuple with the first value being a boolean and the second value being the message to display.
    """
    db = UserDB()

    if password != confirm_pw:
        return (False, "Register failed, passwords do not match")

    if db.fetch_attr("username", username) != None:
        return (False, "Register failed, username already taken")
    
    db.add_entry((username, password, user_type))
    return (True, "Register Sucessful")

class RegisterWindow:

    def	FillFrames(self, attach: App):

        attach.main_frame.grid(
                    row=0,
                    column=0
                )

        full_width = 450
        half_width = full_width / 2

        #title frame

        title_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=40,
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

        register_label = ctk.CTkLabel(
            title_frame,
            text="REGISTER",
            font=("Helvetica", 18, "bold"),
            justify=ctk.CENTER,
        )
        
        register_label.grid(
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
        )

        entry_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        entry_frame.rowconfigure((0, 1, 2), weight=1)
        entry_frame.columnconfigure(0, weight=1)

        new_username = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="New Username", 
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        new_username.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        new_password = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Password",
            show="•",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        new_password.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        confirm_password = ctk.CTkEntry(
            entry_frame,
            height=20,
            placeholder_text="Confirm Password",
            show="•",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        confirm_password.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        # show password checkbox

        checkbox1_status = ctk.IntVar(value=0)

        def show_password():
            print(checkbox1_status.get())
            if checkbox1_status.get() == 1:
                new_password.configure(show="")
                confirm_password.configure(show="")
            else:
                new_password.configure(show="•")
                confirm_password.configure(show="•")
            new_password.update()
            confirm_password.update()

        toggle_show_pw = ctk.CTkCheckBox(
            entry_frame,
            text="Show password",
            font=("Helvetica", 14),
            variable=checkbox1_status,
            onvalue=1,
            offvalue=0,
            command= lambda: show_password()
        )

        toggle_show_pw.grid(
            row=3,
            column=0,
            padx=10,
            pady=20
        )

        register_failed_label = ctk.CTkLabel(
            entry_frame,
            text="",
            font=("Helvetica", 14),
            text_color="#FF0000",
            anchor=ctk.CENTER
        )

        # buttons frame

        button_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=20
        )

        button_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        def registerButtonEvent():
            ret = registerHandler(new_username.get(), new_password.get(), confirm_password.get(), "student")
            if ret[0] == True:
                register_failed_label.configure(text=ret[1], text_color="#00FF00")

            elif ret[0] == False:
                register_failed_label.configure(text=ret[1], text_color="#FF0000")
            
            register_failed_label.grid(
                row=4,
                column=0,
                padx=5,
                pady=5
            )

        register_button = ctk.CTkButton(
            button_frame,
            text="Register",
            font=("Helvetica", 14),
            width=120,
            height=50,
            command=lambda: registerButtonEvent()
        )

        register_button.grid(
            row=0,
            column=0,
            padx=20,
            pady=20
        )

        def loginButtonEvent():
            wingen.loginPage(attach)

        login_button = ctk.CTkButton(
            button_frame, 
            text="Back to Login",
            font=("Helvetica", 14),
            width=120, height=50,
            command=lambda: loginButtonEvent()
        )
        
        login_button.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )
