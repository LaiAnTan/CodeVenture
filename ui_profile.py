import customtkinter as ctk
from App import App
from user.user_student import Student

class ProfilePage:

    def __init__(self, student: Student):
        self.student = student

    def FillFrames(self, attach: App):

        attach.main_frame.grid(
            row=0,
            column=0
        )

        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            attach.main_frame
        )

        profile_title = ctk.CTkLabel(
            header_frame,
            text=f"Dashboard: {self.student.username}'s profile"
        )

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : exit(),
            width=20
        )

        profile_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5
        )

        back_button.pack(
            side=ctk.RIGHT,
            padx=5,
            pady=5
        )

        header_frame.grid(
            row=0,
            column=0,
            sticky="we",
            padx=5,
            pady=5
        )

        ## header details end --------------------------------------------

        ## content frame

        content_frame = ctk.CTkFrame(
            attach.main_frame
        )

        content_frame.grid(
            row=1,
            column=0
        )

        ## user details

        user_details_frame = ctk.CTkFrame(
            content_frame
        )

        user_details_frame.grid(
            row=0,
            column=0
        )

        user_details_label = ctk.CTkLabel(
            user_details_frame,
            text=f"""Username: {self.student.username}
Subscription: Active
Date of birth: 20/10/2020
"""
        )

        user_details_label.pack(
            side=ctk.LEFT,
            pady=5,
            padx=5,
            fill=ctk.BOTH,
            expand=True
        )

        ## graph

        graph_frame = ctk.CTkFrame(
            content_frame
        )

        ## completion stats

        completion_frame = ctk.CTkFrame(
            content_frame
        )

        ## achievements

        achievement_frame = ctk.CTkFrame(
            content_frame
        )

        graph_frame.grid(
            row=0,
            column=1
        )

        completion_frame.grid(
            row=1,
            column=0
        )

        achievement_frame.grid(
            row=1,
            column=1
        )

if __name__ == "__main__":
    test = App()
    p = ProfilePage(Student("tlai-an"))
    p.FillFrames(test)
    test.mainloop()