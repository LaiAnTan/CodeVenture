import customtkinter as ctk
from App import App
from user.user_student import Student

class ProfilePage:

    def __init__(self, student: Student):
        self.student = student

    def FillFrames(self, attach: App):

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


        ## user details

        user_details_frame = ctk.CTkFrame(
            attach.main_frame
        )

        user_details_frame.grid(
            row=0,
            column=0
        )

        username_label = ctk.CTkLabel(
            user_details_frame,
            text=f"Username: {self.student.username}"
        )

        ## graph

        graph_frame = ctk.CTkFrame(
            attach.main_frame
        )

        ## completion stats

        completion_frame = ctk.CTkFrame(
            attach.main_frame
        )

        ## achievements

        achievement_frame = ctk.CTkFrame(
            attach.main_frame
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