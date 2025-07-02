from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Please enter username and password')
    elif usernameEntry.get() == 'rvs' and passwordEntry.get() == hardcoded_password:
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import duplicate
    else:
        messagebox.showerror('Error', 'Please enter correct values')

def forgot_password():
    def reset_password():
        new_password = newPasswordEntry.get().strip()
        if not new_password:
            messagebox.showerror('Error', 'Please enter a new password', parent=forgot_window)
            return
        global hardcoded_password
        hardcoded_password = new_password
        messagebox.showinfo('Success', f'Password reset successfully', parent=forgot_window)
        forgot_window.destroy()

    forgot_window = Toplevel()
    forgot_window.title('Forgot Password')
    forgot_window.geometry('400x300+500+200')
    forgot_window.grab_set()
    forgot_window.resizable(False, False)

    Label(forgot_window, text='Forgot Password', font=('times new roman', 20, 'bold'), bg='white').pack(pady=10)
    Label(forgot_window, text='Enter New Password:', font=('times new roman', 16), bg='white').pack(pady=10)
    newPasswordEntry = Entry(forgot_window, font=('times new roman', 16), bd=5, fg='royalblue')
    newPasswordEntry.pack(pady=10)
    Button(forgot_window, text='Reset Password', font=('times new roman', 14, 'bold'), width=15,
           fg='white', bg='cornflowerblue', cursor='hand2', command=reset_password).pack(pady=10)

window = Tk()
window.geometry('1280x700+0+0')
window.title('Login System of Students Management')
window.resizable(False, False)

try:
    backgroundImage = ImageTk.PhotoImage(file='cd.jpg')
    cdLabel = Label(window, image=backgroundImage)
except TclError:
    backgroundImage = None
    cdLabel = Label(window, text="Background Image Not Found", font=('times new roman', 20, 'bold'), bg='red', fg='white')
cdLabel.place(x=0, y=0)

loginFrame = Frame(window, bg='white')
loginFrame.place(x=350, y=200)

try:
    logoImage = PhotoImage(file='logo.png')
    logoLabel = Label(loginFrame, image=logoImage, bg='white')
except TclError:
    logoImage = None
    logoLabel = Label(loginFrame, text="Logo Image Not Found", font=('times new roman', 20, 'bold'), bg='white', fg='red')
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

try:
    usernameImage = PhotoImage(file='user.png')
    usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                          font=('times new roman', 20, 'bold'), bg='white')
except TclError:
    usernameImage = None
    usernameLabel = Label(loginFrame, text='Username', font=('times new roman', 20, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

try:
    passwordImage = PhotoImage(file='password.png')
    passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                          font=('times new roman', 20, 'bold'), bg='white')
except TclError:
    passwordImage = None
    passwordLabel = Label(loginFrame, text='Password', font=('times new roman', 20, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=15,
                    fg='white', bg='cornflowerblue', cursor='hand2', command=login)
loginButton.grid(row=3, column=1, pady=10)

forgotButton = Button(loginFrame, text='Forgot Password', font=('times new roman', 14, 'bold'), width=15,
                     fg='white', bg='cornflowerblue', cursor='hand2', command=forgot_password)
forgotButton.grid(row=4, column=1, pady=10)

window.backgroundImage = backgroundImage
loginFrame.logoImage = logoImage
loginFrame.usernameImage = usernameImage
loginFrame.passwordImage = passwordImage

# Hardcoded password for validation
hardcoded_password = '9215'

window.mainloop()