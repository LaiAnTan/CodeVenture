import customtkinter as ctk

from interface import UI

from ui_mainlobby import main_lobby


def loading_page(ui: UI):
    ui.frame.destroy()
    ui.frame = ctk.CTkFrame(ui.main)

    ui.frame.pack(
                padx=30,
                pady=20,
                fill="both",
                expand=True
                )
    
    label1 = ctk.CTkLabel(ui.frame,
                        text="CodeVenture",
                        font=("Helvetica Bold", 20)
                        )
    
    label1.pack(
            padx=10,
            pady=20
            )
    
    label2 = ctk.CTkLabel(ui.frame,
                          text="Loading...",
                          font=("Helvetica", 18)
                          )
    
    label2.pack(
            padx=10,
            pady=10
            )
    
    progressbar1 = ctk.CTkProgressBar(ui.frame, 
									width=300,
									height=30,
									mode="indeterminate",
									indeterminate_speed=0.5
									)
    
    progressbar1.pack(padx=10, 
					pady=50
					)
    progressbar1.stop()

    from ui_login import login_page
    
    def loading_bar():
        progressbar1.start()
        ui.frame.after(5000, lambda: main_lobby(ui))

    button1 = ctk.CTkButton(ui.frame,
                            text="debug go back",
                            font= ("Helvetica", 14),
                            command=lambda: login_page(ui)
                            )   
    
    button1.pack(padx=10,
                pady=10
                )
    
    ui.frame.after(1, lambda: loading_bar())


