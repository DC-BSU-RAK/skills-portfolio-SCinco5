import tkinter as tk     #to create the GUI application
from tkinter import ttk, simpledialog, messagebox, font   
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #in this part it is to ensure that the file paths are relative to the script file location thing 
FILE_NAME = os.path.join(BASE_DIR, "resources", "studentMarks.txt")
TOTAL_CW_MARKS = 60
TOTAL_EXAM_MARKS = 100
TOTAL_OVERALL_MARKS = TOTAL_CW_MARKS + TOTAL_EXAM_MARKS


COLOR_PRIMARY = "#000000"  
COLOR_ACCENT = "#FFD700"  
COLOR_TEXT_LIGHT = "#FFFFFF"
COLOR_TEXT_DARK = "#000000"  
TREEVIEW_BG = "#444444"    


FONT_TITLE = "Graduate"    
FONT_BODY = "Montserrat"  
SIZE_TITLE = 24
SIZE_HEADER = 16
SIZE_BUTTON = 10

#this section stores the student data, as well as calculating the totals, grades, and its percentage
class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = str(code)  
        self.name = name
        self.cw_marks = [int(cw1), int(cw2), int(cw3)]
        self.exam_mark = int(exam)


        self.total_cw_mark = sum(self.cw_marks)  #adds all 3 coursework marks
        self.overall_total = self.total_cw_mark + self.exam_mark
        self.overall_percentage = (self.overall_total / TOTAL_OVERALL_MARKS) * 100
        self.grade = self._calculate_grade()   #this automatically calculates the final grade

#with all the calculating, it converts the percentage to the letter grade assigned
    def _calculate_grade(self):
        p = self.overall_percentage
        if p >= 70:
            return 'A'
        elif p >= 60:
            return 'B'
        elif p >= 50:
            return 'C'
        elif p >= 40:
            return 'D'
        else:
            return 'F'


    def to_file_line(self):    #to join the coursework marks list into a single string separated by commas
        cw_str = ",".join(map(str, self.cw_marks))
        return f"{self.code},{self.name},{cw_str},{self.exam_mark}"


    def to_display_tuple(self):      #return all the students info as a tuple so the treeview can display it easily
        return (
            self.name,  #this shows the students name first
            self.code,      #then student code or the ID
            self.total_cw_mark,    #their total coursework marks they got
            self.exam_mark,     #exam mark
            f"{self.overall_percentage:.2f}%",     #overall percentage formatted with 2 decimals
            self.grade      #the final grade where they either get A, B, C, or others
        )


class StudentRecordsDataRn:
    def __init__(self, master):
        self.master = master     #stores the main Tkinter window so we can edit it on later
        master.title("Student Records")

        from tkextrafont import Font as TkExtraFont   #this is to import the extra font loader so I can be able to use custom fonts which I got from google fonts
        import os
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))   #get the folder where this python file is stored
            font_dir = os.path.join(base_dir, "resources", "fonts")  #inside the folder, go to resources/fonts to load the custom font files


            TkExtraFont(file=os.path.join(font_dir, "Graduate-Regular.ttf"), family="Graduate")
            TkExtraFont(file=os.path.join(font_dir, "Montserrat-Regular.ttf"), family="Montserrat")
           
            print("Fonts loaded successfully.")
        except Exception as e:
            print("Font loading error:", e)   #in case the fonts failed to load
       
        master.geometry("1200x700") #the window size
        master.configure(bg=COLOR_PRIMARY) #background color of the main window


        self.students = [] #list to store all student objects
        self._load_data()   #loads student data from the text file into self.students
        self.total_students = len(self.students)   # counts how many students were loaded from the file


        self._setup_styles()  #sets up the custom styles such as the treeview volors, button styles, and more
       
        self._setup_widgets()  #sets up the widgets and layout such as the panels, buttons, etc
       
        self._create_menu()   #creates the top menu bar


    def _setup_styles(self):
        style = ttk.Style()  #creates a style object so we can customize the look of the Tkinter widgets
       
        style.theme_create("university", parent="alt", settings={   
            "TFrame": {"configure": {"background": COLOR_PRIMARY}},  #set frame backgrounds to the primary color
            "TLabel": {"configure": {"background": COLOR_PRIMARY, "foreground": COLOR_ACCENT, "font": (FONT_BODY, 12)}}, # match label background with the frame,accent colored text
            "TButton": {"configure": {"background": COLOR_ACCENT, "foreground": COLOR_TEXT_DARK, "font": (FONT_BODY, SIZE_BUTTON, 'bold')}},
           
            "Treeview": {  
                "configure": {
                    "font": (FONT_BODY, 10),   #table font
                    "background": TREEVIEW_BG,         #table background color
                    "foreground": COLOR_TEXT_LIGHT,    #text color
                    "fieldbackground": TREEVIEW_BG,   #background inside cells
                    "rowheight": 25    #the height of each row
                },
                "map": {   # this highlights row color
                    "background": [('selected', '#666666')],
                    "foreground": [('selected', COLOR_TEXT_LIGHT)]
                }
            },
            "Treeview.Heading": {
                "configure": {
                    "font": (FONT_BODY, 12, 'bold'),   #the header text thats bold
                    "background": COLOR_ACCENT,       # gold header background
                    "foreground": COLOR_TEXT_DARK      #dark header text
                }
            },
            "TCombobox": {
                "configure": {
                    "background": COLOR_ACCENT,       #dropdown background
                    "foreground": COLOR_TEXT_DARK,     # text color
                    "fieldbackground": COLOR_ACCENT,     # inside field area
                    "selectbackground": COLOR_ACCENT,   
                    "selectforeground": COLOR_TEXT_DARK,
                    "arrowcolor": COLOR_TEXT_DARK,     #arrow on the right side
                },
                "map": {
                    "background": [('readonly', COLOR_ACCENT)],   #readonly combo style
                    "foreground": [('readonly', COLOR_TEXT_DARK)],
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground": COLOR_ACCENT,   #entry background
                    "foreground": COLOR_TEXT_DARK,     #entry text
                }
            }
        })
        style.theme_use("university")    #to activiate the theme that i just created
       
       #setting up the custom fonts for titles and headings
        self.font_app_title = font.Font(family=FONT_TITLE, size=SIZE_TITLE, weight="bold")
        self.font_panel_title = font.Font(family=FONT_TITLE, size=SIZE_HEADER, weight="bold")
        self.font_heading = font.Font(family=FONT_BODY, size=SIZE_HEADER, weight="bold")


    def _setup_widgets(self):   
        #creates a frame for the big title at the top
        title_frame = ttk.Frame(self.master, padding="10 10 10 10", style="TFrame")
        title_frame.pack(side="top", fill="x")
       
        title_label = tk.Label(title_frame, text="STUDENT RECORDS",
                               font=self.font_app_title, bg=COLOR_PRIMARY, fg=COLOR_ACCENT)
        title_label.pack(pady=10)

        #so this is the main frame that will hold the left panel which has the buttons and the right panel where the table is
        self.main_content_frame = ttk.Frame(self.master, style="TFrame")
        self.main_content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
       
        self.display_frame = ttk.Frame(self.main_content_frame, padding="10", style="TFrame")
        self.display_frame.pack(side="right", fill="both", expand=True)
       
        self._setup_display_area()


        self._setup_control_panel()
       
    def _setup_display_area(self):
        #creates the treeview widget which is the table
        self.tree = ttk.Treeview(self.display_frame,
                                 columns=("Name", "Code", "Total CW", "Exam Mark", "Percentage", "Grade"),
                                 show='headings')

        #the column settings where the column title, alignment, and width can be edited here
        col_settings = [
            ("Name", "w", 220), ("Code", "center", 120), ("Total CW", "center", 100),
            ("Exam Mark", "center", 100), ("Percentage", "center", 120), ("Grade", "center", 100)
        ]
       
        for col, anchor, width in col_settings:
            self.tree.column(col, anchor=anchor, width=width, minwidth=width)  #set how each column behaves like the alignment and the width
            self.tree.heading(col, text=col)    #set the column header text


        vsb = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.tree.yview)  #to create a vertical scrollbar for the treeview
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)  #connect the treeview to the scrollbar


        self.tree.pack(fill="both", expand=True)   #displays the treeview table
       

        #this label will show the summary texts such as the totals, highest score, etc
        self.summary_label = tk.Label(self.display_frame, text="",
                                      font=(FONT_BODY, 12, 'italic'), bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT, justify=tk.LEFT)
        self.summary_label.pack(side="bottom", fill="x", pady=10)


    def _setup_control_panel(self):
       

       #the left sidebar the one entitled as MENU
        self.control_panel = tk.Frame(self.main_content_frame, bg=COLOR_PRIMARY, width=300, relief='solid', bd=2)
        self.control_panel.pack(side="left", fill="y", padx=10, pady=10)
        self.control_panel.pack_propagate(False)  #to prevent automatic shrinking

        #heaeder text inside the control panel
        header_label = tk.Label(self.control_panel, text="MENU",
                                font=self.font_panel_title, bg=COLOR_PRIMARY, fg=COLOR_ACCENT)
        header_label.pack(side="top", fill="x", pady=15, padx=10)

        #container for the buttons inside the panel
        button_frame = tk.Frame(self.control_panel, bg=COLOR_PRIMARY)
        button_frame.pack(side="top", fill="x", padx=10)
       
        functions = [
            ("View All Student Records", self.view_all_records),
            ("View Individual Student Record", self.view_individual_record),
            ("Show Student with Highest Total Score", lambda: self.show_extremum_record('highest')),
            ("Show Student with Lowest Total Score", lambda: self.show_extremum_record('lowest')),
            ("Sort Student Records", self.sort_records),
            ("Add a Student Record", self.add_record_dialog),
            ("Delete a Student Record", self.delete_record_dialog),
            ("Update a Student's Record", self.update_record_dialog)
        ]

        #create a button for every function above
        for text, command in functions:
            btn = tk.Button(button_frame, text=text, command=command,
                            bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'),
                            activebackground=COLOR_ACCENT, activeforeground=COLOR_TEXT_DARK,
                            relief='flat', padx=5, pady=8)
            btn.pack(fill="x", pady=5)


        # Adjust text size inside the control panel (under MENU header)
        for child in button_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(font=(FONT_BODY, 10))  
           
        self.view_all_records() #shows all records automatically when the program starts


    def _create_menu(self): # creates the top menu bar
        menu_bar = tk.Menu(self.master, bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT, font=(FONT_BODY, 10))
        self.master.config(menu=menu_bar)

        #first dropdown menu the viewing options
        core_menu = tk.Menu(menu_bar, tearoff=0, bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT)
        menu_bar.add_cascade(label="View Records", menu=core_menu)
        core_menu.add_command(label="View All Student Records", command=self.view_all_records)
        core_menu.add_command(label="View Individual Student Record", command=self.view_individual_record)
        core_menu.add_command(label="Show Highest Total Score", command=lambda: self.show_extremum_record('highest'))
        core_menu.add_command(label="Show Lowest Total Score", command=lambda: self.show_extremum_record('lowest'))
       

       #second dropdown which is to manage data
        data_menu = tk.Menu(menu_bar, tearoff=0, bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT)
        menu_bar.add_cascade(label="Data Management", menu=data_menu)
        data_menu.add_command(label="Sort Student Records", command=self.sort_records)
        data_menu.add_command(label="Add a Student Record", command=self.add_record_dialog)
        data_menu.add_command(label="Delete a Student Record", command=self.delete_record_dialog)
        data_menu.add_command(label="Update a Student's Record", command=self.update_record_dialog)
       
       #quick exit button on the menu bar
        menu_bar.add_command(label="Exit", command=self.master.quit)


    def _load_data(self):
        #if file is missing, it warns the user and creates a new file with a "0" count
        if not os.path.exists(FILE_NAME):
            messagebox.showwarning("File Missing", f"File not found: {FILE_NAME}. Creating an empty file.")
            with open(FILE_NAME, 'w') as f:
                f.write("0\n")
            return


        try:
            with open(FILE_NAME, 'r') as f:
                lines = f.readlines()
           
            data_lines = lines[1:] #skips the first line which contrains the number of records
           
            self.students.clear() #clear previous data
            for line in data_lines: #process each students record
                line = line.strip()
                if not line: continue


                parts = line.split(',')  #split each line by comma

                #ensure exactly 6 values exist before creating a student object and adds the student to the internal list
                if len(parts) == 6:
                    student = Student(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
                    self.students.append(student)


            self.total_students = len(self.students)  #updates the count of total students after loading


        except Exception as e:

            #catch any unexpected file-reading error
            messagebox.showerror("Error", f"Error loading data from file: {e}")
            self.students.clear()  #clear list to avoid keeping corrupted data


    def _save_data(self):
        try:
            self.total_students = len(self.students) #update student count before saving
            with open(FILE_NAME, 'w') as f:  #write data to the file
                f.write(f"{self.total_students}\n")  #first line contains number of records
               
                for student in self.students:   #write each student record as one line
                    f.write(student.to_file_line() + "\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data to file: {e}")
            return False


   
    def _clear_display(self):
        #removes all rows from the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

            #clear the summary text at the bottom
        self.summary_label.config(text="")


    def _populate_treeview(self, student_list):
        #clear old content before inserting new
        self._clear_display()
        total_percentage = 0  #for calculating class average
        for student in student_list:  #insert each students data into the table
            self.tree.insert('', 'end', values=student.to_display_tuple())
            total_percentage += student.overall_percentage
       
       #calculate number of students and the average percentage
        num_students = len(student_list)
        avg_percentage = total_percentage / num_students if num_students > 0 else 0
       
       #build a summary text string displayed under the table
        summary = (f"Summary: \n"
                   f"Number of students in class: {num_students}\n"
                   f"Average overall percentage mark obtained: {avg_percentage:.2f}%")
        self.summary_label.config(text=summary)
       
    def _display_single_record(self, student, title="Student Record"):
        #build a formatted string containing one students full info
        result = (f"Student Name: {student.name}\n"
                  f"Student Number: {student.code}\n"
                  f"Total Coursework Mark: {student.total_cw_mark} / {TOTAL_CW_MARKS}\n"
                  f"Exam Mark: {student.exam_mark} / {TOTAL_EXAM_MARKS}\n"
                  f"Overall Percentage: {student.overall_percentage:.2f}%\n"
                  f"Student Grade: {student.grade}")
        messagebox.showinfo(title, result)  #show the details in a popup window

    def view_all_records(self):
        #simply display all loaded students in the treeview
        self._populate_treeview(self.students)


    def view_individual_record(self):
        #asks the user for a student code or student name
        student_id_or_name = simpledialog.askstring("Search Student", "Enter Student Code or Name:", parent=self.master)
        if not student_id_or_name: #if nothing was entered, stops the function
            return

        #try to find the student by code or by lowercase name
        found_student = None
        for student in self.students:
            if student.code == student_id_or_name or student.name.lower() == student_id_or_name.lower():
                found_student = student
                break

        # show the student record if found
        if found_student:
            self._display_single_record(found_student, title="Individual Student Record")
        else:
            #otherwise show a simple not found message
            messagebox.showinfo("Not Found", f"No student found with code or name: {student_id_or_name}")


    def show_extremum_record(self, mode):
        # if no students exist, there is nothing to search for
        if not self.students:
            messagebox.showinfo("Info", "No student records available.")
            return

        # use a lambda to choose students by their total mark value
        key_func = lambda s: s.overall_total
       
       #find the student with the highest or lowest total marks
        if mode == 'highest':
            student = max(self.students, key=key_func)
            title = "Student with Highest Total Score"
        elif mode == 'lowest':
            student = min(self.students, key=key_func)
            title = "Student with Lowest Total Score"
        else:
            return  

        #after choosing highest/lowest student, show the students full record
        self._display_single_record(student, title=title)
       
    def sort_records(self):   #open the sorting dialog window and pass the root window, student list, callback o refresh the table after sorting
        SortDialog(self.master, self.students, self._populate_treeview).show()
       
    def add_record_dialog(self): #this one opents the dialog to add a new student as well as passes the save data so the file updates after adding
        AddStudentDialog(self.master, self.students, self._save_data).show()
        self.view_all_records()
       
    def delete_record_dialog(self): #ask user to enter which student to delete
        student_id_or_name = simpledialog.askstring("Delete Student", "Enter Student Code or Name to DELETE:", parent=self.master)
        if not student_id_or_name:
            return
           
        found_student = None
        for student in self.students: #search for a matching student
            if student.code == student_id_or_name or student.name.lower() == student_id_or_name.lower():
                found_student = student
                break
               
        if found_student: # this part asks for confirmation before deleting
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record for {found_student.name} ({found_student.code})?")
            if confirm: # removes the student from the list
                self.students.remove(found_student)
                if self._save_data():  #save changes to file
                    messagebox.showinfo("Success", f"Record for {found_student.name} deleted and file updated.")
                    self.view_all_records()
        else:  #if no student matches
            messagebox.showinfo("Not Found", f"No student found with code or name: {student_id_or_name}")


    def update_record_dialog(self): #ask which student the user wants to update
        student_id_or_name = simpledialog.askstring("Update Student", "Enter Student Code or Name to UPDATE:", parent=self.master)
        if not student_id_or_name:
            return
           
        found_student = None
        for student in self.students:  #search for student using code or lowercase name
            if student.code == student_id_or_name or student.name.lower() == student_id_or_name.lower():
                found_student = student
                break
               
        if found_student: #open the update dialog, pass root window, student being edited, list of all students, save function to apply changes
            UpdateStudentDialog(self.master, found_student, self.students, self._save_data).show()
            self.view_all_records() #refresh table after update
        else:
            messagebox.showinfo("Not Found", f"No student found with code or name: {student_id_or_name}")


class SortDialog(simpledialog.Dialog):
    def __init__(self, parent, students, callback):
        self.students = students
        self.callback = callback
        self.sort_criteria = tk.StringVar(parent, value='overall_percentage') #the variables storing the users choices
        self.sort_order = tk.StringVar(parent, value='descending')
        super().__init__(parent, title="Sort Student Records")  #initialize tkinter dialog class


    def body(self, master): #create the main frame inside the dialog
        dialog_frame = tk.Frame(master, bg=COLOR_PRIMARY)
        dialog_frame.pack(padx=10, pady=10)
       
        tk.Label(dialog_frame, text="Sort by:", font=(FONT_BODY, 12), bg=COLOR_PRIMARY, fg=COLOR_ACCENT).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        #dictionary connects user-friendly names to actual student attributed
        criteria_options = {
            "Overall Percentage": 'overall_percentage',
            "Name": 'name',
            "Student Code": 'code'
        }
        criteria_names = list(criteria_options.keys())
        self.sort_criteria.set(criteria_options[criteria_names[0]])
       
       #create the dropdown menu for choosing sorting field
        criteria_menu = ttk.Combobox(dialog_frame, textvariable=self.sort_criteria, values=list(criteria_options.values()), state='readonly', font=(FONT_BODY, 10))
        criteria_menu['value'] = tuple(criteria_options.values()) #make sure values inside dropdown show the correct list
        criteria_menu.current(0)
        criteria_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
       
        tk.Label(dialog_frame, text="Order:", font=(FONT_BODY, 12), bg=COLOR_PRIMARY, fg=COLOR_ACCENT).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        order_options = ['Descending', 'Ascending']
        order_menu = ttk.Combobox(dialog_frame, textvariable=self.sort_order, values=order_options, state='readonly', font=(FONT_BODY, 10))
        order_menu.current(0)
        order_menu.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
       
        return dialog_frame


    def apply(self):
        criteria = self.sort_criteria.get() #get the selected sorting option overall %, code, or name
        reverse = self.sort_order.get() == 'Descending'  #check if the user chose descending and if they choose yes it reverse sorting order
       
        if criteria == 'code':
            sort_key = lambda s: int(s.code) #if sorting by code is to convert student.code to integer
        elif criteria == 'name':
            sort_key = lambda s: s.name.lower() # if sorting by name to convert to lowercase for consistent sorting
        else:
            sort_key = lambda s: s.overall_percentage #default sorting to sort by overall percentage
           
        sorted_students = sorted(self.students, key=sort_key, reverse=reverse) #to actually sort the list of students using pythons built in sorted()
       
        self.callback(sorted_students)  #update the main UI table with the sorted results


    def buttonbox(self):
        box = tk.Frame(self, bg=self.master.cget('bg')) #create a frame for OK and cancel buttons
       
        ok_button = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE,
                              bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'), relief='flat')
        ok_button.pack(side="left", padx=5, pady=5) #ok button to triggers .ok() which triggers validate + apply
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel,
                                  bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'), relief='flat')
        cancel_button.pack(side="right", padx=5, pady=5)
       
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
       
        box.pack(fill='x')


class AddStudentDialog(simpledialog.Dialog):  #dialog window for adding a new student record
    def __init__(self, parent, students, save_callback):  
        self.students = students  #reference to the student list
        self.save_callback = save_callback  #function used to save to file
        self.entries = {}    #will store all input fields
        super().__init__(parent, title="Add New Student Record")   #call parent class initializer which creates dialog window


    def body(self, master):
        dialog_frame = tk.Frame(master, bg=COLOR_PRIMARY)
        dialog_frame.pack(padx=10, pady=10) #container for all form inputs
       

       #define label and entry fields
        fields = [
            ("Student Code (1000-9999):", "code"),
            ("Student Name:", "name"),
            ("Coursework 1 (0-20):", "cw1"),
            ("Coursework 2 (0-20):", "cw2"),
            ("Coursework 3 (0-20):", "cw3"),
            ("Exam Mark (0-100):", "exam")
        ]
       
       #create labels and entries in a loop
        for i, (label_text, key) in enumerate(fields):
            tk.Label(dialog_frame, text=label_text, font=(FONT_BODY, 10), bg=COLOR_PRIMARY, fg=COLOR_ACCENT).grid(row=i, column=0, padx=5, pady=5, sticky='w')  #add label for each field
            entry = ttk.Entry(dialog_frame, font=(FONT_BODY, 10))
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')  #add input box
            self.entries[key] = entry   #save each entry widget into a dictionary for later use
           
        return self.entries["code"]  #make the student code field auto focused


    def validate(self):   #validation runs before apply() when clicking ok
        try:
            code = self.entries['code'].get()
            if not (1000 <= int(code) <= 9999):
                messagebox.showwarning("Invalid Input", "Student code must be between 1000 and 9999.")
                return False
            #student code must be a 4 digit number
            if any(s.code == code for s in self.students):
                messagebox.showwarning("Invalid Input", "Student code already exists.")
                return False
            #prevent duplicate student codes


            name = self.entries['name'].get().strip()
            if not name:
                messagebox.showwarning("Invalid Input", "Student Name cannot be empty.")
                return False
            #name cannot be empty


            cw_marks = [int(self.entries[f'cw{i}'].get()) for i in range(1, 4)]
            exam_mark = int(self.entries['exam'].get())  #converts all the coursework and exam text inputs to integers
           
            for mark in cw_marks:
                if not (0 <= mark <= 20):
                    messagebox.showwarning("Invalid Input", "Coursework marks must be between 0 and 20.")
                    return False
                #cw marks must be valid
           
            if not (0 <= exam_mark <= 100):
                messagebox.showwarning("Invalid Input", "Exam mark must be between 0 and 100.")
                return False
            #exam mark range check
           
            self.result = (code, name, cw_marks[0], cw_marks[1], cw_marks[2], exam_mark) #store valid data so apply() can use it
            return True
           
        except ValueError:
            #gets the non-integer inputs
            messagebox.showwarning("Invalid Input", "Marks and Code must be valid integers.")
            return False


    def apply(self):   #this runs after validate() returns true
        code, name, cw1, cw2, cw3, exam = self.result
       
        new_student = Student(code, name, cw1, cw2, cw3, exam) #creates a new student object
       
        self.students.append(new_student) # add student to the main student list
       
        if self.save_callback(): #save to text file
            messagebox.showinfo("Success", f"Student {name} added successfully.")  #notify user


    def buttonbox(self):
        box = tk.Frame(self, bg=self.master.cget('bg'))   #the button container
       
        ok_button = tk.Button(box, text="Add Student", width=15, command=self.ok, default=tk.ACTIVE,
                              bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'), relief='flat')
        ok_button.pack(side="left", padx=5, pady=5)   #ok button renamed as "add student"
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel,
                                  bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'), relief='flat')
        cancel_button.pack(side="right", padx=5, pady=5)
       
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
       
        box.pack(fill='x')


class UpdateStudentDialog(simpledialog.Dialog): # this class creates a pop=up window used to update a students info
    def __init__(self, parent, student, students_list, save_callback):
        self.student = student #to store the specific student object to edit
        self.students_list = students_list #keep the whole student list and is useful later on
        self.save_callback = save_callback #this function will save the updated data back to the file
        self.entries = {} #dictionary to store all input boxes
        super().__init__(parent, title=f"Update Record for {student.name}") #this creates the dialog window with a title


    def body(self, master):
        dialog_frame = tk.Frame(master, bg=COLOR_PRIMARY) #a frame inside the dialog to hold the form elements

        dialog_frame.pack(padx=10, pady=10) #add padding so that the UI doesnt look too much crowded
       
        tk.Label(dialog_frame, text=f"Updating Record for: {self.student.name} ({self.student.code})", #create a label that tells the user whose record is being edited
                 font=(FONT_BODY, 12, 'bold'), bg=COLOR_PRIMARY, fg=COLOR_ACCENT).grid(row=0, column=0, columnspan=2, pady=10)
                 
        fields = [ #the list of all the form fields that I want to show
            ("Student Name:", "name", self.student.name), #so here, each field has a label, a dictionary key, and a default value
            ("Coursework 1 (0-20):", "cw1", self.student.cw_marks[0]),
            ("Coursework 2 (0-20):", "cw2", self.student.cw_marks[1]),
            ("Coursework 3 (0-20):", "cw3", self.student.cw_marks[2]),
            ("Exam Mark (0-100):", "exam", self.student.exam_mark)
        ]
       
        for i, (label_text, key, current_value) in enumerate(fields): #this loops through each field to create the input rows dynamically
            tk.Label(dialog_frame, text=label_text, font=(FONT_BODY, 10), bg=COLOR_PRIMARY, fg=COLOR_ACCENT).grid(row=i + 1, column=0, padx=5, pady=3, sticky='w')
            entry = ttk.Entry(dialog_frame, font=(FONT_BODY, 10))#creates an entry box for user input
            entry.insert(0, str(current_value)) #pre-fill the entry box with the students current data
            entry.grid(row=i + 1, column=1, padx=5, pady=3, sticky='ew') #places the entry next to the label
            self.entries[key] = entry #store the entry widget in the dictionary
           
        return self.entries["name"] 


    def validate(self):
        try:
            new_name = self.entries['name'].get().strip()
            if not new_name:
                messagebox.showwarning("Invalid Input", "Student Name cannot be empty.")
                return False


            cw_marks = [int(self.entries[f'cw{i}'].get()) for i in range(1, 4)] #converts all the coursework marks to integers
            exam_mark = int(self.entries['exam'].get()) #converts exam mark to an integer
           
            for mark in cw_marks:     #validates each coursework mark
                if not (0 <= mark <= 20):         #checks if within the range I've placed
                    messagebox.showwarning("Invalid Input", "Coursework marks must be between 0 and 20.")
                    return False
           
            if not (0 <= exam_mark <= 100):    #validates exam mark range
                messagebox.showwarning("Invalid Input", "Exam mark must be between 0 and 100.")
                return False
           
            self.new_data = (new_name, cw_marks, exam_mark) #store validated values for use in apply()
            return True
           
        except ValueError:        #happens if the user types letters instead of numbers
            messagebox.showwarning("Invalid Input", "Marks must be valid integers.")
            return False


    def apply(self):
        new_name, new_cw_marks, new_exam_mark = self.new_data
       
        self.student.name = new_name   #updates students name
        self.student.cw_marks = new_cw_marks     #updates coursework marks
        self.student.exam_mark = new_exam_mark      #updates exam mark
       
        self.student.total_cw_mark = sum(self.student.cw_marks) #this recalculates the coursework total
        self.student.overall_total = self.student.total_cw_mark + self.student.exam_mark #recalculates overall total
        self.student.overall_percentage = (self.student.overall_total / TOTAL_OVERALL_MARKS) * 100 #recalculate percentage
        self.student.grade = self.student._calculate_grade()      #recalculate grade
       
        if self.save_callback():    #saves the updated record to the file
            messagebox.showinfo("Success", f"Record for {self.student.name} updated and file saved.")


    def buttonbox(self):
        box = tk.Frame(self, bg=self.master.cget('bg'))  #this part creates a container for the buttons
       
        ok_button = tk.Button(box, text="Update Record", width=15, command=self.ok, default=tk.ACTIVE,      #this is the button where to confirm and update the record
                              bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'), relief='flat')
        ok_button.pack(side="left", padx=5, pady=5)
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel,       #the button to cancel the update
                                  bg=COLOR_ACCENT, fg=COLOR_TEXT_DARK, font=(FONT_BODY, SIZE_BUTTON, 'bold'), relief='flat')
        cancel_button.pack(side="right", padx=5, pady=5)
       
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
       
        box.pack(fill='x')


if __name__ == "__main__":    #this will ensure that the program will run only when executed directly
    root = tk.Tk()
    app = StudentRecordsDataRn(root)
    root.mainloop()
