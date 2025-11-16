import tkinter as tk #imports the GUI library in order to create the app window and widgets
from tkinter import ttk #this imports the themed Tkinter widgets for modern looks
from tkinter import messagebox #to show error dialogs
from PIL import Image, ImageTk #imports pillow to handle and display images
from tkextrafont import Font as TkFont #imports TkFont from tkextrafont to load the fonts that I wanted to use
import pygame #this imports the pygame lubrary so I can play background music and sound effects
import random # to choose the jokes randomly
import os #for file path handling

BASE = os.path.dirname(os.path.abspath(__file__)) #sets the base directory to the folder where the script is running
RES = os.path.join(BASE, "stuffs") #where all the images, background image, and such are stored here

JOKES_FILE = os.path.join(RES, "randomJokes.txt")
BG_IMAGE = os.path.join(RES, "background.jpg")
BANGERS_FONT_FILE = os.path.join(RES, "Bangers-Regular.ttf")
POPPINS_FONT_FILE = os.path.join(RES, "Poppins-Regular.ttf")
MUSIC = os.path.join(RES, "haha.mp3")
SFX = os.path.join (RES, "badumtss.mp3")

FONT_BANGERS = "Bangers"
FONT_POPPINS = "Poppins"

def load_jokes():
    jokes = [] #initialized an empty list to hold all the jokes

    if not os.path.exists(JOKES_FILE): #checks if the joke file is present in the stuffs folder
        messagebox.showerror("Error", "randomJokes.txt not found, yikes")
        return jokes
    
    with open (JOKES_FILE, "r", encoding="utf-8") as f: #opens the joke file safely and can support special characters
        for line in f: #loops through each line in the joke file
            line = line.strip() #removes leading/trailing whitespace from the line
            if  not line: #checks if the line is empty or a blank line between jokes
                continue

            parts = line.split("?", 1) #splits the line into at most 2 parts, then using the first ? to separate setup and punchline
            if len(parts) > 1 and parts [1].strip(): #checks if a punchline part exists and isn't just whitespace
                setup = parts[0].strip() + "?" #sets the setup as the first part plus the question mark
                punch = parts[1].strip() #this one sets the punchline as the clean second part
            elif len(parts) > 1: #if theres a question mark but the punchline is empty
                setup = parts[0].strip() + "?"
                punch = "(No punchline)"
            else: #if the line has no question mark 
                setup = line.strip()
                punch = "(No punchline)"

            jokes.append({ #adds the structured joke as a dictionary to the main jokes list
                "setup": setup, #jokes question 
                "punchline": punch #jokes answer
            })

    return jokes #returns the full list of jokes thats already ready


class JokesOnYouLilBoi: #defines main app class that contains all the GUI functions

    def __init__(self, root): #runs when a new app object is created
        self.root = root
        self.root.title("Alexa Tell Me a Joke!")
        self.root.geometry("900x560")
        self.root.resizable(False, False) # prevents the user from resizing the window

        self.bangers_font = TkFont(file=BANGERS_FONT_FILE)
        self.poppins_font = TkFont(file=POPPINS_FONT_FILE)

        self.title_font = (FONT_BANGERS, 38)
        self.text_font = (FONT_POPPINS, 12)
        self.punchline_font = (FONT_POPPINS, 13, "bold")

        self.bangers_message_font=(FONT_BANGERS, 14)
        self.list_title_font = (FONT_BANGERS, 16, "bold")

        self.white = "#FFFFFF"
        self.blue = "#1c5db2"
        self.black = "#000000"
        self.yellow = "#FFFF00"
        self.light_gray = "#f2f2f2"

        self.jokes = load_jokes() #calls the helper function to load all the jokes from the file into here
        self.current_index = None #variable to track which joke is currently being shown

        pygame.mixer.init() #starts the pygame mixer module to play music

        self.setup_background() # for the background image

        self.build_title_banner()
        self.build_left_panel() #to create the joke list panel on the left
        self.build_message_bubble() #to create the area where the joke setup and punchline shows
        self.build_buttons() #to create the control buttons

        self.start_music()

    def setup_background(self): #to load and display the bg image
        self.canvas = tk.Canvas(self.root, width=900, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expan=True)

        if os.path.exists(BG_IMAGE): #checks if the bg image file exists
            img = Image.open(BG_IMAGE).resize((900, 560))
            self.bg = ImageTk.PhotoImage(img)
            self.canvas.create_image(0,0,anchor="nw", image=self.bg)

    def build_title_banner(self):
        pass

    def build_left_panel(self): #to create the scrollable list of joke setups
        panel = tk.Frame(self.root, bg=self.black) 
        panel.place(x=20, y=20, width=260, height=520)


        tk.Label(
            panel,
            text="All Jokes",
            font=self.list_title_font,
            fg=self.white,
            bg=self.black
        ).pack(pady=10)

        list_frame = tk.Frame(panel) #makes a sub-frame inside the panel to hold the listbox and scrollbar together
        list_frame.pack(fill="both", expand=True, padx=10) #packs the sub-frame

        self.listbox = tk.Listbox(list_frame, font=self.text_font, bg=self.black, fg=self.white, selectbackground=self.blue, selectforeground=self.white)
        self.listbox.pack(side="left", fill="both", expand=True) #packs the listbox to the left 

        sb = tk.Scrollbar(list_frame, command=self.listbox.yview) #creates a vertical scrollbar for the listbox
        sb.pack(side="right", fill="y") #packs the scrollbox to the right side so it fills vertically
        self.listbox.config(yscrollcommand=sb.set) #links the listbox vertical scrolling to the scrollbar

        for j in self.jokes: #this one loops through all loaded jokes
            self.listbox.insert("end", j["setup"]) #adds the question of each joke to the listbox

        self.listbox.bind("<<ListboxSelect>>", self.select_from_list) #links selecting an item in the listbox to the "select_from_list"

    def build_message_bubble(self): #to create the joke display area
        self.bubble = tk.Frame(self.root, bg=self.black, bd=0, relief="flat")
        self.bubble.place(x=310, y=50, width=560, height=70)

        self.setup_label = tk.Label( #creates the label to display the joke setup
            self.bubble,
            text="Press 'Alexa tell me a Joke' to start bruh",
            bg=self.black,
            fg=self.white,
            font=self.bangers_message_font,
            wraplength=520, # wraps the text after 520 pixels to keep it within the label width
            justify= "left",
            anchor="nw"
        )
        self.setup_label.pack(padx=15, pady=5, fill="both", expand=True) #adds padding and makes the label fill the bubble frame

        self.punch_label = tk.Label( #creates the label to display the joke punchline
            self.root,
            text="",
            bg=self.black,
            fg=self.yellow,
            font=self.punchline_font,
            wraplength=520,
            justify="left",
            anchor="nw",
            pady=10,
            padx=20,
            bd=0,
            relief="flat"
        )
        self.punch_label.place(x=310, y=140, width=560, height=50)

    def build_buttons(self): #to create the control buttons
        btn_frame = tk.Frame(self.root, bg=self.black) #creates a frame to hold all the buttons
        btn_frame.place(x=330, y=210)

        style=ttk.Style()
        style.theme_use("clam")

        style.configure('TButton', #set up te appearance of all TButton widgets
                        font=(FONT_POPPINS, 10),
                        background='#333333',
                        foreground='white',
                        bordercolor='white',
                        lightcolor='#555555',
                        darkcolor='#111111')
        style.map('TButton', #sets up what happens when the button is hovered or pressed
                  background=[('active', '#555555')],
                  foreground= [('active', 'white')])
        
        ttk.Button(btn_frame, text="Alexa tell me a joke", #creates the random joke button
                   command=self.random_joke, style='TButton').grid(row=0, column=0, padx=5, pady=5)
        

        ttk.Button(btn_frame, text="Show Punchline", 
                   command=self.show_punchline, style='TButton').grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="Next Joke",
                   command=self.next_joke, style='TButton').grid(row=0, column=2, padx=5, pady=5)
        

        ttk.Button(btn_frame, text="Quit",
                   command=self.root.destroy, style='TButton').grid(row=0, column=3, padx=5, pady=5)
        

    def start_music(self): #to start the background music
        if os.path.exists(MUSIC): #checks if the music file is there
            pygame.mixer.music.load(MUSIC) #loads the music file into the mixer
            pygame.mixer.music.play(-1) #to loop the music

    def pause_music(self): #to temporarily stop the music
        if pygame.mixer.music.get_busy(): #checks if music is currently playing
            pygame.mixer.music.pause() #pauses the playback

    def resume_music(self): 
        if pygame.mixer.get_init():
            pygame.mixer_music.unpause() #resumes back to when the music was last paused

    def play_sfx_then_resume(self): # to play sound effect and then resume the music
        if not os.path.exists(SFX): #checks if the sound effect file is not there
            self.resume_music() #if its not there it just plays the music
            return
        
        self.pause_music()

        sound = pygame.mixer.Sound(SFX) #loads the sound effect
        length=sound.get_length()

        sound.play()

        self.root.after(int(length * 1000), self.resume_music) #scheds the resume_music function to run after the sound effect has finished

    def random_joke(self):
        if not self.jokes:
            return
        idx = random.randint(0, len(self.jokes) - 1) #chooses a random index number within the jokes list
        self.show_joke(idx) #calls main display function with the random index

    def next_joke(self):
        if not self.jokes:
            return
        
        new_index = random.randint(0, len(self.jokes) - 1) #picks a new random index

        while new_index == self.current_index and len(self.jokes) > 1: #loops to ensure the new index is different from the current one
            new_index = random.randint(0, len(self.jokes) - 1) #picks another random index

        self.show_joke(new_index) #shows the new random joke

    def show_punchline(self):
        if self.current_index is None: #checks if a joke setup is currently selected
            self.punch_label.config(text="Select a joke first") #shows this message if no joke is selected
            return
        
        punch = self.jokes[self.current_index]["punchline"] #gets the punchline text for the currently selected joke
        self.punch_label.config(text=punch) #updates the punchline label with the answer

        self.play_sfx_then_resume() #plays the sound effect and plays the music

    def select_from_list(self, event): #this is called when a user clicks a joke in the listbox
        if not self.listbox.curselection(): #checks if anything is actually selected
            return
        
        idx = self.listbox.curselection()[0] #gets the position of the selected joke in the listbox
        self.show_joke(idx) #displays selected joke

    def show_joke(self, idx): #the central part to displaying a joke based on its index
        self.current_index = idx #updates the current joke index tracker
        joke = self.jokes[idx] #gets the entire joke dictionary using the index

        self.setup_label.config(text=joke["setup"]) #updates the setup label to show the joke question
        self.punch_label.config(text="") #this part clears the punchline label so the person playing the game has to click "show punchline" to see it

        self.listbox.selection_clear(0, "end") #clears all existing selections in the listbox
        self.listbox.selection_set(idx) #selects the joke that is currently being displayed
        self.listbox.see(idx) #scrolls the listbox to make the selected joke visible

if __name__ == "__main__":
    root = tk.Tk()
    app = JokesOnYouLilBoi(root)
    root.mainloop()