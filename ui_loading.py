import customtkinter as ctk

from interface import UI

from ui_mainlobby import main_lobby

def loading_page(ui:UI):
    dots = 0
    counter = 0
    colour_lst = ["#ffffff", "#ededed", "#d6d6d6", "#b5b3b3", "#a1a1a1", "#8a8a8a", "#737272", "#6a6a6a" ,"#5c5c5c", "#4a4a4a", "#3a3a3a" ,"#2b2b2b", "#212121", '#212121', '#2b2b2b', '#3a3a3a', '#4a4a4a', '#5c5c5c', '#6a6a6a', '#737272', '#8a8a8a', '#a1a1a1', '#b5b3b3', '#d6d6d6', '#ededed', '#ffffff']

    def fade_word(colour, dots):
        try:
            for widget in ui.frame.winfo_children():
                widget.destroy()
        except:
            pass

        ui.frame.pack(
                    padx=30,
                    pady=25,
                    fill="both",
                    expand=True
                    )
    
    
        label1 = ctk.CTkLabel(ui.frame,
                            text="CodeVenture",
                            font=("Helvetica Bold", 60),
                            text_color=colour
                            )
        
        label1.pack(
                pady=(200, 10)
                )
        
        label2 = ctk.CTkLabel(ui.frame,
                            text="Loading crypto miner 0.0 " + "." * dots,
                            font=("Helvetica", 18)
                            )
        
        label2.pack(
                pady=0
                )
        

    while counter < 65:
        ui.frame.after(75, fade_word(colour_lst[counter % 26], dots))
        counter += 1
        dots += 1
        if dots > 6:
            dots = 0

    ui.frame.after(1,main_lobby(ui))