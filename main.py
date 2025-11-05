import tkinter as tk
from main_menu import show_main_menu

def main():
    root = tk.Tk()
    root.title("Quiz Marker")
    root.geometry("400x500")
    root.configure(bg="white")

    # Show the main menu first
    show_main_menu(root)

    root.mainloop()

if __name__ == "__main__":
    main()
