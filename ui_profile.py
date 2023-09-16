import customtkinter as ctk
from App import App
from user.user_student import Student
from ui_window_gen import studentMenuPage

class ProfileWindow:

    def __init__(self, student: Student):
        self.student = student

    def FillFrames(self, attach: App):

        attach.main_frame.grid(
            row=0,
            column=0
        )

        header_height = 20
        full_width = 450
        half_width = full_width / 2
        full_content_height = 460 - header_height
        half_content_height = full_content_height / 2


        ## header details -------------------------------------------

        header_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=header_height
        )

        profile_title = ctk.CTkLabel(
            header_frame,
            text=f"Dashboard: {self.student.username}'s profile"
        )

        def backButtonEvent():
            studentMenuPage(attach, self.student)

        back_button = ctk.CTkButton(
            header_frame,
            text="Back",
            command=lambda : backButtonEvent(),
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

        ## main content frame

        content_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=full_content_height
        )

        content_frame.grid(
            row=1,
            column=0
        )

        ## user details

        user_details_frame = ctk.CTkFrame(
            content_frame,
            width=half_width,
            height=half_content_height
        )

        user_details_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # user details header

        user_details_header_frame = ctk.CTkFrame(
            user_details_frame,
            width=half_width,
            height=header_height
        )

        user_details_header_frame.pack(
            padx=5,
            pady=5,
            fill=ctk.BOTH,
            expand=True
        )

        user_details_header_frame.grid(
            row=0,
            column=0,
            sticky="we"
        )

        user_details_title = ctk.CTkLabel(
            user_details_header_frame,
            justify="left",
            text="User Details"
        )

        user_details_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5,
        )
        
        # user details content

        user_details_content_frame = ctk.CTkFrame(
            user_details_frame,
            width=half_width,
            height=half_content_height - header_height
        )

        user_details_content_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        user_details_label = ctk.CTkLabel(
            user_details_content_frame,
            justify="left",
            wraplength=210,
            text=
f"""Name: {self.student.getName()}
Date of birth: {self.student.getDateOfBirth()}
Email: {self.student.getEmail()}
Subscription: {self.student.getSubscriptionStatus()}
Subscription End Date: {self.student.getSubscriptionEndDate()}
""",
            width=half_width,
            height=half_content_height - header_height,
        )

        user_details_label.grid(
            row=0,
            column=0
        )

        ## graph

        graph_frame = ctk.CTkFrame(
            content_frame,
            width=half_width,
            height=half_content_height
        )

        graph_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        ## graph header

        graph_header_frame = ctk.CTkFrame(
            graph_frame,
            width=half_width,
            height=header_height
        )

        graph_header_frame.grid(
            row=0,
            column=0,
            sticky="we"
        )

        graph_title = ctk.CTkLabel(
            graph_header_frame,
            justify="left",
            text="Skills Graph"
        )

        graph_title.grid(
            row=0,
            column=0,
        )

        graph_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5,
        )

        ## graph content

        graph_content_frame = ctk.CTkFrame(
            graph_frame,
            width=half_width,
            height=half_content_height - header_height
        )

        graph_content_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        ## completion stats frame

        completion_frame = ctk.CTkFrame(
            content_frame,
            width=half_width,
            height=half_content_height
        )

        completion_frame.grid(
            row=0,
            column=1
        )

        # completion header

        completion_header_frame = ctk.CTkFrame(
            completion_frame,
            width=half_width,
            height=header_height
        )

        completion_header_frame.grid(
            row=0,
            column=0,
            sticky="we"
        )

        completion_title = ctk.CTkLabel(
            completion_header_frame,
            justify="left",
            text="Completed Activities"
        )
        
        completion_title.grid(
            row=0,
            column=0,
            sticky="we"
        )

        completion_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5,
        )

        # completion content

        completion_content_frame = ctk.CTkScrollableFrame(
            completion_frame,
            width=half_width,
            height=half_content_height - header_height
        )

        completion_content_frame.grid(
            row=1,
            column=0
        )

        ## achievements

        achievement_frame = ctk.CTkFrame(
            content_frame,
            width=half_width,
            height=half_content_height
        )

        achievement_frame.grid(
            row=1,
            column=1
        )

        # achievement header

        achievment_header_frame = ctk.CTkFrame(
            achievement_frame,
            width=half_width,
            height=header_height
        )

        achievment_header_frame.pack(
            padx=5,
            pady=5,
            fill=ctk.BOTH,
            expand=True
        )

        achievment_header_frame.grid(
            row=0,
            column=0,
            sticky="we"
        )

        achievment_title = ctk.CTkLabel(
            achievment_header_frame,
            justify="left",
            text="Achievements"
        )
        
        achievment_title.grid(
            row=0,
            column=0
        )

        achievment_title.pack(
            side=ctk.LEFT,
            padx=5,
            pady=5,
        )

        # achievement content

        achievment_content_frame = ctk.CTkScrollableFrame(
            achievement_frame,
            width=half_width,
            height=half_content_height - header_height
        )

        achievment_content_frame.grid(
            row=1,
            column=0
        )

if __name__ == "__main__":
    test = App()
    p = ProfilePage(Student("tlai-an"))
    p.FillFrames(test)
    test.mainloop()