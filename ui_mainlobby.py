import customtkinter as ctk

from interface import UI


def main_lobby(ui: UI):
    ui.frame.destroy()
    ui.frame = ctk.CTkFrame(ui.main)

    ui.frame.pack(
                padx=30,
                pady=20,
                fill="both",
                expand=True
                )
    
    ui.frame.grid(column=3, row=2)
    
    label1 = ctk.CTkLabel(ui.frame,
                        text="MAIN MENU OMGGGGG WHATT?!?!?!",
                        font=("Helvetica Bold", 20)
                        )
    
    label1.pack(pady=50
                )
    
    from ui_login import login_page
    
    button1 = ctk.CTkButton(ui.frame,
                            text="debug go back",
                            font= ("Helvetica", 14),
                            command=lambda: login_page(ui)
                            )
    
    button1.pack(padx=10,
                pady=10
                )
    
