import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import pymysql


# static method


def DbConnect():
    global cursor
    db = pymysql.connect("localhost", "root", "", "dbpos")
    cursor = db.cursor()
    # testing area
    # sql = "SELECT VERSION()"
    # cursor.execute(sql)
    # data = cursor.fetchone()
    # print("Database version: %s " % data)
    # cursor.close()


def user_admin(username, password):
    try:
        sql = f"select usertype_id from tbluser where uname = '{username}' and password = '{password}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result is not None:
            userType = [[i[0]] for i in result]
            usrtype = userType[0][0]
            if usrtype == 1:
                ok = mb.showinfo("", "Admin")
                if ok:
                    print("admin")

            elif usrtype == 2:
                ok = mb.showinfo("", "User")
                if ok:
                    print("User")
    except:
        mb.showerror("Error in Sql", "Incorrect Username or Password")


# class Login / app
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # initialize variable
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # calling Center_Window method
        self.Center_window(250, 150)

        # style and configure
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 12))

        # frames
        self.frame = ttk.Frame(self, relief='raised')
        self.frame_btn = ttk.Frame(self)

        # first Login
        self.loginBtn = ttk.Button(self.frame_btn, text='Login', cursor='hand2', command=self.Login, style='my.TButton')
        self.registerBtn = ttk.Button(self.frame_btn, text='Register', cursor='hand2', style='my.TButton')

        # layout for frame_btn and its child
        self.loginBtn.pack()
        self.registerBtn.pack(pady=5)
        self.frame_btn.pack(expand='yes')

        # frame
        self.psswd_en = ttk.Entry(self.frame)
        self.usrname = ttk.Label(self.frame, text='Username')
        self.psswd = ttk.Label(self.frame, text='Password')
        self.usrname_en = ttk.Entry(self.frame, textvariable=self.username)
        self.psswd_en = ttk.Entry(self.frame, textvariable=self.password, show="*")
        self.loginBtn_go = ttk.Button(self.frame, text='Login', cursor='hand2', command=self.Login_auth)
        self.backTo = ttk.Button(self.frame, text='Back', cursor='hand2', command=self.BckTo)
        self.title("Al Dave Program")

    def Center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.resizable(0, 0)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))

    def Login(self):
        self.frame_btn.pack_forget()
        self.usrname.grid(row=0, column=0, ipady='5', padx='5', pady='10')
        self.psswd.grid(row=1, column=0, ipady='5', padx='5')
        self.usrname_en.grid(row=0, column=1)
        self.psswd_en.grid(row=1, column=1)
        self.loginBtn_go.grid(row=2, column=1)
        self.backTo.grid(row=2, column=0, padx=7)
        self.frame.pack(expand='yes', ipady=5, ipadx=15)

    def Login_auth(self):
        usr = self.username.get().strip()
        pss = self.password.get().strip()
        if usr == '' and pss == '':
            mb.showerror("Input", "No input")

        else:
            user_admin(usr, pss)
            self.password.set('')
            self.username.set('')

    def BckTo(self):
        self.frame.pack_forget()
        self.frame_btn.pack(expand='yes')


if __name__ == "__main__":
    dbError = True
    try:
        DbConnect()
    except:
        mb.showerror("Database Error", "there's error while connecting to the database"
                                       "\nplease check (db_connect)")
        dbError = False
    if dbError:
        a = App()
        a.mainloop()
