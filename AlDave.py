import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import pymysql

# global sql
select_all = "select * from tbluser"


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


def Center_window_sub(s, width, height):
    screen_width = s.winfo_screenwidth()
    screen_height = s.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    s.resizable(0, 0)
    s.geometry("%dx%d+%d+%d" % (width, height, x, y))


def cancel_edit():
    popupwindow.destroy()


def cancel_edit_add():
    add_Frame.destroy()


class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        # calling Center_Window method and title

        self.Center_window(1200, 700)
        self.title("Al Dave Program")

        # variables
        self.search_en = tk.StringVar()
        self.username_reg_var = tk.StringVar()
        self.password_reg_var = tk.StringVar()
        self.fn_reg_var = tk.StringVar()
        self.ln_reg_var = tk.StringVar()
        self.cn_reg_var = tk.StringVar()
        # for usertype variable / radio button
        self.userType = tk.IntVar()
        self.status = tk.IntVar()

        # style and configure
        s = ttk.Style()
        s.configure('my1.TButton', font=('Helvetica', 14), background='#e7505a', foreground='#e7505a')
        s.configure('my.TButton', font=('Helvetica', 12), background='#e7505a', foreground='#e7505a')
        s.configure('my2.TButton', font=('Helvetica', 11))
        s.configure('my3.TLabel', font=('Helvetica', 11))
        s.configure('my3.TEntry', font=('Helvetica', 11))
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold')
                        , foreground='green')  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        # ####Admin Side####
        # ****sidebar****
        # labelFrame
        # side
        self.sidebar = ttk.LabelFrame(self, text='Menu List')
        # main
        self.main = tk.Frame(self)
        # main's sub frames
        self.m_top = ttk.LabelFrame(self.main, text='Control')
        self.m_body = ttk.LabelFrame(self.main, text='Account')
        # top
        self.top = ttk.LabelFrame(self, text='top')

        # sidebar attributes
        self.add_user_btn = ttk.Button(self.sidebar, text='Add User', style='my.TButton', cursor='hand2',
                                       command=self.Add_new_user)
        self.add_edit_btn = ttk.Button(self.sidebar, text='Edit', style='my.TButton', cursor='hand2',
                                       command=self.edit_auth)
        self.add_changePass_btn = ttk.Button(self.sidebar, text='Password', style='my.TButton', cursor='hand2')

        # main attributes
        # top
        self.m_reset_btn = ttk.Button(self.m_top, text='Reset', style='my.TButton', )
        self.m_delete_btn = ttk.Button(self.m_top, text='Delete', style='my.TButton', command=self.delete)
        self.m_search_btn = ttk.Button(self.m_top, text='Search', style='my.TButton', )
        self.m_search_en = ttk.Entry(self.m_top, textvariable=self.search_en, font=('Helvetica', 12))

        # body
        # Scrollbar
        scrollbarx = tk.Scrollbar(self.m_body, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(self.m_body, orient=tk.VERTICAL)

        # treeview
        self.tree1 = ttk.Treeview(self.m_body,
                                  columns=("user_id", "uname", "fname", "lname", "contact_no", "usertype", "status"),
                                  selectmode="extended", height=15, yscrollcommand=scrollbary.set,
                                  xscrollcommand=scrollbarx.set, style="mystyle.Treeview")
        # self.tree1.tag_configure('odd', background='#E8E8E8')
        self.tree1.tag_configure('even', background='#DFDFDF')
        self.tree1.bind("<Motion>", self.mycallback)
        self.tree1.bind("<Double-Button>", self.edit_auth)
        self.last_focus = None

        scrollbary.config(command=self.tree1.yview)
        scrollbary.pack(side='right', fill='y')
        scrollbarx.config(command=self.tree1.xview)
        scrollbarx.pack(side='bottom', fill='x')

        # tree heading
        self.tree1.heading('user_id', text="User id", anchor=tk.W)
        self.tree1.heading('uname', text="Username", anchor=tk.W)
        self.tree1.heading('fname', text="First Name", anchor=tk.W)
        self.tree1.heading('lname', text="Last Name", anchor=tk.W)
        self.tree1.heading('contact_no', text="Contact", anchor=tk.W)
        self.tree1.heading('usertype', text="User Type", anchor=tk.W)
        self.tree1.heading('status', text="Status", anchor=tk.W)

        # tree column
        self.tree1.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree1.column('#1', stretch=tk.NO, minwidth=0, width=100)
        self.tree1.column('#2', stretch=tk.NO, minwidth=0, width=130)
        self.tree1.column('#3', stretch=tk.NO, minwidth=0, width=130)
        self.tree1.column('#4', stretch=tk.NO, minwidth=0, width=130)
        self.tree1.column('#5', stretch=tk.NO, minwidth=0, width=130)
        self.tree1.column('#6', stretch=tk.NO, minwidth=0, width=130)
        self.tree1.column('#7', stretch=tk.NO, minwidth=0, width=130)

        cursor.execute(select_all)
        res = cursor.fetchall()
        treeInsertVal = [[i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]] for i in res]
        # inserting value
        cnt = 0
        for row in treeInsertVal:
            usr_tp = 'admin' if row[6] == 1 else 'user'
            act = 'active' if row[7] == 1 else 'inactive'
            if row[7] == 1:
                self.tree1.insert('', "end", cnt, text="",
                                  values=(row[0], row[1], row[3], row[4], row[5], usr_tp, act))

            cnt = cnt + 1

        # (main) attributes frame layout
        # top
        self.m_reset_btn.pack(side='left', padx=20)
        self.m_delete_btn.pack(side='right', padx=20)
        self.m_search_btn.pack(side='left', padx=20)
        self.m_search_en.pack(side='left', padx=20)

        # body
        self.tree1.pack(expand=0, fill='both')

        # top attributes
        self.add_user_btn2 = ttk.Button(self.top, text='Logout', style='my1.TButton')
        self.add_pos_btn2 = ttk.Button(self.top, text='POS', style='my1.TButton')

        # layout attributes

        # sidebar layout
        self.add_user_btn.pack(pady=10)
        self.add_edit_btn.pack(pady=10)
        self.add_changePass_btn.pack(pady=10)

        # main layout
        self.m_reset_btn.pack()
        # main's sub layout
        self.m_top.pack(fill='both', expand=0, ipady=20)
        self.m_body.pack(expand=0, pady=35, fill='both')

        # top layout
        self.add_user_btn2.pack(side='right', padx=15)
        self.add_pos_btn2.pack(side='left', padx=15)

        # frame layout
        # top frame
        self.top.pack(fill='both', ipady=5, pady=10)

        # side frame
        self.sidebar.pack(fill='y', side='left', expand=0, padx=50, ipadx=20, pady=20)

        # main frame
        self.main.pack(fill='x', padx=50, pady=20)

    # function
    def Center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.resizable(0, 0)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # edit and update
    def edit_auth(self, event=None):
        try:
            global s_user_id
            curItem = self.tree1.focus()
            aya = self.tree1.item(curItem)
            s_user_id = aya['values'][0]
            sql = f"select uname, fname, lname, contact_no, usertype_id, active from tbluser" \
                  f" where User_Id='{s_user_id}'"
            cursor.execute(sql)
            res_edit = cursor.fetchone()
            self.username_reg_var.set(f'{res_edit[0]}')
            self.fn_reg_var.set(f'{res_edit[1]}')
            self.ln_reg_var.set(f'{res_edit[2]}')
            self.cn_reg_var.set(f'{res_edit[3]}')
            # for usertype variable / radio button
            self.userType.set(f'{res_edit[4]}')
            self.status.set(f'{res_edit[5]}')
            self.edit()
        except:
            mb.showerror("Error Found!", "Please Select Row")

    def edit(self):
        global popupwindow
        popupwindow = tk.Toplevel(self)

        popupwindow.grab_set()
        popupwindow.focus_set()
        Center_window_sub(popupwindow, 300, 300)
        wrap = tk.Frame(popupwindow, bd=8, relief='flat')
        user_type = ttk.LabelFrame(wrap, text='User Type')
        status = ttk.LabelFrame(wrap, text='Status')
        # radio button area
        rbAdmin = ttk.Radiobutton(user_type, text='Admin', variable=self.userType,
                                  value=1)
        rbUser = ttk.Radiobutton(user_type, text='User', variable=self.userType, value=2)
        active_r = ttk.Radiobutton(status, text='Enable', variable=self.status,
                                   value=1)
        inactive_r = ttk.Radiobutton(status, text='Disable', variable=self.status, value=0)
        #         # label area
        usrname_reg = ttk.Label(wrap, text='Username', style='my3.TLabel', )
        fn_reg = ttk.Label(wrap, text='First Name', style='my3.TLabel')
        ln_reg = ttk.Label(wrap, text='Last Name', style='my3.TLabel')
        cn_reg = ttk.Label(wrap, text='Contact Number', style='my3.TLabel')
        # entry area
        usrname_reg_en = ttk.Entry(wrap, textvariable=self.username_reg_var, style='my3.TEntry')
        fn_reg_en = ttk.Entry(wrap, textvariable=self.fn_reg_var, style='my3.TEntry')
        ln_reg_en = ttk.Entry(wrap, textvariable=self.ln_reg_var, style='my3.TEntry')
        cn_reg_en = ttk.Entry(wrap, textvariable=self.cn_reg_var, style='my3.TEntry')
        registerBtn_go = ttk.Button(wrap, text='Update', cursor='hand2', style='my2.TButton', command=self.update)
        registerBackTo = ttk.Button(wrap, text='Cancel', cursor='hand2', style='my2.TButton', command=cancel_edit)

        # radio button layout area
        rbAdmin.grid(row=0, column=1, ipady='3', padx='19')
        rbUser.grid(row=0, column=0, ipady='3', padx='42')
        inactive_r.grid(row=0, column=0, ipady='3', padx='42')
        active_r.grid(row=0, column=1, ipady='3', padx='4')
        # label layout
        usrname_reg.grid(row=2, column=0, ipady='5', padx='5', sticky='e')
        fn_reg.grid(row=4, column=0, ipady='5', padx='5', sticky='e')
        ln_reg.grid(row=5, column=0, ipady='5', padx='5', sticky='e')
        cn_reg.grid(row=6, column=0, ipady='5', padx='5', sticky='e')
        # entry layout
        usrname_reg_en.grid(row=2, column=1, pady='5', padx='5')
        usrname_reg_en.focus_set()
        fn_reg_en.grid(row=4, column=1, pady='5', padx='5')
        ln_reg_en.grid(row=5, column=1, pady='5', padx='5')
        cn_reg_en.grid(row=6, column=1, pady='5', padx='5')
        registerBtn_go.grid(row=7, column=1, pady='5', padx='5')
        registerBackTo.grid(row=7, column=0, pady='5', padx='5')
        user_type.grid(row=0, columnspan=2, sticky='nswe')
        status.grid(row=1, columnspan=2, sticky='nswe', pady=10)
        wrap.pack(expand=1, fill='both', padx=10)

    def mycallback(self, event):
        _iid = self.tree1.identify_row(event.y)
        if _iid != self.last_focus:
            if self.last_focus:
                self.tree1.item(self.last_focus, tags=[])
            self.tree1.item(_iid, tags=['even'])
            self.last_focus = _iid

    def update(self):
        user = self.username_reg_var.get().strip()
        fn = self.fn_reg_var.get().strip()
        ln = self.ln_reg_var.get().strip()
        cn = self.cn_reg_var.get().strip()
        usertype = self.userType.get()
        status = self.status.get()
        if user == '' or fn == '' or ln == '' or cn == '':
            mb.showerror("", "please fill all fields")
        else:
            try:
                sql = f"update tbluser set Uname='{user}', Fname='{fn}', Lname='{ln}', Contact_no={int(cn)}, " \
                      f"UserType_Id='{usertype}', active={status}  where User_Id={s_user_id}"
                print(sql)
                cursor.execute(sql)
                db.commit()
                popupwindow.destroy()

                ##
                curItem = self.tree1.focus()
                sql = f"select User_Id, uname, fname, lname, contact_no, usertype_id, active from tbluser" \
                      f" where User_Id='{s_user_id}'"
                cursor.execute(sql)
                res = cursor.fetchone()
                usr_tp = 'admin' if res[5] == 1 else 'user'
                act = 'active' if res[6] == 1 else 'inactive'
                self.tree1.delete(curItem)
                self.tree1.insert('', curItem, curItem, text="", values=(res[0], user, fn, ln, cn
                                                                         , usr_tp, act))
            except:
                mb.showerror("Error Found!", "Contact number contain number only")

    # add new user
    def Add_new_user(self):
        global add_Frame
        self.username_reg_var.set('')
        self.password_reg_var.set('')
        self.fn_reg_var.set('')
        self.ln_reg_var.set('')
        self.cn_reg_var.set('')
        # for usertype variable / radio button
        self.userType.set(2)
        self.status.set(1)
        add_Frame = tk.Toplevel()
        add_Frame.grab_set()
        add_Frame.focus_set()
        Center_window_sub(add_Frame, 300, 350)
        wrap = ttk.Frame(add_Frame)
        user_type = ttk.LabelFrame(wrap, text='User Type')
        status = ttk.LabelFrame(wrap, text='Status')
        # radio button area
        rbAdmin = ttk.Radiobutton(user_type, text='Admin', variable=self.userType,
                                  value=1)
        rbUser = ttk.Radiobutton(user_type, text='User', variable=self.userType, value=2)
        active_r = ttk.Radiobutton(status, text='Enable', variable=self.status,
                                   value=1)
        inactive_r = ttk.Radiobutton(status, text='Disable', variable=self.status, value=0)
        #         # label area
        usrname_reg = ttk.Label(wrap, text='Username', style='my3.TLabel', )
        pass_reg = ttk.Label(wrap, text='Password', style='my3.TLabel', )
        fn_reg = ttk.Label(wrap, text='First Name', style='my3.TLabel')
        ln_reg = ttk.Label(wrap, text='Last Name', style='my3.TLabel')
        cn_reg = ttk.Label(wrap, text='Contact Number', style='my3.TLabel')
        # entry area
        usrname_reg_en = ttk.Entry(wrap, textvariable=self.username_reg_var, style='my3.TEntry')
        pass_reg_en = ttk.Entry(wrap, textvariable=self.username_reg_var, style='my3.TEntry')
        fn_reg_en = ttk.Entry(wrap, textvariable=self.fn_reg_var, style='my3.TEntry')
        ln_reg_en = ttk.Entry(wrap, textvariable=self.ln_reg_var, style='my3.TEntry')
        cn_reg_en = ttk.Entry(wrap, textvariable=self.cn_reg_var, style='my3.TEntry')
        registerBtn_go = ttk.Button(wrap, text='Submit', cursor='hand2', style='my2.TButton')
        registerBackTo = ttk.Button(wrap, text='Cancel', cursor='hand2', style='my2.TButton', command=cancel_edit_add)

        # radio button layout area
        rbAdmin.grid(row=0, column=1, ipady='3', padx='19')
        rbUser.grid(row=0, column=0, ipady='3', padx='42')
        inactive_r.grid(row=0, column=0, ipady='3', padx='42')
        active_r.grid(row=0, column=1, ipady='3', padx='4')
        # label layout
        usrname_reg.grid(row=2, column=0, ipady='5', padx='5', sticky='e')
        pass_reg.grid(row=3, column=0, ipady='5', padx='5', sticky='e')
        fn_reg.grid(row=4, column=0, ipady='5', padx='5', sticky='e')
        ln_reg.grid(row=5, column=0, ipady='5', padx='5', sticky='e')
        cn_reg.grid(row=6, column=0, ipady='5', padx='5', sticky='e')
        # entry layout
        usrname_reg_en.grid(row=2, column=1, pady='5', padx='5')
        usrname_reg_en.focus_set()
        pass_reg_en.grid(row=3, column=1, pady='5', padx='5')
        fn_reg_en.grid(row=4, column=1, pady='5', padx='5')
        ln_reg_en.grid(row=5, column=1, pady='5', padx='5')
        cn_reg_en.grid(row=6, column=1, pady='5', padx='5')
        registerBtn_go.grid(row=7, column=1, pady='5', padx='5')
        registerBackTo.grid(row=7, column=0, pady='5', padx='5')
        user_type.grid(row=0, columnspan=2, sticky='nswe')
        status.grid(row=1, columnspan=2, sticky='nswe', pady=10)
        wrap.pack(expand=1, fill='both', padx=20, pady=20)

    def delete(self):
        curItem = self.tree1.focus()
        self.tree1.delete(curItem)

if __name__ == "__main__":
    dbError = True
    try:
        DbConnect()
    except:
        mb.showerror("Database Error", "there's error while connecting to the database"
                                       "\nplease check (db_connect)")
        dbError = False
    if dbError:
        a = MainFrame()
        a.mainloop()
        db.close()
