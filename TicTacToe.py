import tkinter as tk
from tkinter import messagebox

# List of available colors
color_list = ["lightpink", "lightcoral", "lightsalmon", "lightgoldenrodyellow", "lightcyan", "lightsteelblue", "lightblue", "lightskyblue", "lightseagreen", "lightgreen"]
players_list = []

# region Classes
''' Classes '''
# Create Players
class players:
    def __init__(self, name, sign, turn, color):
        self.name = name
        self.sign = sign
        self.turn = turn
        self.color = color
        players_list.append(self)

    def set_next_player_turn(self):
        for i in range(len(players_list)):
            if players_list[i] == self:
                next_index = (i + 1) % len(players_list)  # Wrap around to the first player if at the end
                players_list[next_index].turn = True

    def move(self, button):
        button.config(text=self.sign, bg=self.color, state="disabled")
        self.turn = False
        self.set_next_player_turn() 
        if(check_winner(self, buttons)):
            self.win()
        elif(check_draw(buttons)):
            destroy_window(tictactoeWindow, buttons)
            setup_resultWindow()

    def win(self):
        destroy_window(tictactoeWindow, buttons)
        setup_resultWindow(self)
# endregion

# region Windows
''' Window functions'''   
# Function to destroy a window
def destroy_window(window, list=None):
    window.destroy()
    if(list!=None): list.clear()

# Function to creat a window
def creat_window(title, geometry):
    window = tk.Tk()
    window.title(title)
    window.geometry(geometry)
    window.config(bg="dimgray")
    return window

# Create the player selection window
def setup_playerSelectionWindow():
    global playerSelectionWindow
    playerSelectionWindow = creat_window("Name and Color Selection", "370x300")

    # Configure the grid to center the button
    for i in [0, 11]:
        expand_column(playerSelectionWindow, i, 1)

    """ Player 1 """
    # Labels 
    add_label(playerSelectionWindow, "Player 1: Enter Name and Choose Color", 0)
    # Entry fields for player name
    player1_name_entry = add_entry(playerSelectionWindow, 1)
    # Color buttons
    add_colorButtons(playerSelectionWindow, player1_name_entry, 2)

    """ Player 2 """
    # Labels 
    add_label(playerSelectionWindow, "Player 2: Enter Name and Choose Color", 3)
    # Entry fields for player name
    player2_name_entry = add_entry(playerSelectionWindow, 4)
    # Color buttons
    add_colorButtons(playerSelectionWindow, player2_name_entry, 5)

    # game version check buttons
    def toggle_checkbuttons(selected):
        if selected == "basic":
            ultimate_var.set(not ultimate_var.get())  # Uncheck the ULTIMATE button
            basic_var.set(not ultimate_var.get())
        elif selected == "ultimate":
            basic_var.set(not basic_var.get())  # Uncheck the ULTIMATE button
            ultimate_var.set(not basic_var.get())
    # BASIC Checkbutton
    basic_var = tk.IntVar(value=1)
    basic_check = tk.Checkbutton(playerSelectionWindow, text="BASIC", variable=basic_var, 
                              command=lambda: toggle_checkbuttons("basic"))
    basic_check.grid(row=6, column=1, columnspan=5, padx=10, pady=10)

    # ULTIMATE Checkbutton
    ultimate_var = tk.IntVar(value=0)
    ultimate_check = tk.Checkbutton(playerSelectionWindow, text="ULTIMATE!", variable=ultimate_var, 
                                 command=lambda: toggle_checkbuttons("ultimate"))
    ultimate_check.grid(row=6, column=6, columnspan=5, padx=10, pady=10)

    # Confirm button to check the inputs and proceed
    confirm_button = tk.Button(playerSelectionWindow, bg="lightsteelblue", text="Confirm", font=("Arial", 12))
    confirm_button.config(command=lambda: confirm_selection(player1_name_entry, player2_name_entry, basic_var.get()))
    confirm_button.grid(row=7, column=1, columnspan=10, pady=10)

    # Start the Tkinter event loop
    playerSelectionWindow.mainloop()

# Function to set up the TicTacToe window
def setup_TicTacToeWindow():
    global tictactoeWindow
    tictactoeWindow = creat_window("TicTacToe", "270x290")
    tictactoeWindow.resizable(False, False) # Make the window size unchangeable

    global buttons
    buttons = []
    # Create a 3x3 grid of buttons
    for row in range(3):
        for col in range(3):
            # Create a button, with text and command to handle clicks
            ticButton = tk.Button(tictactoeWindow, text=f"*", 
                            width=10, height=5)  # Adjust size as needed
            # Assign the button click function with reference to the button itself
            ticButton.config(command=lambda b=ticButton: ticButton_click(b))
            # Place the button in the grid
            ticButton.grid(row=row, column=col, padx=5, pady=5)  # Add padding around the buttons
            # Store the button reference in the list
            buttons.append(ticButton)

    tictactoeWindow.mainloop() # start the main event loop

# Function to set up the window when TicTacToe is finished
def setup_resultWindow(player=None):
    global resultWindow
    resultWindow = creat_window("Result", "230x180")
    if(player==None): label = tk.Label(resultWindow, text="DRAW!", font="arial") 
    else: label = tk.Label(resultWindow, text=player.name+" won!", bg=player.color, font="arial")
    label.grid(row=1, column=1, columnspan=2, ipadx=10, ipady=20, pady=10)  # pady is padding around the label

    buttonReplay = tk.Button(resultWindow, text=f"Replay", 
                            width=12, height=3, bg="lightyellow")  
    buttonReplay.config(command=lambda: buttonReplay_click())
    buttonReplay.grid(row=2, column=1, padx=10, pady=10)  # Add padding around the buttons
    
    buttonNewPlayers = tk.Button(resultWindow, text=f"New Players", 
                            width=12, height=3, bg="lightgray", 
                            command=lambda: buttonNewPlayers_clicked())  
    buttonNewPlayers.grid(row=2, column=2, padx=10, pady=10)  # Add padding around the buttons
    # Configure the grid to center the button
    for i in [0, 3]:
        expand_row(resultWindow, i, 1)
        expand_column(resultWindow, i, 1)
# endregion

# region Button clicks
''' Button click functions '''
# Function to handle button clicks
def colorButton_click(clicked_colorButton, entry):
    entry.config(bg=clicked_colorButton.cget("bg"))

    # Function to check whether the players have entered names and selected unique colors
def confirm_selection(player1_name_entry, player2_name_entry, version):
    player1_name = player1_name_entry.get()
    player2_name = player2_name_entry.get()
    player1_color = player1_name_entry.cget("bg")
    player2_color = player2_name_entry.cget("bg")

    if not player1_name or not player2_name:
        messagebox.showerror("Error", "Both players must enter a name.")
    elif player1_color == player2_color:
        messagebox.showerror("Error", "Both players must choose different colors.")
    elif version:
        global player1, player2
        player1 = players(player1_name, "X", True, player1_color)
        player2 = players(player2_name, "O", False, player2_color)
        destroy_window(playerSelectionWindow)
        setup_TicTacToeWindow()
    else:
        messagebox.showerror("Error", "This mode is not implemented yet.")

def ticButton_click(button):
    player1.move(button) if player1.turn else player2.move(button)

def buttonReplay_click():
    destroy_window(resultWindow, buttons)
    setup_TicTacToeWindow()

def buttonNewPlayers_clicked():
    destroy_window(resultWindow, players_list)
    setup_playerSelectionWindow()
# endregion

# region TicTacToe mechanics
''' TicTacToe mechanics functions '''
# Function to check if there's a winner
def check_winner(player, buttons):
    # Check rows
    for i in range(3):
        if(all(button.cget('text') == player.sign for button in buttons[i*3:i*3+3])):
            return True
    # Check columns
    for i in range(3):
        if(all(button.cget('text') == player.sign for button in [buttons[i], buttons[i+3], buttons[i+6]])):
            return True
    # Check diagonals    
    if(all(button.cget('text') == player.sign for button in [buttons[0], buttons[4], buttons[8]])):
        return True
    if(all(button.cget('text') == player.sign for button in [buttons[2], buttons[4], buttons[6]])):
        return True
    # no winner
    return False

# Function to check if there's a draw
def check_draw(buttons):
    if(all(button.cget('state') == "disabled" for button in buttons)): return True
    else: return False
# endregion

# region UI elements
''' GUI functions '''
# Function to ad label 
def add_label(window, text, row):
    label = tk.Label(window, bg=window.cget("bg"), fg="lightblue", text=text, font=("Arial", 12))
    label.grid(row=row, column=1, columnspan=10, pady=10, sticky="nsew")

# Function to ad entry field
def add_entry(window, row):
    entry = tk.Entry(window, bg=window.cget("bg"), font=("Arial", 10), width=30)
    entry.grid(row=row, column=1, columnspan=10, pady=5, sticky="nsew")
    return entry

# Function to ad color buttons
def add_colorButtons(window, entry, row):
    for i in range(10):
        colorButton = tk.Button(window, width=2, bg=color_list[i])
        colorButton.config(command=lambda b=colorButton, e=entry: colorButton_click(b,e))
        colorButton.grid(row=row, column=i+1, padx=2)  

# Function to make column expandable
def expand_row(window, number, weight):
    window.grid_rowconfigure(number, weight=weight)  # Allow row to expand

# Function to make column expandable
def expand_column(window, number, weight):
    window.grid_columnconfigure(number, weight=weight)  # Allow row to expand
# endregion

# Start up -----------------------------------------------------------------------------------
setup_playerSelectionWindow()
