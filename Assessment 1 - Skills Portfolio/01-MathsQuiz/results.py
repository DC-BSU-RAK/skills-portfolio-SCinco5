import tkinter as tk
import pygame

class ResultsFrame(tk.Frame): #initialize the frame, attach to master which is the main app then sets it bg color
    def __init__(self, master):
        super().__init__(master, bg="#285430")
        pygame.mixer.music.stop() #stops bg music when it shows the results
        score = master.score #get the final score from the main app


        if score >= 90:
            grade = "A+" #if score is 90 or more, player gets A+
        elif score >= 80:
            grade = "A" #80-89
        elif score >= 70:
            grade = "B" #70-79
        elif score >= 60:
            grade = "C" #60-69
        else:
            grade = "F" #below 60


        tk.Label(self,
                 text="RESULTS",
                 font=master.big_font,
                 bg="#285430",
                 fg="#FCE700"
                 ).pack(pady=20) #a big title label for results screen
        
        tk.Label(self,
                 text=f"Your Final Score: {score}/100",
                 font=("Helvetica", 18, "bold"),
                 bg="#285430",
                 fg="#FFEEA9"
                 ).pack(pady=10) #shows the numeric score 
        
        tk.Label(self,
                 text=f"Grade: {grade}",
                 font=("Helvetica", 18, "bold"),
                 bg="#285430",
                 fg="#F6E96B"
                 ).pack(pady=5) #shows the letter grade from the previous calculation
        tk.Button(self,
                  text="Play Again",
                  font=master.custom_font,
                  bg="#F6C453",
                  activebackground="#FFDE59",
                  command=master.show_menu,
                  width=20,
                  height=2,
                  bd=4
                  ).pack(pady=15) #button to restart quiz and calls show_menu in main app
        
        
        tk.Button(self,
                  text="Leave",
                  font=master.custom_font,
                  bg="#E76F51",
                  activebackground="#FFD8C4",
                  command=master.quit,
                  width=20,
                  height=2,
                  bd=4
                  ).pack(pady=5) #button to close the app, calls main app's quit()
        

        tk.Label(self,
                 text="Thanks for playing the game!",
                 bg="#285430",
                 fg="white",
                 font=("Helvetica", 12, "italic")
                 ).pack(side="bottom", pady=10)
