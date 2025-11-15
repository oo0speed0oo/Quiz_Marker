import tkinter as tk
from main_menu import show_main_menu

def main():
    main_window = tk.Tk()
    main_window.title("Quiz Marker")
    main_window.geometry("400x600")
    main_window.configure(bg="white")

    # Show the main menu first
    show_main_menu(main_window)

    main_window.mainloop()

if __name__ == "__main__":
    main()
