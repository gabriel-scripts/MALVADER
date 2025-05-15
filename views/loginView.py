import tkinter
from tkinter import ttk

def login():
    window = tkinter.Tk()
    window.title("Login")
    window.geometry("980x720")
    window.configure(bg="lightblue")    
    window.resizable(False, False)

    mainframe = ttk.Frame(window, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tkinter.W, tkinter.E, tkinter.N, tkinter.S))
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    window.button1 = tkinter.Button(window, text="Funcionário", width=20, height=2, bg="blue", fg="white")
    window.button2 = tkinter.Button(window, text="Cliente", width=20, height=2, bg="blue", fg="white")
    window.button3 = tkinter.Button(window, text="Sair", width=20, height=2, bg="blue", fg="white")

    window.button1.grid(column=0, row=0, padx=10, pady=20)
    window.button2.grid(column=0, row=1, padx=10, pady=20)
    window.button3.grid(column=0, row=2, padx=10, pady=20)

    window.mainloop()
