import tkinter as tk
from tkinter import messagebox #for popups or feedback to the user
from need import randomInt, decideOperation, isCorrect #to generate numbers based on the difficulty, picks what kind of operation will be used for the problem, and checks if the players answer is correct
import pygame

class QuizFrame (tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#285430")
        self.master = master #store the reference to the main display to access score, question_number, level, and play sounds
        self.num1 = 0 #initialize first number of the math problem
        self.num2 = 0 #initialize second number
        self.operation = "" #initialize operation
        self.attempts = 1 #initialize attempts for each question

        self.master.play_sound_effect(correct=True) #plays correct answer when the frame opens
        self.create_problem() #to generate and display first math question
 

    def create_problem(self):
        self.clear() #removes all previous widgets from the frame so new questions can be shown
        self.attempts = 1 #resets attempts to 1 for the new question
        level = self.master.level #gets the difficulty level from the main app
        self.num1, self.num2 = randomInt(level) #generates 2 random numbers based on the difficulty
        self.operation = decideOperation() #randomly chooses a math operation


        #display the question number as a label and style it
        tk.Label(self,
                 text=f"Question {self.master.question_number + 1} of 10",
                 font=self.master.big_font,
                 bg= "#285430",
                 fg="#F6E96B"
                 ).pack(pady=10)
        
        #displays actual math question in big font with the color and spacing
        tk.Label(self,
                 text=f"{self.num1} {self.operation} {self.num2} = ?",
                 font=self.master.big_font,
                 bg="#285430",
                 fg="#FFEEA9"
                 ).pack(pady=15)
        
        #creates an entry box for the player to type the answer
        self.answer_entry = tk.Entry(self,
                                     font=("Helvetica", 18),
                                     justify="center",
                                     bg="#F6E96B",
                                     relief="sunken"
                                     )
        self.answer_entry.pack(pady=15)
        self.answer_entry.focus() #focus the entry box so the player can start typing immediately

        #creates a submit button, style, and links it to check_answer()
        tk.Button(self,
                  text="Submit Answer",
                  font=self.master.custom_font,
                  bg="#F6C453",
                  activebackground="#FFDE59",
                  bd=4,
                  command=self.check_answer
                  ).pack(pady=10)
    
    #checks if input is correct
    def check_answer(self):
        try:
            user_ans = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid", "Enter a valid number.")
            return
        
        #checks if answer is correct
        if isCorrect(user_ans, self.num1, self.num2, self.operation):
            self.master.play_sound_effect(correct=True)
            if self.attempts == 1: #if first attempt
                self.master.score += 10 #it will give them 10 points
                messagebox.showinfo("Nice one!", "Sheeesh! +10 points")
            else: #if second attempt
                self.master.score += 5 #it will give them 5 points
                messagebox.showinfo("Good job!", "Correct on the second try! +5 points")


            self.master.question_number +=1
            if self.master.question_number < 10: #if less than ten questions, create the next question
                self.create_problem()
            else:
                self.master.show_results() #otherwise, it will show the results

        else: #if answer is wrong

            self.master.play_sound_effect(correct=False) #plays wrong answer sound effect
            if self.attempts == 1: #first attempt
                self.attempts += 1 #increase attempts to allow them to have a second try
                messagebox.showinfo("Try Again Broski", "Nuh uh! Try Again!")
                self.answer_entry.delete(0, tk.END)
            else: #if second attempt is still wrong
                messagebox.showinfo("Wrong!", "Bad luck! Next question.")
                self.master.question_number += 1 #move to next question
                if self.master.question_number < 10: #checks if the quiz is still ongoing
                    self.create_problem() #shows next question
                else:
                    self.master.show_results() #else, show results
    def clear(self): #function to remove all widgets from the frame
        for widget in self.winfo_children():
            widget.destroy() #destroy each widget