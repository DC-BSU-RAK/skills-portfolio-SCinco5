import tkinter as tk

#is a frame that acts as the main menu for selecting the quiz difficulty
class GameMenu(tk.Frame):
    """Menu to allow the player to select difficulty"""
    
    def __init__(self, master): 
        super().__init__(master, bg="#285430") 

        #creates title label for the menu
        tk.Label(
            self, 
            text="DIFFICULTY LEVEL",
            font=master.big_font,
            bg="#285430",
            fg="#FCE700"
            ).pack(pady=40) #adds label to the frame and for the pady it adds vertical spacing from top


        button_style = {
            "font": master.custom_font,
            "width": 25,
            "height": 2,
            "bg": "#F6E96B",
            "activebackground": "#F6C453", #the color you see when the button is clicked or hovered
            "fg": "#000",
            "relief": "ridge", #gives a 3D look
            "bd": 4 #border thickness
        }
        
        #Easy button
        tk.Button(self,
                  text="Easy",
                  command=lambda: master.start_quiz("Easy"), #when clicked,call the main quiz app's start_quix method with Easy
                  **button_style
                  ).pack(pady=10)
        
        #Moderate button
        tk.Button(self,
                  text="Moderate",
                  command=lambda: master.start_quiz("Moderate"),
                  **button_style
                  ).pack(pady=10)
        
        #Advanced button
        tk.Button(self,
                  text="Advanced",
                  command=lambda: master.start_quiz("Advanced"),
                  **button_style
                  ).pack(pady=10)
        
        #just a message at the bottom of the menu for the player
        tk.Label(self,
                 text="Ready or Not, Your Maths Quiz is Here!",
                 bg="#285430",
                 fg="white",
                 font=("Helvetica", 12,"italic")
                 ).pack(side="bottom", pady=20)