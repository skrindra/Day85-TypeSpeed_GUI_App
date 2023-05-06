from tkinter import *
from PIL import ImageTk, Image, ImageFont
from tkinter import messagebox, ttk
from sample_text import text_dict


BG_COLOR = "khaki"
TEXT_OPTIONS = [key for key in text_dict]


class TypeSpeedApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x1000")
        self.master.title("Type Speed App")
        self.master.config(bg=BG_COLOR)

        # ----------- CREATING THE WIDGETS---------#
        # ----The Header Widget-----
        self.header_canvas = Canvas(master, width=800, height=250, highlightthickness=0)
        self.side_bar_canvas = Canvas(self.master, width=245, height=750, bg="green", highlightthickness=0)
        self.header_image = Image.open("kb_image.jpeg")  # replace with your own image file
        self.header_image = self.header_image.resize((800, 250))
        self.header_bg = ImageTk.PhotoImage(self.header_image)
        self.header_canvas.create_image(0, 0, anchor=NW, image=self.header_bg)
        self.header_label = Label(master, text="ZinGo Type Speed", bg="White", font=("Courier", 40))

        # Display Text
        self.canvas = Canvas(master, width=500, height=250, highlightbackground="blue", highlightthickness=2, bg="pink")
        self.instruct_text = Label(master, text="Start Typing the above text ...", bg=BG_COLOR, font=("Courier", 20))
        self.display_text = Text(self.master, height=8, width=34, wrap='word', state='normal', font=("Arial", 25))

        # Score canvas
        self.score_canvas = Canvas(master, width=235, height=235, bg="green", highlightthickness=0)
        self.score_canvas.create_oval(10, 10, 230, 230, fill="black")
        self.timer = Label(master, font=("Courier", 50), width=4, height=2, text="60", bg="black", fg="white")

        # Accuracy
        self.acc_canvas = Canvas(self.master, width=235, height=235, bg="green", highlightthickness=0)
        self.acc_canvas.create_oval(10, 10, 230, 230, fill="black")
        self.acc_canvas.place(x=560, y=500)
        self.acc_text = Label(self.master, text=f"Accuracy", font=("Courier", 35), fg="green", bg="black")
        self.acc_text.place(x=592, y=580)

        # Text Selection dropdown
        self.selected_text_topic = StringVar()
        self.selected_text_topic.set("  ----Select a Sample Text---")
        self.text_dropdown = ttk.Combobox(self.master, textvariable=self.selected_text_topic, values=TEXT_OPTIONS,
                                          state="readonly")
        self.text_dropdown.bind("<<ComboboxSelected>>", self.on_select_text)

        # Editable Textbox
        self.text_box = Text(master, width=71, height=10)
        self.text_box.focus_set()
        # the start_timer function gets triggered when any key is pressed
        self.text_box.bind("<Key>", self.start_timer)

        # start button
        self.start_button = Button(self.master, text="START", width=6, height=3, command=self.start,
                                   highlightthickness=2,
                                   highlightbackground="green",
                                   )
        self.start_button.configure(bg="black")

        # ------- POSITIONING OF WIDGETS -----------
        self.header_canvas.place(x=0, y=0)
        self.side_bar_canvas.place(x=556, y=250)
        self.header_label.place(x=235, y=40)
        self.canvas.place(x=47, y=160)
        self.display_text.place(x=53.5, y=168)
        self.text_dropdown.place(x=560, y=160)
        self.score_canvas.place(x=560, y=251)
        self.timer.place(x=618, y=317)
        self.instruct_text.place(x=47, y=425)
        self.text_box.place(x=47, y=497)
        self.start_button.place(x=260, y=660)

        # -------- INITIALIZING VARIABLES ---------
        self.actual_text = None
        self.time_left = 60
        self.timer_status = False
        self.user_input = None

    # ================ METHODS =============
    def on_select_text(self, event=None):
        """Enabled when user selects a sample text"""
        self.text_box.delete("1.0", "end-1c")
        self.text_box.focus_set()
        self.display_text.delete("1.0", "end-1c")
        selected_text = self.selected_text_topic.get()
        self.actual_text = text_dict[selected_text]
        self.display_text.insert(END, self.actual_text)

    def start(self):
        """Enabled when START button is clicked"""
        self.timer_status = False
        self.actual_text = None  # Read-only sample text
        self.time_left = 60  # reset time left to 60 seconds
        self.selected_text_topic.set("  ----select a text---")
        self.display_text.delete("1.0", "end-1c")
        self.text_box.delete("1.0", "end-1c")
        self.acc_text.config(text="Accuracy")
        self.timer.config(text="60", fg="white")

    def start_timer(self, event):
        """The function initiates the timer countdown
                and updates the timer text"""

        if self.actual_text is None:
            messagebox.showwarning("OOPs!", "Please Select a Sample Text")
            self.text_box.delete("1.0", "end-1c")

        # elif not self.started and self.actual_text:
        elif not self.timer_status and self.actual_text:
            self.timer_status = True
            # start the timer only if a key is pressed inside the text box
            self.countdown()

    def countdown(self):
        """The countdown process"""
        if self.time_left >= 1:
            if self.time_left < 10:
                self.timer.config(text=f"0{str(self.time_left)}")
            else:
                self.timer.config(text=f"{str(self.time_left)}")

            if self.timer_status:
                self.time_left -= 1
                # call the countdown function after each second
                self.master.after(1000, self.countdown)
        if self.time_left == 0:
            self.get_result()

    def get_result(self):
        """Calculates the WPM and accuracy & displays on window"""
        text_typed = self.text_box.get("1.0", "end-1c")
        word_count = len(text_typed.split())
        elapsed_time = 60-self.time_left
        try:
            wpm = round((word_count / elapsed_time) * 60)
            accuracy = self.calculate_accuracy(text_typed)
            # update the accuracy
            self.timer.config(text=f"{wpm}\nWPM", fg="yellow", font=("Courier", 50))
            self.acc_text.config(text=f"Accuracy\n{accuracy}%")
        except ZeroDivisionError:
            self.timer.config(text=f"0\nWPM", fg="yellow", font=("Courier", 50))
            self.acc_text.config(text=f"Accuracy\n0%")

    def calculate_accuracy(self, text_typed):
        correct_chars = sum([1 for i, c in enumerate(text_typed) if c == self.actual_text[i]])
        return round((correct_chars / len(text_typed)) * 100, 2)


# Create the Tkinter window and run the app
root = Tk()
app = TypeSpeedApp(root)
root.mainloop()
