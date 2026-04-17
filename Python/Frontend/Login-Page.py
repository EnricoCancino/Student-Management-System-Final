from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def login():
    if userEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    if userEntry.get() != "admin" or passwordEntry.get() != "password":
        messagebox.showerror("Error", "Invalid username or password.")
    elif userEntry.get() == "admin" and passwordEntry.get() == "password":
        messagebox.showinfo("Success", "Login successful!")
        window.destroy()
        import StudentManagementSystem
    else:
        messagebox.showerror("Error", "Please, Enter correct credentials")
        
    
window=Tk()
window.geometry("1280x700+0+0")
window.resizable(False, False)
window.title("Login Page")

#Login Page
image = Image.open("Frontend/PhotoHouse/Background-python.jpg")
image = image.resize((1280, 700), Image.Resampling.LANCZOS)
backgroundImage = ImageTk.PhotoImage(image)

bgLabel=Label(window,image=backgroundImage)
bgLabel.place(x=0,y=0)

#Login Frame
loginFrame = Frame(window, bg="white")
loginFrame.place(x=400, y=150)

logoImage = PhotoImage(file="Frontend/PhotoHouse/Students.png")

logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

#Entries
user_logo_raw = Image.open("Frontend/PhotoHouse/Userlogo.png")
user_logo_raw = user_logo_raw.resize((30, 30), Image.Resampling.LANCZOS)

usernameImage = ImageTk.PhotoImage(user_logo_raw)
usernameLabel = Label(loginFrame, image=usernameImage, text="Username", compound=LEFT, font=("Italic", 15))
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

userEntry=Entry(loginFrame, font=("Italic", 15), bd=5, fg="Royalblue")
userEntry.grid(row=1, column=1, pady=10, padx=20)

password_logo_raw = Image.open("Frontend/PhotoHouse/Locklogo.png")
password_logo_raw = password_logo_raw.resize((30, 30), Image.Resampling.LANCZOS)

passwordImage = ImageTk.PhotoImage(password_logo_raw)
passwordLabel = Label(loginFrame, image=passwordImage, text="Password", compound=LEFT, font=("Italic", 15))
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry=Entry(loginFrame, font=("Italic", 15), bd=5, fg="Royalblue")
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text="LOGIN", font=("Italic", 15), fg="white" , bg="Cornflowerblue", activeforeground="white", cursor="hand2", command=login)
loginButton.grid(row=3, column=1, pady=10)

window.mainloop()