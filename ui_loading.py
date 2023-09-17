#import dependencies
import customtkinter as ctk

from App import App

import random

from ui_window_gen import *

from user.user_student import Student

class LoadingMenu:
    def __init__(self, student: Student):
        self.student = student

    def	FillFrames(self, attach: App, redirect: str, message: list):
        progress = 0
        if (message == []):
            randomized_msg = ["Lagging? Just get a better computer.", 
                            "Did you know *4 guys* made this without touching grass?",
                            "I we was me who huh? he asked what?",
                            "Our motto: Git Gud <3"]
        else:
            randomized_msg = message
        
        attach.main_frame.grid(
                    row=0,
                    column=0
                )
        
        #debug
        print("Random list:",randomized_msg)
        print("Message list:",message)
        print("Redirecting to:",redirect)
        #debug end

        full_width = 450
        half_width = full_width / 2

        #title frame
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
            font=("Helvetica Bold", 60),
            anchor=ctk.CENTER,
        )

        title_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky=""
        )

        loading_label = ctk.CTkLabel(
            title_frame,
            text=str(progress) + "%",
            font=("Helvetica Bold", 20),
            justify=ctk.CENTER,
        )
        
        loading_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=(20,5),
            sticky=""
        )

        loading_msg = ctk.CTkLabel(
            title_frame,
            text=" ",
            font=("Helvetica", 20),
            justify=ctk.CENTER,
        )

        loading_msg.grid(
            row=2,
            column=0,
            padx=10,
            pady=20,
            sticky=""
        )

        # loading bar frame

        loading_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=100,
            fg_color="transparent"
        )

        loading_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        loading_frame.rowconfigure((0, 1, 2), weight=1)
        loading_frame.columnconfigure(0, weight=1)

        loading_bar = ctk.CTkProgressBar(loading_frame, 
                                        width=half_width, 
                                        height =25
                                        )

        loading_bar.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=10
        )
        
        loading_bar.set(0)
        loading_msg.configure(text=random.choice(randomized_msg))
        # loading bar frame end
        #start animation loop
        lag_spot = random.randint(0, 100)
        delay = self.loading_time(redirect)
        for i in range(0, 100):
            loading_bar.set(float(i/100))
            loading_label.configure(text=str(i) + "%")
            attach.main.update()
            if ((i % 15) == 0):
                loading_msg.configure(text=random.choice(randomized_msg))
            #simulate loading lag for intensive tasks
            if (redirect != "settingsPage" and redirect != "profilePage"):
                if (i == lag_spot):
                    lag_spot = random.randint(lag_spot, 100)
                    attach.main.after(500)
            attach.main.after(delay)
        #end animation loop

        #redirect to page
        self.redirection(attach, redirect)

    def loading_time(self, redirect: str):
        if redirect == "profilePage":
            return 10
        elif redirect == "settingsPage":
            return 10
        else:
            return 50
    
    def redirection (self, attach: App, redirect: str):
        if redirect == "profilePage":
            profilePage(attach, self.student)
        elif redirect == "settingsPage":
            settingsPage(attach, self.student)
        elif redirect == "studentMenuPage":
            studentMenuPage(attach, self.student)
        elif redirect == "loginPage":
            loginPage(attach)
        elif redirect == "registerPage":
            registerPage(attach)

if __name__ == "__main__":
    test = App()
    l = LoadingMenu(Student("tlai-an"))
    l.FillFrames(test)
    test.mainloop()