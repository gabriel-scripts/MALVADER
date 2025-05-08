import tkinter

window = tkinter.Tk()
window.title("Login")
window.geometry("980x720")

window.configure(bg="lightblue")    

window.resizable(False, False)

mainframe = tkinter.Frame(window, padding="3 3 12 12", bg="lightblue")
mainframe.grid(column=0, row=0, sticky=(tkinter.W, tkinter.E, tkinter.N, tkinter.S))
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

window.title("Login")

window.button1 = tkinter.Button(window, text="Funcionário", width=20, height=2, bg="blue", fg="white")
window.button2 = tkinter.Button(window, text="Cliente", width=20, height=2, bg="blue", fg="white")
window.button2 = tkinter.Button(window, text="Sair", width=20, height=2, bg="blue", fg="white")

window.mainloop()