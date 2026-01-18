import tkinter as tk
from main_menu import MainMenu  # Updated import

def main():
    main_window = tk.Tk()
    main_window.title("Quiz Marker")
    main_window.geometry("800x800")
    main_window.configure(bg="white")

    # Initialize the Main Menu class.
    # This now handles the logic of whether to skip the unit selector or not.
    MainMenu(main_window)

    main_window.mainloop()

if __name__ == "__main__":
    main()