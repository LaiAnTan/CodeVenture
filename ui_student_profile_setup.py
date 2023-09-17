import customtkinter as ctk
from App import App
from ui_window_gen import studentMenuPage, datePickerTopLevelPage
from database.database_student import StudentDB
from user.user_student import Student

import shutil
import os

def profileSetupHandler(full_name: str, email: str, dob: str, profile_pic_path: bool):
    """
    Handles first time profile setup of a new student

    returns a 2-tuple with the first value being a boolean and the second value being the message to display.
    """

    sdb = StudentDB()

    if full_name == "" or email == "" or dob == "" or profile_pic_path == "":
        return (False, "One or more fields incomplete")
    
    sdb.add_entry()

    return (True, "Profile setup sucessful")



class StudentProfileSetupWindow:

    profile_pic_dir_path = "pfp"

    def __init__(self, student: Student):
        self.student = student
        self.full_name = ""
        self.email = ""
        self.dob = ""
        self.profile_pic_path = ""

    def	FillFrames(self, attach: App):

        def deleteProfilePic():
            try:
                os.remove(self.profile_pic_path)
            except FileNotFoundError:
                pass
            attach.main.destroy()

        attach.main.protocol("WM_DELETE_WINDOW", lambda: deleteProfilePic())

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
            text="First time profile setup",
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

        # details frame

        details_frame = ctk.CTkFrame(
            attach.main_frame,
            width=full_width,
            height=100,
            fg_color="transparent"
        )

        details_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        details_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        details_frame.columnconfigure((0, 1), weight=1)

        name_label = ctk.CTkLabel(
            details_frame,
            height=20,
            text="Full Name:",
            font=("Helvetica", 14),
        )

        name_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        name = ctk.CTkEntry(
            details_frame,
            height=20,
            placeholder_text="Full Name", 
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        name.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        email_label = ctk.CTkLabel(
            details_frame,
            height=20,
            text="Email:", 
            font=("Helvetica", 14),
        )

        email_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )

        email = ctk.CTkEntry(
            details_frame,
            height=20,
            placeholder_text="Email",
            font=("Helvetica", 14),
            justify=ctk.CENTER
        )

        email.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        date_of_birth_label = ctk.CTkLabel(
            details_frame,
            height=20,
            text="Date of Birth:",
            font=("Helvetica", 14),
        )

        date_of_birth_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )

        date_picker = None

        def dateOfBirthButtonEvent():
            date = datePickerTopLevelPage(attach)
            self.dob = date
            date_of_birth_button.configure(
                text=date
            )

        date_of_birth_button = ctk.CTkButton(
            details_frame,
            text="Select Date",
            font=("Helvetica", 14),
            width=80,
            height=30,
            command=lambda: dateOfBirthButtonEvent()
        )

        date_of_birth_button.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        profile_pic_label = ctk.CTkLabel(
            details_frame,
            height=20,
            text="Profile picture:",
            font=("Helvetica", 14),
        )

        profile_pic_label.grid(
            row=3,
            column=0,
            padx=10,
            pady=10
        )

        def profilePicButtonEvent():
            profile_pic_filepath = ctk.filedialog.askopenfilename()
            if profile_pic_filepath == ():
                return
            pfp_format = profile_pic_filepath.split(".")[-1]
            if pfp_format not in ["jpeg", "png"]:
                print("Invalid file format")
                profile_pic_button.configure(text="Invalid file format")
                return
            profile_pic_button.configure(text=f"{profile_pic_filepath.split('/')[-1]}")
            profile_pic_dirpath = "/".join(profile_pic_filepath.split("/")[:-1])
            self.profile_pic_path = self.profile_pic_dir_path + "/" + self.student.getUsername() + "." + pfp_format
            os.rename(profile_pic_filepath, self.profile_pic_path)
            shutil.copyfile(self.profile_pic_path, profile_pic_filepath)

        
        profile_pic_button = ctk.CTkButton(
            details_frame,
            text="Select Profile Picture",
            font=("Helvetica", 14),
            width=80,
            height=30,
            command=lambda: profilePicButtonEvent()
        )

        profile_pic_button.grid(
            row=3,
            column=1,
            padx=10,
            pady=10
        )

        profile_setup_failed_label = ctk.CTkLabel(
            details_frame,
            text="",
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

        def doneButtonEvent():
            ret = profileSetupHandler(self.full_name, self.email, self.dob, self.profile_pic_path)
            if ret[0] == True:
                attach.main.protocol("", "")
                studentMenuPage(attach, self.student)
            else:
                profile_setup_failed_label.configure(text=ret[1], text_color="#FF0000")
                profile_setup_failed_label.grid(
                    row=4,
                    column=0,
                    columnspan=2,
                    padx=5,
                    pady=5
                )
        

        done_button = ctk.CTkButton(
            button_frame,
            text="Done",
            font=("Helvetica", 14),
            width=80,
            height=30,
            command=lambda: doneButtonEvent()
        )

        done_button.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=30
        )