import tkinter as tk
from PIL import Image, ImageTk
import random

# Initialize the main window
root = tk.Tk()
root.title("Scissors Paper Rock")
root.iconbitmap("icon.ico")
root.resizable(False, False)

# Set window dimensions and position
window_width = 600
window_height = 720
root.geometry(f"{window_width}x{window_height}")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 4
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set the background color of the root window
root.configure(bg="black")

# Configure grid layout
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Initialize game variables
round_counter = 0
user_score = 0
computer_score = 0

# Function to display image
def show_image(image_path):
    width = 100
    height = 100
    image = Image.open(image_path)
    image = image.resize((width, height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    return photo

# Custom dialog class for displaying messages with images
class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, message, image_path):
        super().__init__(parent)
        self.title(title)
        self.geometry("280x220")
        self.iconbitmap("icon.ico")
        self.resizable(False, False)
        self.configure(bg="grey")  # Set background color of the dialog to grey

        # Center the dialog on the main window and move it up on the y-axis
        self.update_idletasks()
        dialog_width = 280
        dialog_height = 220
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2 + 150  # Move dialog box down by 150 pixels
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

        # Display the message
        message_label = tk.Label(self, text=message, font=("Arial", 14), bg="grey", fg="white")
        message_label.pack(pady=10)

        # Display the image
        image = show_image(image_path)
        image_label = tk.Label(self, image=image, bg="grey")
        image_label.image = image
        image_label.pack(pady=10)

        # Play Again button to close the dialog
        play_again_button = tk.Button(self, text="Play Again", command=self.destroy, bg="grey", fg="white", cursor="hand2")
        play_again_button.pack(pady=10)

        # Make the dialog modal
        self.transient(parent)  # Set the dialog as a transient window
        self.grab_set()         # Grab all input focus

        # Wait for the dialog to be closed
        self.wait_window(self)

# Function to handle game logic
def play(user_choice):
    global round_counter, user_score, computer_score

    if round_counter >= 20:
        over_image = show_image("over.png")
        image_label.config(image=over_image)
        image_label.image = over_image  # Keep a reference to the image
        if user_score == computer_score:
            final_message = "Draw!"
            lose_image_path = "draw.png"
            CustomDialog(root, "Game Over", final_message, lose_image_path)
        elif user_score > computer_score:
            final_message = "Congratulations on your victory!"
            badge_image_path = f"badge.png"
            CustomDialog(root, "Game Over", final_message, badge_image_path)
        else:
            final_message = "Nice try!"
            lose_image_path = "lose.png"
            CustomDialog(root, "Game Over", final_message, lose_image_path)

        round_counter = 0
        user_score = 0
        computer_score = 0
        round_label.config(text=f"Round: {round_counter}")
        score_label.config(text=f"Score - Computer: {computer_score} | You: {user_score}")
        user_label.config(text="")
        computer_label.config(text="")
        image_label.config(image=start_image)
        image_label.image = start_image
        user_image_label.config(image=None)
        computer_image_label.config(image=None)
        return

    computer_choice = random.choice(["scissor", "paper", "rock"])

    # Load user choice image
    user_image = show_image(f"{user_choice}.png")
    computer_image = show_image(f"{computer_choice}.png")

    if computer_choice == user_choice:
        result_image = show_image(f"draw.png")
    elif (user_choice == "scissor" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "rock" and computer_choice == "scissor"):
        result_image = show_image(f"win.png")
        user_score += 1
    else:
        result_image = show_image(f"lose.png")
        computer_score += 1

    round_counter += 1

    computer_label.config(text="Computer\n\n" + computer_choice)
    user_label.config(text="You\n\n" + user_choice)

    # Update labels with the images
    image_label.config(image=result_image)
    image_label.image = result_image
    user_image_label.config(image=user_image)
    user_image_label.image = user_image
    computer_image_label.config(image=computer_image)
    computer_image_label.image = computer_image

    # Update round and score display
    round_label.config(text=f"Round: {round_counter}")
    score_label.config(text=f"Score - Computer: {computer_score} | You: {user_score}")

# Create and place widgets
game_title = tk.Label(root, text="Scissors Paper Rock", fg="white", bg="black", font=("Arial", 24))
game_title.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

scissors_btn = tk.Button(root, text="Scissors", width=15, bd=0, bg="light blue", pady=5, cursor="hand2", command=lambda: play("scissor"))
scissors_btn.grid(row=1, column=0, padx=8, pady=20, sticky="nsew")

paper_btn = tk.Button(root, text="Paper", width=15, bd=0, bg="silver", pady=5, cursor="hand2", command=lambda: play("paper"))
paper_btn.grid(row=1, column=1, padx=8, pady=20, sticky="nsew")

rock_btn = tk.Button(root, text="Rock", width=15, bd=0, bg="pink", pady=5, cursor="hand2", command=lambda: play("rock"))
rock_btn.grid(row=1, column=2, padx=8, pady=20, sticky="nsew")

# Labels for images
computer_label = tk.Label(root, text="", font=("Arial", 18), fg="white", bg="black")
computer_label.grid(row=2, column=0, pady=20, sticky="nsew")

start_image = show_image("spr.png")
image_label = tk.Label(root, image=start_image, bg="black")
image_label.grid(row=2, column=1, pady=20, sticky="nsew")

user_label = tk.Label(root, text="", font=("Arial", 18), fg="white", bg="black")
user_label.grid(row=2, column=2, pady=20, sticky="nsew")

computer_image_label = tk.Label(root, image=None, bg="black")
computer_image_label.grid(row=3, column=0, pady=20, sticky="nsew")

user_image_label = tk.Label(root, image=None, bg="black")
user_image_label.grid(row=3, column=2, pady=20, sticky="nsew")

# Labels for round and score
round_label = tk.Label(root, text="Round: 0", font=("Arial", 18), fg="white", bg="black")
round_label.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")

score_label = tk.Label(root, text="Score - Computer: 0 | You: 0", font=("Arial", 18), fg="white", bg="black")
score_label.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

# Start the main loop
root.mainloop()
