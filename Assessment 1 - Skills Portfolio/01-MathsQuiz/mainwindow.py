import tkinter as tk #to import tkinter so we can be able to make the GUI
from gamemenu import GameMenu #bringing in the game menu screen
from quiz import QuizFrame #importing quiz screen where the questions will show
from results import ResultsFrame #importing the results
import pygame #this is so that we can be able to have the music


class QuizApp(tk.Tk): 
    def __init__(self): #runs when we start the quiz
        super().__init__() #initializing Tk
        pygame.mixer.init() #so we can be able to play sounds
        self.title("Math Quiz")
        self.geometry("600x450")
        self.config(bg="#285430")
        
        #loads the fils for the correct and wrong answers
        self.correct_sound = pygame.mixer.Sound("01-MathsQuiz/music2.mp3") 
        self.wrong_sound = pygame.mixer.Sound("01-MathsQuiz/music3.mp3")

        self.play_music("01-MathsQuiz/music1.mp3", loop=True) #plays bg music as soon as the display starts and being able to repeat all over since there's a loop

        self.custom_font = ("Helvetica", 14)
        self.big_font = ("Helvetica", 20, "bold")

        #to keep track of current frame, the scores, level, and question number
        self.current_frame = None
        self.score = 0
        self.level = ""
        self.question_number = 0

        self.show_menu()

    #function to play bg music
    def play_music(self, filename, loop=False):
        pygame.mixer.music.load(filename) #load the music file
        pygame.mixer.music.play(-1 if loop else 0)

    #function to switch to the main menu
    def show_menu(self):
        self.switch_frame(GameMenu)

    #function to start the quiz
    def start_quiz(self, level):
        self.level = level #stores the selected level
        self.score = 0  #reset score
        self.question_number = 0 #reset question number
        self.switch_frame(QuizFrame) #switches to the QuizFrame to show questions

    def show_results(self):
        self.switch_frame(ResultsFrame) #switch to ResultsFrame to display score

    def switch_frame(self, frame_class):
        if self.current_frame is not None: #checks if theres already a frame on the window
            self.current_frame.destroy() #if yes, it removes it so it doesnt stack multiple frames
        self.current_frame = frame_class(self) #creates new instance of the frame we want to show
        self.current_frame.pack(fill="both", expand=True) # make it fill the window and expands it in a proper way

    def play_sound_effect(self, correct=True):
        if correct:
            self.correct_sound.play()
        else:
            self.wrong_sound.play()

#runs the app
if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
