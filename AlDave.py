import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import pymysql


# static method


# for database connection
def DbConnect():
    global cursor, db
    db = pymysql.connect("localhost", "root", "", "dbpos")
    cursor = db.cursor()
    # testing area
    # sql = "SELECT VERSION()"
    # cursor.execute(sql)
    # data = cursor.fetchone()
    # print("Database version: %s " % data)
    # cursor.close()


# to check if the user login is admin or not
def user_admin(username, password):
    try:  # try except
        sql = f"select usertype_id, active from tbluser where uname = '{username}' and password = '{password}'"  # sql
        cursor.execute(sql)  # execute the sql statement
        result = cursor.fetchall()  # get the result
        userType = [[i[0], i[1]] for i in result]
        usrtype = userType[0][0]
        act = userType[0][1]
        if usrtype == 1 and act == 1:
            ok = mb.showinfo("", "Admin")
            if ok:
                print("admin")
        elif usrtype == 2 and act == 1:
            ok = mb.showinfo("", "User")
            if ok:
                print("User")
        else:
            mb.showwarning('', "Account is inactive")
    except:
        mb.showerror("Error in Sql", "Incorrect Username or Password")


def register_new_user(un, pd, fn, ln, cn):
    try:
        sql = 'select * from tbluser'
        cursor.execute(sql)
        res = cursor.fetchall()
        userType = [True for i in res if un == i[1]]
        if not userType:
            sql = f"insert into tbluser (Uname, Password, Fname, Lname, Contact_no, UserType_Id, active) values ('{un}', '{pd}', '{fn}', '{ln}', {cn}, '{2}', {'0'})"
            try:
                # execute the command
                cursor.execute(sql)
                # commit changes in the database
                db.commit()
            except:
                # roll back in case there's any error
                db.rollback()
        else:
            mb.showwarning("", "Username is already taken")
    except:
        mb.showerror("", "there's error in (register_new_user)")


# validations


# class Login / app
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # initialize variable
        # for login variable
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        # for usertype variable / radio button
        self.userType = tk.IntVar()
        self.userType.set(2)
        # for register variable
        self.username_reg_var = tk.StringVar()
        self.password_reg_var = tk.StringVar()
        self.fn_reg_var = tk.StringVar()
        self.ln_reg_var = tk.StringVar()
        self.cn_reg_var = tk.StringVar()

        # calling Center_Window method and title
        self.Center_window(250, 150)
        self.title("Al Dave Program")

        # style and configure
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 12))

        # frames
        self.frame = ttk.Frame(self, relief='raised')
        self.frame_btn = ttk.Frame(self)
        self.frame_register = ttk.LabelFrame(self, text='Register Form')

        # first Login
        self.loginBtn = ttk.Button(self.frame_btn, text='Login', cursor='hand2', command=self.Login, style='my.TButton')
        self.registerBtn = ttk.Button(self.frame_btn, text='Register', cursor='hand2', style='my.TButton',
                                      command=self.Register)

        # layout for frame_btn and its child
        self.loginBtn.pack()
        self.registerBtn.pack(pady=5)
        self.frame_btn.pack(expand='yes')

        # frame for login
        self.psswd_en = ttk.Entry(self.frame)
        self.usrname = ttk.Label(self.frame, text='Username')
        self.psswd = ttk.Label(self.frame, text='Password')
        self.usrname_en = ttk.Entry(self.frame, textvariable=self.username)
        self.psswd_en = ttk.Entry(self.frame, textvariable=self.password, show="*")
        self.loginBtn_go = ttk.Button(self.frame, text='Login', cursor='hand2', command=self.Login_auth)
        self.backTo = ttk.Button(self.frame, text='Back', cursor='hand2', command=self.BckTo)

        # frame for register
        # radio button area
        self.rbAdmin = ttk.Radiobutton(self.frame_register, text='Admin', variable=self.userType,
                                       value=1, state='disabled')
        self.rbUser = ttk.Radiobutton(self.frame_register, text='User', variable=self.userType, value=2)
        # separator
        self.sep = ttk.Label(self.frame_register, text='-----------------User Only--------------')
        # label area
        self.usrname_reg = ttk.Label(self.frame_register, text='Username')
        self.psswd_reg = ttk.Label(self.frame_register, text='Password')
        self.fn_reg = ttk.Label(self.frame_register, text='First Name')
        self.ln_reg = ttk.Label(self.frame_register, text='Last Name')
        self.cn_reg = ttk.Label(self.frame_register, text='Contact Number')
        # entry area
        self.usrname_reg_en = ttk.Entry(self.frame_register, textvariable=self.username_reg_var)
        self.psswrd_reg_en = ttk.Entry(self.frame_register, textvariable=self.password_reg_var)
        self.fn_reg_en = ttk.Entry(self.frame_register, textvariable=self.fn_reg_var)
        self.ln_reg_en = ttk.Entry(self.frame_register, textvariable=self.ln_reg_var)
        self.cn_reg_en = ttk.Entry(self.frame_register, textvariable=self.cn_reg_var)
        self.registerBtn_go = ttk.Button(self.frame_register, text='Signup', cursor='hand2', command=self.Register_auth)
        self.registerBackTo = ttk.Button(self.frame_register, text='Back', cursor='hand2', command=self.BckTo1)

    def Center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.resizable(0, 0)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))

    def Login(self):
        self.frame_btn.pack_forget()
        self.usrname.grid(row=0, column=0, ipady='5', padx='5', pady='10', sticky='e')
        self.psswd.grid(row=1, column=0, ipady='5', padx='5', sticky='e')
        self.usrname_en.grid(row=0, column=1)
        self.psswd_en.grid(row=1, column=1)
        self.loginBtn_go.grid(row=2, column=1)
        self.backTo.grid(row=2, column=0, padx=7)
        self.frame.pack(expand='yes', ipady=5, ipadx=15)

    def Register(self):
        self.frame_btn.pack_forget()
        self.Center_window(300, 320)  # set the size of the frame
        # radio button layout area
        self.rbAdmin.grid(row=0, column=1, ipady='5', padx='5')
        self.rbUser.grid(row=0, column=0, ipady='5', padx='5')
        # line separator
        self.sep.grid(row=1, column=0, columnspan=2)
        # label layout
        self.usrname_reg.grid(row=2, column=0, ipady='5', padx='5', sticky='e')
        self.psswd_reg.grid(row=3, column=0, ipady='5', padx='5', sticky='e')
        self.fn_reg.grid(row=4, column=0, ipady='5', padx='5', sticky='e')
        self.ln_reg.grid(row=5, column=0, ipady='5', padx='5', sticky='e')
        self.cn_reg.grid(row=6, column=0, ipady='5', padx='5', sticky='e')
        # entry layout
        self.usrname_reg_en.grid(row=2, column=1, pady='5', padx='5')
        self.psswrd_reg_en.grid(row=3, column=1, pady='5', padx='5')
        self.fn_reg_en.grid(row=4, column=1, pady='5', padx='5')
        self.ln_reg_en.grid(row=5, column=1, pady='5', padx='5')
        self.cn_reg_en.grid(row=6, column=1, pady='5', padx='5')
        self.registerBtn_go.grid(row=7, column=1, pady='5', padx='5')
        self.registerBackTo.grid(row=7, column=0, pady='5', padx='5')
        self.frame_register.pack(expand='yes')

    def Login_auth(self):
        usr = self.username.get().strip()
        pss = self.password.get().strip()
        if usr == '' and pss == '':
            mb.showerror("Input", "No input")
        else:
            user_admin(usr, pss)
            self.password.set('')
            self.username.set('')

    def Register_auth(self):
        un = self.username_reg_var.get().strip()
        pd = self.password_reg_var.get().strip()
        fn = self.fn_reg_var.get().strip()
        ln = self.ln_reg_var.get().strip()
        cn = self.cn_reg_var.get().strip()
        if un == '' and pd == '' and fn == '' and ln == '':
            mb.showerror("", "No input")
        else:
            try:
                register_new_user(un, pd, fn, ln, int(cn))
                ok = mb.showinfo("", "Successfully Added")
                self.username_reg_var.set('')
                self.password_reg_var.set('')
                self.fn_reg_var.set('')
                self.ln_reg_var.set('')
                self.cn_reg_var.set('')
                if ok:
                    self.BckTo1()
            except:
                mb.showerror("", "number input only for contact number")

    def BckTo(self):
        self.Center_window(250, 150)
        self.frame.pack_forget()
        self.frame_btn.pack(expand='yes')

    def BckTo1(self):
        self.Center_window(250, 150)
        self.frame_register.pack_forget()
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
