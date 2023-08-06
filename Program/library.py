from tkinter import *
from tkinter import messagebox as msg, ttk
from PIL import Image, ImageTk
import webbrowser as web
import mysql.connector as conn
import password_hasher as ph
import re
import os
import json
from isbnlib import meta
from isbnlib.registry import bibformatters
import requests
from urllib.request import urlopen
from datetime import datetime
from io import BytesIO
import threading
import validators
import random
import string

try:
    connection = conn.connect(
        host="sql10.freesqldatabase.com",
        user="sql10618972",
        password="fBNE8Pwvag",
        database="sql10618972"
    )
    # using a buffered cursor, the connector fetches ALL rows and takes one from the connector
    cursor = connection.cursor(buffered=True)
except:
    print("[CONNECTION ERROR]")
    exit()

PATH = os.path.dirname(__file__)
hasher = ph.PasswordHasher()
windows = {}
BGCOLOR = "#7895CB"
ENTRY = "#EEEEEE"
LABEL = "#777777"


class Common():
    def __init__(self, root):
        self.root = root
        self.SCREEN = (root.winfo_screenwidth(), root.winfo_screenheight())

    def set_screen(self, wl=60, back=True):
        _logo = Image.open(
            f"{PATH}/../static/Personal/Images/display/logo.png")
        _logo = _logo.resize((wl, wl))
        self.LOGO = ImageTk.PhotoImage(_logo)
        _back = Image.open(
            f"{PATH}/../static/Personal/Images/display/back.png")
        _back = _back.resize((50, 50))
        self.BACK = ImageTk.PhotoImage(_back)
        self.root.iconphoto(0, self.LOGO)
        self.root.minsize(self.SCREEN[0], self.SCREEN[1])
        self.root.after(0, lambda: self.root.state("zoomed"))
        back_btn = Button(self.root, image=self.BACK,
                          command=self.back, cursor="hand2")
        if back:
            back_btn.place(x=0, y=0)

    def close_window(self, x):
        windows[x].destroy()
        del windows[x]

    def close_all_windows(self):
        while len(windows):
            self.close_window(list(windows.keys())[0])

    def back(self):
        self.close_all_windows()
        Dashboard()

    def refresh(self):
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            user_id = json.load(cookie)[0]['id']
        cursor.execute(
            f"select * from logged_users where id={user_id}")
        arr = cursor.fetchall()[0]
        user = {'id': arr[0], 'name': arr[1], 'email': arr[2], 'username': arr[6],
                'avatar': arr[7], 'phone': arr[8]}
        library = {
            'author': arr[9], 'category': arr[10], 'language': arr[11], 'publisher': arr[12]}
        library_offline = {'library_name': arr[13], 'library_email': arr[14],
                           'library_phone': arr[15], 'library_address': arr[16], 'library_url': arr[17]}
        with open(f'{PATH}/../static/Personal/Data/cookie.json', 'w') as cookie:
            cookie.write(json.dumps(
                [user, library, library_offline], indent=4))
        with open(f'{PATH}/../static/Personal/Data/logged.txt', 'w') as f:
            f.write(arr[5])

    def address_packer(self, *consts):
        add1_lbl, add2_lbl, ent3x, ent3y, dist_lbl, stt_lbl, pin_lbl, country_lbl = consts
        add1_lbl.grid(row=0, column=0, sticky=W)
        self.root.add1_ent.grid(row=1, column=0, pady=2)
        add2_lbl.grid(row=2, column=0, sticky=W)
        self.root.add2_ent.grid(row=3, column=0, pady=2)
        ent3x.grid(row=4, column=0, sticky=W)
        ent3y.grid(row=5, column=0, sticky=W)
        dist_lbl.grid(row=0, column=0, sticky=W)
        self.root.dist_ent.grid(row=1, column=0, pady=2)
        Label(ent3x, width=1, bg="white").grid(row=0, column=1)
        Label(ent3x, width=1, bg="white").grid(row=1, column=1, pady=2)
        stt_lbl.grid(row=0, column=2, sticky=W)
        self.root.stt_ent.grid(row=1, column=2, pady=2)
        pin_lbl.grid(row=0, column=0, sticky=W)
        self.root.pin_ent.grid(row=1, column=0, pady=2)
        Label(ent3y, width=1, bg="white").grid(row=0, column=1)
        Label(ent3y, width=1, bg="white").grid(row=1, column=1, pady=2)
        country_lbl.grid(row=0, column=2, sticky=W)
        self.root.country_ent.grid(row=1, column=2, pady=2)

    def load_toggle(self, size=70):
        _right = Image.open(
            f"{PATH}/../static/Personal/Images/display/right.png")
        _right = _right.resize((size, size))
        _left = _right.rotate(180)
        self.AFTER = ImageTk.PhotoImage(_right)
        self.BEFORE = ImageTk.PhotoImage(_left)

    def avatar_toggle(self, dir, task):
        size = len(os.listdir(f"{PATH}/../static/Personal/Images/{task}s"))-1
        self.root.pic = self.root.pic+dir
        if self.root.pic < 0:
            self.root.pic = size
        elif self.root.pic > size:
            self.root.pic = 0
        _avatar = Image.open(
            f"{PATH}/../static/Personal/Images/{task}s/{task}_{self.root.pic}.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)
        self.root.avatar.config(image=AVATAR)
        self.root.avatar.image = AVATAR


class Opener(Tk):
    def __init__(self):
        super().__init__()
        windows["opener"] = self
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            try:
                cookies = json.load(cookie)
            except:
                pass
            else:
                cursor.execute(
                    f"select user_hash from logged_users where username = '{cookies[0]['username']}'")
                user_hash = cursor.fetchone()[0]
                with open(f'{PATH}/../static/Personal/Data/logged.txt') as log:
                    if log.read() == user_hash:
                        Common(self).close_all_windows()
                        Dashboard()

        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.config(bg=BGCOLOR)
        root.title("Shelfmate")
        common = Common(root)
        common.set_screen(back=False)
        frame1 = Frame(root, bg=BGCOLOR)
        frame1.pack(ipady=100)
        frame2 = Frame(root, bg=BGCOLOR)
        frame2.pack()

        img = Label(frame1, image=common.LOGO, bg=BGCOLOR)
        img.image = common.LOGO
        name = Label(frame1, text="Shelfmate",
                     font="Arial 30", bg=BGCOLOR, fg="white")
        img.grid(row=0, column=0)
        name.grid(row=0, column=1)
        log_btn = Button(frame2, text="Log In", font=("Arial", 15), bg="#AAC8A7",
                         cursor="hand2", activebackground="#C3EDC0", bd=0, padx=10, pady=5, command=lambda: Login())
        sign_btn = Button(frame2, text="Sign Up", font=("Arial", 15), bg="#AAC8A7",
                          cursor="hand2", activebackground="#C3EDC0", bd=0, padx=10, pady=5, command=lambda: Signup())
        gap_v = Label(frame2, height=3, bg=BGCOLOR)
        log_btn.grid(row=1, column=0)
        gap_h = Label(frame2, width=10, bg=BGCOLOR)
        gap_v.grid(row=0, column=0)
        gap_h.grid(row=1, column=1)
        sign_btn.grid(row=1, column=2)

        link = Button(root, text="Try our website for a better interface..", command=lambda: web.open_new_tab("https://shelfmate.onrender.com"),
                      bg=BGCOLOR, bd=0, activebackground=BGCOLOR, activeforeground="red", font=("Arial", 15, "underline"), cursor="hand2")
        link.pack(side=BOTTOM, ipady=30)

        root.protocol("WM_DELETE_WINDOW",
                      lambda: common.close_window("opener"))


class Login(Tk):
    def __init__(self):
        if "login" not in windows:
            super().__init__()
            common = Common(self)
            self.BGCOLOR = "#333333"
            self.title("Log In")
            self.geometry("600x400")
            self.resizable(0, 0)
            self.config(bg=self.BGCOLOR)
            windows["login"] = self
            self.create_screen()
            self.protocol("WM_DELETE_WINDOW",
                          lambda: common.close_window("login"))
            self.mainloop()

    def create_screen(root):
        frame = Frame(root, bg=root.BGCOLOR)
        login_label = Label(root, text="Login", bg=root.BGCOLOR,
                            fg="#FF3399", font=("Arial", 30))
        username_label = Label(
            frame, text="Username/\nEmail", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.username = Entry(frame, font=("Arial", 16))
        root.username.focus()
        root.password = Entry(frame, show="*", font=("Arial", 16))
        password_label = Label(
            frame, text="Password", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        login_button = Button(root, text="Login", bg="#FF3399", fg="#FFFFFF", font=(
            "Arial", 16), command=root.login)
        login_label.pack(ipady=30)
        frame.pack()
        gap1 = Label(frame, width=5, bg=root.BGCOLOR)
        gap2 = Label(frame, width=5, bg=root.BGCOLOR)
        username_label.grid(row=0, column=0)
        gap1.grid(row=0, column=1)
        root.username.grid(row=0, column=2, pady=20)
        password_label.grid(row=1, column=0)
        gap2.grid(row=1, column=1)
        root.password.grid(row=1, column=2, pady=20)
        Label(root, pady=10, bg=root.BGCOLOR).pack()
        login_button.pack()
        root.username.bind("<Return>", root.login)
        root.password.bind("<Return>", root.login)

    def login(root, ev=0):
        username = root.username.get()
        password = root.password.get()
        if username and password:
            cursor.execute(
                "select username, email, pswd_hash from logged_users")
            all_users = cursor.fetchall()

            if "@" in username:
                code = 1
                typeof = "email"
            else:
                code = 0
                typeof = "username"
            for data in all_users:
                if username == data[code]:
                    unq = int(re.findall('\$(\d+)\$', data[2])[0])
                    hashed = hasher.get_hash(password, unq)
                    if hashed == data[2]:
                        cursor.execute(
                            f"select * from logged_users where {typeof}='{username}'")
                        arr = cursor.fetchall()[0]
                        user = {'id': arr[0], 'name': arr[1], 'email': arr[2], 'username': arr[6],
                                'avatar': arr[7], 'phone': arr[8]}
                        library = {
                            'author': arr[9], 'category': arr[10], 'language': arr[11], 'publisher': arr[12]}
                        library_offline = {'library_name': arr[13], 'library_email': arr[14],
                                           'library_phone': arr[15], 'library_address': arr[16], 'library_url': arr[17]}

                        Common(root).close_all_windows()
                        with open(f'{PATH}/../static/Personal/Data/cookie.json', 'w') as cookie:
                            cookie.write(json.dumps(
                                [user, library, library_offline], indent=4))
                        with open(f'{PATH}/../static/Personal/Data/logged.txt', 'w') as f:
                            f.write(arr[5])
                        Dashboard()
                    else:
                        msg.showwarning("Shelfmate", "Wrong Password!")
                    break

                elif data == all_users[-1]:
                    msg.showwarning("Shelfmate", "Unregistered User!")
                    break
        else:
            msg.showwarning("Shelfmate", "Fill all the fields!")


class Signup(Tk):
    def __init__(self):
        if "signup" not in windows:
            super().__init__()
            common = Common(self)
            self.BGCOLOR = "#333333"
            self.title("Sign Up")
            self.geometry("600x600")
            self.resizable(0, 0)
            self.config(bg=self.BGCOLOR)
            windows["signup"] = self
            self.create_screen()
            self.protocol("WM_DELETE_WINDOW",
                          lambda: common.close_window("signup"))
            self.mainloop()

    def create_screen(root):
        frame = Frame(root, bg=root.BGCOLOR)
        signup_label = Label(root, text="Signup",
                             bg=root.BGCOLOR, fg="#FF3399", font=("Arial", 30))
        email_label = Label(frame, text="Email", bg=root.BGCOLOR,
                            fg="#FFFFFF", font=("Arial", 16))
        root.email = Entry(frame, font=("Arial", 16))
        root.email.focus()
        name_label = Label(frame, text="Full Name",
                           bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.name = Entry(frame, font=("Arial", 16))
        username_label = Label(
            frame, text="Username", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.username = Entry(frame, font=("Arial", 16))
        password_label = Label(
            frame, text="Password", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.password = Entry(frame, show="*", font=("Arial", 16))
        confirm_label = Label(frame, text="Confirm Password",
                              bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.confirm = Entry(frame, show="*", font=("Arial", 16))
        signup_btn = Button(root, text="Signup", bg="#FF3399",
                            fg="#FFFFFF", font=("Arial", 16), command=root.signup)
        signup_label.pack(ipady=30)
        frame.pack()
        email_label.grid(row=0, column=0)
        Label(frame, width=5, bg=root.BGCOLOR).grid(row=0, column=1)
        root.email.grid(row=0, column=2, pady=20)
        name_label.grid(row=1, column=0)
        Label(frame, width=5, bg=root.BGCOLOR).grid(row=1, column=1)
        root.name.grid(row=1, column=2, pady=20)
        username_label.grid(row=2, column=0)
        Label(frame, width=5, bg=root.BGCOLOR).grid(row=2, column=1)
        root.username.grid(row=2, column=2, pady=20)
        password_label.grid(row=3, column=0)
        Label(frame, width=5, bg=root.BGCOLOR).grid(row=3, column=1)
        root.password.grid(row=3, column=2, pady=20)
        confirm_label.grid(row=5, column=0)
        Label(frame, width=5, bg=root.BGCOLOR).grid(row=5, column=1)
        root.confirm.grid(row=5, column=2, pady=20)
        Label(root, pady=10, bg=root.BGCOLOR).pack()
        signup_btn.pack()
        root.email.bind("<Return>", root.signup)
        root.name.bind("<Return>", root.signup)
        root.username.bind("<Return>", root.signup)
        root.password.bind("<Return>", root.signup)
        root.confirm.bind("<Return>", root.signup)

    def signup(root, ev=0):
        email = root.email.get()
        name = root.name.get()
        username = root.username.get()
        password = root.password.get()
        confirm = root.confirm.get()

        if email and name and username and password and confirm:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                if re.search(r"[^a-zA-Z0-9_\s]", username) == None:
                    if len(username) >= 5:
                        if len(password) >= 8:
                            if password == confirm:
                                cursor.execute(
                                    f'''insert into logged_users (name, email, pswd_hash, date_created, user_hash, username, avatar, phone, author, category, language, publisher, library_name, library_email, library_phone, library_address, library_url)
                                    values ("{name}", "{email}", "{hasher.get_hash(password)}", "{datetime.now()}", "{hasher.get_hash(username)}", "{username}", 0, "", "", "", "", "", "", "", "", "", "");''')
                                connection.commit()

                                Common(root).close_all_windows()
                                msg.showinfo(
                                    "Success", "You have signed up successfully. Now log in to your account.")
                                Login()
                            else:
                                msg.showwarning(
                                    "Shelfmate", "Password and confirmation doesn't match!")
                        else:
                            msg.showwarning(
                                "Shelfmate", "Password must be atleast 8 characters!")
                    else:
                        msg.showwarning(
                            "Shelfmate", "Username should be atleast 5 characters!")
                else:
                    msg.showwarning(
                        "Shelfmate", "Username can contain numbers, letters and underscore (_) only!")
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all the fields!")


class Dashboard(Tk):
    def __init__(self):
        super().__init__()
        self.common = Common(self)
        windows["dashboard"] = self
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        cursor.execute(
            f"select user_hash from logged_users where username = '{cookies[0]['username']}'")
        user_hash = cursor.fetchone()[0]
        with open(f'{PATH}/../static/Personal/Data/logged.txt') as log:
            if log.read() != user_hash:
                self.common.close_all_windows()
                Opener()

        self.user = cookies[0]
        self.library = cookies[1]
        self.library_offline = cookies[2]
        self.title(f"Dashboard @{self.user['username']}")

        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common.set_screen(30, False)
        root.config(bg=BGCOLOR)

        _avatar = Image.open(
            f"{PATH}/../static/Personal/Images/avatars/avatar_{root.user['avatar']}.png")
        _avatar = _avatar.resize((60, 60))
        AVATAR = ImageTk.PhotoImage(_avatar)

        frame1 = Frame(root, pady=20, bg=BGCOLOR, cursor="hand2")
        avatar = Label(frame1, image=AVATAR)
        avatar.image = AVATAR
        user_head = Label(frame1, text=root.user["name"], font=(
            "Verdana", 20), padx=20, bg=BGCOLOR, fg="white")
        log_out_btn = Button(root, text="Log Out", font="Comicsans 14",
                             fg="red", cursor="hand2", padx=10, pady=5, command=root.log_out)

        frame2 = Frame(root, bg=BGCOLOR, pady=100)
        btn1 = Button(frame2, text="Add Resources", font=("Comicsans", 15), padx=10, pady=10, width=20,
                      activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=root.add_res)
        btn2 = Button(frame2, text="All Resources", font=("Comicsans", 15), padx=10, pady=10, width=20,
                      activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=root.all_res)
        btn3 = Button(frame2, text="Borrow Request", font=("Comicsans", 15), padx=10, pady=10,
                      width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn4 = Button(frame2, text="Check-In User", font=("Comicsans", 15), padx=10, pady=10,
                      width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn5 = Button(frame2, text="Checked-In Readers", font=("Comicsans", 15), padx=10,
                      pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn6 = Button(frame2, text="Readers History", font=("Comicsans", 15), padx=10,
                      pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn7 = Button(frame2, text="Add Member", font=("Comicsans", 15), padx=10, pady=10, width=20,
                      activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=root.add_mem)
        btn8 = Button(frame2, text="All Members", font=("Comicsans", 15), padx=10, pady=10, width=20,
                      activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=root.all_mem)
        btn9 = Button(frame2, text="Requests To Borrow", font=("Comicsans", 15), padx=10,
                      pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn10 = Button(frame2, text="Borrowed Requests", font=("Comicsans", 15), padx=10,
                       pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn11 = Button(frame2, text="Library Details", font=("Comicsans", 15), padx=10, pady=10, width=20,
                       activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=root.lib_det)
        btn12 = Button(frame2, text="Minor Settings", font=("Comicsans", 15), padx=10,
                       pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")

        frame3 = Frame(root, bg=BGCOLOR, pady=20)
        logo = Label(frame3, image=root.common.LOGO, bg=BGCOLOR)
        logo.image = root.common.LOGO
        shelf = Label(frame3, text="Shelfmate", font=(
            "Comicsans", 15), bg=BGCOLOR, fg="#2D4356", cursor="hand2")

        log_out_btn.place(x=0, y=0)
        frame1.pack()
        frame2.pack()
        frame3.pack(side=BOTTOM)
        avatar.grid(row=0, column=0)
        user_head.grid(row=0, column=1)
        for i in range(12):
            eval(f"btn{i+1}.grid(row=i//4, column=i%4)")
        logo.grid(row=0, column=0)
        shelf.grid(row=0, column=1)

        avatar.bind("<Button-1>", root.setting)
        user_head.bind("<Button-1>", root.setting)
        shelf.bind("<Button-1>",
                   lambda e: web.open_new_tab("https://shelfmate.onrender.com"))

        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("dashboard"))

    def log_out(self):
        if msg.askyesno("Shelfmate", "Do you really want to log out?"):
            with open(f'{PATH}/../static/Personal/Data/logged.txt', 'w') as log:
                log.write("")
            with open(f'{PATH}/../static/Personal/Data/cookie.json', 'w') as cookie:
                cookie.write("")
            self.common.close_all_windows()
            Opener()

    def setting(self, ev=0):
        self.common.close_all_windows()
        AccountSettings()

    def add_res(self):
        self.common.close_all_windows()
        AddResources()

    def all_res(self):
        self.common.close_all_windows()
        AllResources()

    def add_mem(self):
        self.common.close_all_windows()
        AddMembers()

    def lib_det(self):
        self.common.close_all_windows()
        LibraryDetails()

    def all_mem(self):
        self.common.close_all_windows()
        AllMembers()


class AccountSettings(Tk):
    def __init__(self):
        super().__init__()
        windows["account settings"] = self
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common = Common(root)
        root.common.set_screen()
        root.title("Account Settings")
        root.config(bg="white")
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        root.user = cookies[0]
        root.pic = root.user['avatar']
        _avatar = Image.open(
            f"{PATH}/../static/Personal/Images/avatars/avatar_{root.pic}.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)

        title = Label(root, text="Account Settings", font=(
            "Verdana", 30, "underline"), pady=50, bg="white")
        avatar_label = Label(root, text="Profile Photo",
                             font=("Arial", 10, "bold"), bg="white")

        frame0 = Frame(root, padx=50, pady=30,
                       highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=20, padx=50)
        frame2 = Frame(frame0, pady=30, bg="white")
        frame3 = Frame(frame0, pady=30, bg="white")

        root.common.load_toggle()
        left_btn = Button(frame1, image=root.common.BEFORE, bd=0, width=100,
                          cursor="hand2", command=lambda: root.common.avatar_toggle(-1, "avatar"))
        root.avatar = Label(frame1, image=AVATAR, width=100)
        right_btn = Button(frame1, image=root.common.AFTER, bd=0, width=100,
                           cursor="hand2", command=lambda: root.common.avatar_toggle(1, "avatar"))
        left_btn.image = root.common.BEFORE
        root.avatar.image = AVATAR
        right_btn.image = root.common.AFTER

        name_label = Label(frame2, text="Your Name", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.name = StringVar()
        root.name_entry = Entry(frame2, textvariable=root.name, font=(
            "Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.name.set(root.user["name"])
        root.name_entry.focus()
        username_label = Label(frame2, text="Your Username", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.username = StringVar()
        root.username_entry = Entry(frame2, textvariable=root.username, font=(
            "Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.username.set(root.user["username"])
        email_label = Label(frame2, text="Email Address",
                            font=("Arial", 10), fg=LABEL, bg="white")
        root.email = StringVar()
        root.email_entry = Entry(frame2, textvariable=root.email, font=(
            "Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.email.set(root.user["email"])
        phone_label = Label(frame2, text="Phone Number (Optional)", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.phone = StringVar()
        root.phone_entry = Entry(frame2, textvariable=root.phone, font=(
            "Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.phone.set(root.user["phone"])

        save_btn = Button(frame3, text="Save Changes", bg="#0D6EFD", fg="white", activebackground=BGCOLOR,
                          activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=root.save_changes)
        cancel_btn = Button(frame3, text="Cancel", bg="black", fg="white", activebackground="#6C757D",
                            activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=root.common.back)

        title.pack()
        avatar_label.pack()
        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        frame3.grid(row=2, column=0)
        left_btn.grid(row=0, column=0)
        root.avatar.grid(row=0, column=1)
        right_btn.grid(row=0, column=2)
        name_label.grid(row=0, column=0, sticky=W)
        Label(frame2, width=20, bg="white").grid(row=0, column=1)
        username_label.grid(row=0, column=2, sticky=W)
        root.name_entry.grid(row=1, column=0)
        Label(frame2, width=20, bg="white").grid(row=1, column=1)
        root.username_entry.grid(row=1, column=2)
        for i in range(3):
            Label(frame2, height=1, bg="white").grid(row=2, column=i)
        email_label.grid(row=3, column=0, sticky=W)
        root.email_entry.grid(row=4, column=0)
        phone_label.grid(row=3, column=2, sticky=W)
        root.phone_entry.grid(row=4, column=2)
        save_btn.grid(row=0, column=0)
        Label(frame3, width=5, bg="white").grid(row=0, column=1)
        cancel_btn.grid(row=0, column=2)

        root.name_entry.bind("<Return>", root.save_changes)
        root.username_entry.bind("<Return>", root.save_changes)
        root.email_entry.bind("<Return>", root.save_changes)
        root.phone_entry.bind("<Return>", root.save_changes)

        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("account settings"))

    def save_changes(self, ev=0):
        name = self.name.get().strip()
        username = self.username.get().strip()
        email = self.email.get()
        phone = self.phone.get().strip()

        if name and username and email:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                if re.search(r"[^a-zA-Z0-9_\s]", username) == None:
                    if len(username) >= 5:
                        if username != self.user["username"]:
                            extra = f', user_hash="{hasher.get_hash(username)}"'
                        else:
                            extra = ""
                        cursor.execute(
                            f'''update logged_users set name="{name}", username="{username}", email="{email}", avatar="{self.pic}", phone="{phone}"{extra} where id={self.user["id"]}''')
                        connection.commit()
                        self.common.refresh()
                        self.common.back()
                    else:
                        msg.showwarning("Shelfmate",
                                        "Username should be atleast 5 characters!")
                else:
                    msg.showwarning("Shelfmate",
                                    "Username can contain numbers, letters and underscore (_) only!")
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all required fields!")


class AddResources(Tk):
    def __init__(self):
        super().__init__()
        windows["add resources"] = self
        self.last_isbn = ""
        self.url = "../static/Personal/Images/display/book_cover.png"
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common = Common(root)
        root.common.set_screen()
        root.title("Add Resources")
        root.config(bg="gainsboro")
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        root.user = cookies[0]
        root.library = cookies[1]

        FRAME = Frame(root)
        frame0 = Frame(FRAME, padx=50, pady=30,
                       highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=30, bg="white")
        frame2 = Frame(frame0, bg="white")
        root.frame00 = Frame(FRAME, bg="white")
        frame01 = Frame(root.frame00, bg="white")
        frame02 = Frame(root.frame00, bg="white")

        title = Label(root, text="Add Resources", font=(
            "Verdana", 25, "underline"), pady=50, bg="gainsboro")

        isbn_label = Label(frame1, text="ISBN *", font=(
            "Arial", 13), bg="white", padx=50)
        root.isbn = StringVar()
        root.isbn_entry = Entry(frame1, textvariable=root.isbn, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.isbn_entry.focus()

        title_label = Label(frame1, text="Title *", font=(
            "Arial", 13), bg="white", padx=50)
        root.title = StringVar()
        root.title_entry = Entry(frame1, textvariable=root.title, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        edition_label = Label(frame1, text="Edition", font=(
            "Arial", 13), bg="white", padx=50)
        root.edition = StringVar()
        root.edition_entry = Entry(frame1, textvariable=root.edition, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        root.author_label = Label(frame1, text="Authors (0) *", font=(
            "Arial", 13), bg="white", padx=50, cursor="hand2")
        root.author = StringVar()
        root.author_entry = Entry(frame1, textvariable=root.author, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.author_add_btn = Button(
            frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(0))
        root.author_sel = []

        root.category_label = Label(frame1, text="Category (0) *", font=(
            "Arial", 13), bg="white", padx=50, cursor="hand2")
        root.category = StringVar()
        root.category_entry = Entry(frame1, textvariable=root.category, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.category_add_btn = Button(
            frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(1))
        root.category_sel = []

        root.publisher_label = Label(frame1, text="Publisher (0) *", font=(
            "Arial", 13), bg="white", padx=50, cursor="hand2")
        root.publisher = StringVar()
        root.publisher_entry = Entry(frame1, textvariable=root.publisher, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.publisher_add_btn = Button(
            frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(2))
        root.publisher_sel = []

        root.language_label = Label(frame1, text="Language (0) *", font=(
            "Arial", 13), bg="white", padx=50, cursor="hand2")
        root.language = StringVar()
        root.language_entry = Entry(frame1, textvariable=root.language, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.language_add_btn = Button(
            frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(3))
        root.language_sel = []

        quantity_label = Label(frame1, text="Quantity *", font=(
            "Arial", 13), bg="white", padx=50)
        root.quantity = StringVar()
        root.quantity_entry = Entry(frame1, textvariable=root.quantity, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        submit_btn = Button(frame2, text="Submit", fg="white", bg="black", activebackground="#111111",
                            activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=root.submit_form)

        root.book = Label(frame01)
        book_title_label = Label(
            frame02, font="arial 14", bg="white", text="Title: ")
        book_author_label = Label(
            frame02, font="arial 14", bg="white", text="Author: ")
        book_year_label = Label(frame02, font="arial 14",
                                bg="white", text="Year: ")
        book_publisher_label = Label(
            frame02, font="arial 14", bg="white", text="Publisher: ")
        root.book_title = Label(frame02, font="comicsans 12", bg="white")
        root.book_author = Label(frame02, font="comicsans 12", bg="white")
        root.book_year = Label(frame02, font="comicsans 12", bg="white")
        root.book_publisher = Label(frame02, font="comicsans 12", bg="white")

        title.pack()
        FRAME.pack()
        frame0.grid(row=0, column=0)
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        frame01.grid(row=0, column=0)
        frame02.grid(row=2, column=0)
        isbn_label.grid(row=0, column=0, sticky=W, pady=10)
        root.isbn_entry.grid(row=0, column=1, padx=50, pady=10)
        title_label.grid(row=1, column=0, sticky=W, pady=10)
        root.title_entry.grid(row=1, column=1, padx=50, pady=10)
        edition_label.grid(row=2, column=0, sticky=W, pady=10)
        root.edition_entry.grid(row=2, column=1, padx=50, pady=10)
        root.author_label.grid(row=3, column=0, sticky=W, pady=10)
        root.author_entry.grid(row=3, column=1, padx=50, pady=10)
        root.category_label.grid(row=4, column=0, sticky=W, pady=10)
        root.category_entry.grid(row=4, column=1, padx=50, pady=10)
        root.publisher_label.grid(row=5, column=0, sticky=W, pady=10)
        root.publisher_entry.grid(row=5, column=1, padx=50, pady=10)
        root.language_label.grid(row=6, column=0, sticky=W, pady=10)
        root.language_entry.grid(row=6, column=1, padx=50, pady=10)
        quantity_label.grid(row=7, column=0, sticky=W, pady=10)
        root.quantity_entry.grid(row=7, column=1, padx=50, pady=10)
        root.author_add_btn.grid(row=3, column=2)
        root.category_add_btn.grid(row=4, column=2)
        root.publisher_add_btn.grid(row=5, column=2)
        root.language_add_btn.grid(row=6, column=2)
        submit_btn.grid(row=0, column=0)
        root.book.grid(row=0, column=0)
        book_title_label.grid(row=1, column=0, sticky=W)
        book_author_label.grid(row=2, column=0, sticky=W)
        book_year_label.grid(row=3, column=0, sticky=W)
        book_publisher_label.grid(row=4, column=0, sticky=W)
        root.book_title.grid(row=1, column=1, sticky=W)
        root.book_author.grid(row=2, column=1, sticky=W)
        root.book_year.grid(row=3, column=1, sticky=W)
        root.book_publisher.grid(row=4, column=1, sticky=W)

        root.author_label.bind("<Button-1>", lambda e: root.view_selected(0))
        root.category_label.bind("<Button-1>", lambda e: root.view_selected(1))
        root.publisher_label.bind(
            "<Button-1>", lambda e: root.view_selected(2))
        root.language_label.bind("<Button-1>", lambda e: root.view_selected(3))
        root.author_entry.bind("<Return>", lambda e: root.add_option(0))
        root.category_entry.bind("<Return>", lambda e: root.add_option(1))
        root.publisher_entry.bind("<Return>", lambda e: root.add_option(2))
        root.language_entry.bind("<Return>", lambda e: root.add_option(3))
        root.isbn_entry.bind("<FocusOut>", root.find_book)
        root.isbn_entry.bind("<Return>", root.find_book)
        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("add resources"))

    def view_selected(self, type):
        types = ["author", "category", "publisher", "language"]
        type = types[type]
        viewer = Tk()
        common = Common(viewer)
        if type in windows:
            common.close_window(type)
        else:
            types.remove(type)
            for t in types:
                if t in windows:
                    common.close_window(t)

        windows[type] = viewer
        viewer.title(type.capitalize())
        viewer.geometry("400x200")
        viewer.resizable(0, 0)
        Label(viewer, text="Double click to delete an item",
              font="arial 10", fg="blue").pack()
        scroller = Scrollbar(viewer, width=20)
        self.tree = ttk.Treeview(
            viewer, yscrollcommand=scroller.set, column=type, show='headings', selectmode="browse")
        self.tree.column("# 1", anchor=CENTER, width=380)
        self.tree.heading("# 1", text=type.capitalize())
        for x in eval(f"self.{type}_sel"):
            self.tree.insert('', 'end', text=x, values=[x])
        scroller.config(command=self.tree.yview)
        self.tree.bind(
            "<Double-1>", lambda e: self.delete_option(e, self.tree['column'][0]))
        self.tree.pack(side=LEFT, fill=Y)
        scroller.pack(side=RIGHT, fill=Y)

        viewer.protocol("WM_DELETE_WINDOW",
                        lambda: common.close_window(type))
        viewer.mainloop()

    def update_count(self):
        self.author_label.config(text=f"Author ({len(self.author_sel)})")
        self.category_label.config(text=f"Category ({len(self.category_sel)})")
        self.publisher_label.config(
            text=f"Publisher ({len(self.publisher_sel)})")
        self.language_label.config(text=f"Language ({len(self.language_sel)})")

    def add_option(self, type):
        types = ["author", "category", "publisher", "language"]
        type = types[type]
        value = eval(f"self.{type}_entry.get()")
        value = value.strip().replace(';', '')
        if value not in eval(f"self.{type}_sel") and value:
            eval(f"self.{type}_sel.append(value)")
        eval(f"self.{type}.set('')")
        self.update_count()

    def delete_option(self, ev, type):
        item_id = ev.widget.focus()
        item = ev.widget.item(item_id)
        data = item['values'][0]
        self.tree.delete(item_id)
        eval(f"self.{type}_sel.remove('{data}')")
        self.update_count()

    def find_book(self, ev):
        isbn = self.isbn.get()
        if isbn != self.last_isbn and isbn.strip():
            cursor.execute("select isbn from resources_library")
            all_isbn = cursor.fetchall()
            isbns = []
            for x in all_isbn:
                isbns.append(''.join(re.findall(r"\d+", x[0])))
            if ''.join(re.findall(r"\d+", isbn)) in isbns:
                self.title.set("")
                self.title_entry.config(state="normal")
                msg.showwarning(
                    "Shelfmate", "This book is already in your resources!")
                self.isbn.set("")
            else:
                SERVICE = "openl"
                bibtex = bibformatters["bibtex"]
                self.last_isbn = isbn
                try:
                    urlopen('https://www.google.com')
                except Exception as e:
                    self.title.set("")
                    self.title_entry.config(state="normal")
                    print("[POOR CONNECTION]", e)
                else:
                    try:
                        if not any(char.isalpha() for char in isbn):
                            res = bibtex(meta(isbn, SERVICE))
                            title = re.findall(
                                "title = {(.*)}", res)[0].replace(' and ', ", ")
                            author = ', '.join(
                                set(re.findall("author = {(.*)}", res)[0].replace(' and ', ", ").split(', ')))
                            year = re.findall(
                                "year = {(.*)}", res)[0].replace(' and ', ", ")
                            publisher = re.findall(
                                "publisher = {(.*)}", res)[0].replace(' and ', ", ")
                            isbn = re.findall("isbn = {(.*)}", res)[0]

                            self.title.set(title)
                            self.title_entry.config(state="readonly")
                            self.author_sel.extend(author.split(", "))
                            self.publisher_sel.append(publisher)
                            self.update_count()
                            self.frame00.grid(row=0, column=1, sticky=N)

                            try:
                                u = requests.get(
                                    f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg")
                                self.url = u.url
                                _cover = Image.open(BytesIO(u.content))
                                if _cover.width < 10:
                                    raise ValueError
                            except:
                                self.url = f"{PATH}/../static/Personal/Images/display/book_cover.png"
                                _cover = Image.open(self.url)
                            _cover = _cover.resize((300, 400))
                            COVER = ImageTk.PhotoImage(_cover)
                            self.book.config(image=COVER)
                            self.book.image = COVER
                            if len(title) > 50:
                                title = title[:47]+'...'
                            if len(author) > 50:
                                author = author[:47]+'...'
                            if len(publisher) > 50:
                                publisher = publisher[:47]+'...'
                            self.book_title.config(text=title)
                            self.book_author.config(text=author)
                            self.book_year.config(text=year)
                            self.book_publisher.config(text=publisher)
                        else:
                            self.frame00.grid_forget()
                            self.title.set("")
                            self.title_entry.config(state="normal")
                            print("[BAD ISBN]")
                    except Exception as e:
                        self.frame00.grid_forget()
                        self.title.set("")
                        self.title_entry.config(state="normal")
                        print("[ISBN UNTRACKABLE]", e)

    def submit_form(form):
        isbn = form.isbn.get()
        title = form.title.get()
        edition = form.edition.get()
        author = form.author_sel
        category = form.category_sel
        publisher = form.publisher_sel
        language = form.language_sel
        try:
            quantity = int(form.quantity.get())
        except:
            quantity = 0
        book = form.url
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        all_author = cookies[1]['author'].split(';')[:-1]
        all_category = cookies[1]['category'].split(';')[:-1]
        all_publisher = cookies[1]['publisher'].split(';')[:-1]
        all_language = cookies[1]['language'].split(';')[:-1]
        all_author.extend(author)
        all_category.extend(category)
        all_publisher.extend(publisher)
        all_language.extend(language)
        all_author = ';'.join(list(set(all_author)))+';'
        all_category = ';'.join(list(set(all_category)))+';'
        all_publisher = ';'.join(list(set(all_publisher)))+';'
        all_language = ';'.join(list(set(all_language)))+';'

        if isbn and title and author and category and publisher and language and category and quantity:
            if msg.askyesno("Confirm", "Do you want to submit?"):
                cursor.execute(f'''insert into resources_library(isbn, title, edition, author, category, publisher, language, quantity, user_id, book_cover, borrowed, reading)
                            values ("{isbn}", "{title}", "{edition}", "{';'.join(author)};", "{';'.join(category)};", "{';'.join(publisher)};", "{';'.join(language)};", {quantity}, {cookies[0]['id']}, "{book}", 0, 0);''')
                connection.commit()
                cursor.execute(f'''update logged_users
                               set author="{all_author}", category="{all_category}", publisher="{all_publisher}", language="{all_language}"
                               where id={cookies[0]['id']}''')
                connection.commit()
                common = Common(form)
                common.refresh()
                msg.showinfo("Shelfmate", "Book added successfully!")
                common.close_all_windows()
                AddResources()
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")


class AllResources(Tk):
    def __init__(self):
        super().__init__()
        windows["all resources"] = self
        _cover = Image.open(
            f"{PATH}/../static/Personal/Images/display/book_cover.png")
        _cover = _cover.resize((150, 200))
        self.INIT_COVER = ImageTk.PhotoImage(_cover)
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common = Common(root)
        root.common.set_screen()
        root.title("All Resources")
        root.config(bg="gainsboro")
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(
            f"select * from resources_library where user_id={root.user_id}")
        root.books = cursor.fetchall()
        CARDBG = "#94ADD7"

        BIG_FRAME = Frame(root)
        root.canvas = Canvas(BIG_FRAME, bg="gainsboro")
        root.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        root.scrollbar = Scrollbar(
            BIG_FRAME, orient=VERTICAL, command=root.canvas.yview)
        root.scrollbar.pack(side=RIGHT, fill=Y)
        root.canvas.configure(yscrollcommand=root.scrollbar.set)
        root.canvas.bind("<Configure>", lambda e: root.canvas.config(
            scrollregion=root.canvas.bbox(ALL)))

        FRAME = Frame(root.canvas, bg="gainsboro")
        root.canvas.create_window((0, 0), window=FRAME, anchor="nw")
        root.canvas.bind_all("<MouseWheel>", root._on_mousewheel)

        root.bind("<Configure>", root._on_configure)

        title = Label(root, text="All Resources", font=(
            "Verdana", 25, "underline"), pady=20, bg="gainsboro")

        root.book_holders = []
        root.frame0_holders = []
        root.buttons = []
        root.book_cards = {}
        root.STATUS = []
        for i in range(len(root.books)):
            thebook = root.books[i]
            frame = Frame(FRAME, bg=CARDBG, padx=20, pady=10)
            root.book_cards[thebook[0]] = frame
            frame0 = Frame(frame, bg="white", padx=10, pady=5)
            frame1 = Frame(frame)
            frame2 = Frame(frame0)
            book = Label(frame1, image=root.INIT_COVER)
            book.image = root.INIT_COVER
            root.book_holders.append(book)
            name = Label(
                frame, text=thebook[2], font="comicsans 15", bg=CARDBG, wraplength=300)
            btn1 = Button(frame2, text="Edit", font="robota 12", bg="black", fg="white", activebackground="grey",
                          activeforeground="white", bd=0, cursor="hand2", command=lambda e=(thebook[0], i): root.edit_res(*e))
            btn2 = Button(frame2, text="Delete", font="robota 12", bg="#C51605", fg="white", activebackground="grey",
                          activeforeground="white", bd=0, cursor="hand2", command=lambda e=(thebook[0], i): root.delete_res(*e))

            root.frame0_holders.append(frame0)
            root.buttons.append((btn1, btn2))
            root.STATUS.append(1)

            frame2.grid(row=9, column=0, sticky=E)
            Label(frame, width=10, bg=CARDBG).grid(row=1, column=1)
            frame1.grid(row=2, column=2)
            name.grid(row=0, column=0)
            Label(frame, height=2, bg=CARDBG).grid(row=1, column=0)
            frame0.grid(row=2, column=0, sticky=W)
            book.grid(row=0, column=0)
            btn1.grid(row=0, column=0)
            btn2.grid(row=0, column=1)
            frame.grid(row=i//2, column=i % 2, padx=30, pady=20, sticky=W)

        root.show_card_set()
        title.pack()
        BIG_FRAME.pack(fill=BOTH, expand=1)

        image_loading_thread = threading.Thread(target=root.load_covers)
        image_loading_thread.start()

        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("all resources"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.pack_forget()
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def adjust_card(self, frame0, thebook):
        for content in frame0.winfo_children()[1:]:
            content.destroy()

        lbl0 = Label(
            frame0, text=f"ISBN - {thebook[1]}", bg="white", font="comicsans 13")
        lbl1 = Label(
            frame0, text=f"Authors - {thebook[4].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13")
        lbl2 = Label(
            frame0, text=f"Publisher - {thebook[6].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13")
        lbl3 = Label(
            frame0, text=f"Category - {thebook[5].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13")
        lbl4 = Label(
            frame0, text=f"Language - {thebook[7].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13")
        lbl5 = Label(
            frame0, text=f"Edition - {thebook[3]}", bg="white", font="comicsans 13")
        lbl6 = Label(
            frame0, text=f"Available - {thebook[8]-thebook[11]-thebook[12]}", bg="white", font="comicsans 13")
        lbl7 = Label(
            frame0, text=f"Borrowed - {thebook[11]}", bg="white", font="comicsans 13")
        lbl8 = Label(
            frame0, text=f"Reading - {thebook[12]}", bg="white", font="comicsans 13")

        for i in range(9):
            eval(f"lbl{i}.grid(row={i}, column=0, sticky=W)")

    def show_card_set(root, target=None, thebook=None):
        if target == None:
            for i in range(len(root.books)):
                frame0 = root.frame0_holders[i]
                thebook = root.books[i]
                root.adjust_card(frame0, thebook)
        else:
            frame0 = root.frame0_holders[target]
            if thebook == None:
                thebook = root.books[target]
            root.adjust_card(frame0, thebook)
            root.STATUS[target] = 1
            root.buttons[target][0].config(text="Edit")
            root.buttons[target][1].config(text="Delete")

    def edit_card_set(root, target, thebook=None):
        frame0 = root.frame0_holders[target]
        for content in frame0.winfo_children()[1:]:
            content.destroy()
        root.STATUS[target] = 0

        l0_frame = Frame(frame0)
        l0_lbl = Label(l0_frame, text="Authors - ",
                       bg="white", font="comicsans 13")
        root.aut_var = StringVar()
        root.aut_var.set(thebook[4].replace(';', ', ')[:-2])
        l0 = Entry(l0_frame, bg="white",
                   font="comicsans 13", textvariable=root.aut_var)
        l1_frame = Frame(frame0)
        l1_lbl = Label(l1_frame, text="Publisher - ",
                       bg="white", font="comicsans 13")
        root.pub_var = StringVar()
        root.pub_var.set(thebook[6].replace(';', ', ')[:-2])
        l1 = Entry(l1_frame, bg="white",
                   font="comicsans 13", textvariable=root.pub_var)
        l2_frame = Frame(frame0)
        l2_lbl = Label(l2_frame, text="Category - ",
                       bg="white", font="comicsans 13")
        root.cat_var = StringVar()
        root.cat_var.set(thebook[5].replace(';', ', ')[:-2])
        l2 = Entry(l2_frame, bg="white",
                   font="comicsans 13", textvariable=root.cat_var)

        l3_frame = Frame(frame0)
        l3_lbl = Label(l3_frame, text="Language - ",
                       bg="white", font="comicsans 13")
        root.lan_var = StringVar()
        root.lan_var.set(thebook[7].replace(';', ', ')[:-2])
        l3 = Entry(l3_frame, bg="white",
                   font="comicsans 13", textvariable=root.lan_var)
        l4_frame = Frame(frame0)
        l4_lbl = Label(l4_frame, text="Edition - ",
                       bg="white", font="comicsans 13")
        root.edi_var = StringVar()
        root.edi_var.set(thebook[3])
        l4 = Entry(l4_frame, bg="white",
                   font="comicsans 13", textvariable=root.edi_var)
        l5_frame = Frame(frame0)
        l5_lbl = Label(l5_frame, text="Available - ",
                       bg="white", font="comicsans 13")
        root.avail_var = StringVar()
        root.avail_var.set(thebook[8]-thebook[11]-thebook[12])
        l5 = Entry(l5_frame, bg="white",
                   font="comicsans 13", textvariable=root.avail_var)

        for i in range(6):
            eval(f"l{i}_frame.grid(row={i}, column=0, sticky=W)")
            eval(f"l{i}_lbl.grid(row={i}, column=0, sticky=W)")
            eval(f"l{i}.grid(row={i}, column=1, sticky=W)")

        root.buttons[target][0].config(text="Save")
        root.buttons[target][1].config(text="Cancel")

    def load_covers(self):
        try:
            self.cover_images = []
            for i in range(len(self.books)):
                book = self.books[i]
                _url = book[10]
                if _url.startswith('../static'):
                    self.cover_images.append(self.INIT_COVER)
                else:
                    self.cover_images.append(ImageTk.PhotoImage(Image.open(
                        BytesIO(requests.get(_url).content)).resize((150, 200))))
            self.after(0, self.present_covers)
        except Exception as e:
            print("[APP CLOSED]", e)

    def present_covers(self):
        try:
            for i, cover in enumerate(self.cover_images):
                self.book_holders[i].config(image=cover)
                self.book_holders[i].image = cover
        except Exception as e:
            print("[DELETED BEFORE BOOK LOAD]", e)

    def delete_res(self, book, target):
        if self.STATUS[target]:
            if msg.askyesno("Shelfmate", "Do you really want to delete this book?"):
                cursor.execute(
                    f"delete from resources_library where id={book}")
                connection.commit()
                for content in self.book_cards[book].winfo_children():
                    content.destroy()
                Label(self.book_cards[book], text="(Deleted)",
                      font="comicsans 30", bg="#94ADD7", fg="#C51605").pack()
        else:
            self.show_card_set(target)

    def edit_res(self, book, target):
        if self.STATUS[target]:
            cursor.execute(f'''select * from resources_library
                           where user_id={self.user_id} and id={book}''')
            thebook = cursor.fetchone()
            self.edit_card_set(target, thebook)
        else:
            aut = self.aut_var.get()
            pub = self.pub_var.get()
            cat = self.cat_var.get()
            lan = self.lan_var.get()
            edi = self.edi_var.get()

            cursor.execute(f'''select borrowed, reading, quantity
                           from resources_library where id={book}''')
            bor, read, prev = cursor.fetchone()
            try:
                avail = int(self.avail_var.get())
                1/(avail >= 0)
            except:
                avail = prev-bor-read

            cursor.execute(f'''update resources_library
                           set author="{aut.replace(', ', ';')};", publisher="{pub.replace(', ', ';')};",
                           category="{cat.replace(', ', ';')};", language="{lan.replace(', ', ';')};",
                           edition="{edi}", quantity={avail+bor+read}
                           where id={book}''')
            connection.commit()
            cursor.execute(f'''select * from resources_library
                           where user_id={self.user_id} and id={book}''')
            thebook = cursor.fetchone()
            self.show_card_set(target, thebook)


class LibraryDetails(Tk):
    def __init__(self):
        super().__init__()
        windows["library details"] = self
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common = Common(root)
        root.common.set_screen()
        root.title("Library Details")
        root.config(bg="gainsboro")
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.cookie = json.load(cookie)

        title = Label(root, text="Library Details", font=(
            "Verdana", 25, "underline"), pady=40, bg="gainsboro")
        root.FRAME = Frame(root)

        title.pack()
        root.FRAME.pack()

        if root.cookie[2]['library_name']:
            root.display_screen()
        else:
            root.edit_screen()

        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("library details"))

    def edit_screen(root, edit=False):
        frame0 = Frame(root.FRAME, padx=50, pady=20,
                       highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=20, bg="white")
        frame2 = Frame(frame0, bg="white")

        lbl0 = Label(frame1, text="Library Name *",
                     font=("Arial", 13), bg="white", padx=50)
        root.name = StringVar()
        ent0 = Entry(frame1, textvariable=root.name, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        ent0.focus()

        lbl1 = Label(frame1, text="Email *",
                     font=("Arial", 13), bg="white", padx=50)
        root.email = StringVar()
        ent1 = Entry(frame1, textvariable=root.email, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        lbl2 = Label(frame1, text="Phone number *",
                     font=("Arial", 13), bg="white", padx=50)
        root.phone = StringVar()
        ent2 = Entry(frame1, textvariable=root.phone, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        lbl3 = Label(frame1, text="Address *",
                     font=("Arial", 13), bg="white", padx=50)
        root.add1 = StringVar()
        root.add2 = StringVar()
        root.dist = StringVar()
        root.stt = StringVar()
        root.pin = StringVar()
        root.country = StringVar()
        ent3 = Frame(frame1, bg="white")
        add1_lbl = Label(ent3, text="Address Line 1", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.add1_ent = Entry(ent3, textvariable=root.add1, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        add2_lbl = Label(ent3, text="Address Line 2", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.add2_ent = Entry(ent3, textvariable=root.add2, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        ent3x = Frame(ent3, bg="white")
        dist_lbl = Label(ent3x, text="District", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.dist_ent = Entry(ent3x, textvariable=root.dist, font=(
            "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        stt_lbl = Label(ent3x, text="State", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.stt_ent = Entry(ent3x, textvariable=root.stt, font=(
            "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        ent3y = Frame(ent3, bg="white")
        pin_lbl = Label(ent3y, text="Postal Code", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.pin_ent = Entry(ent3y, textvariable=root.pin, font=(
            "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        country_lbl = Label(ent3y, text="Country", font=(
            "Arial", 10), fg=LABEL, bg="white")
        countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'Colombia', 'Comoros', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', "CÃ´te d'Ivoire", 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kingdom of the Netherlands', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                     'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', "People's Republic of China", 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Republic of Ireland', 'Republic of the Congo', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'SÃ£o TomÃ© and PrÃ\xadncipe', 'Tajikistan', 'Tanzania', 'Thailand', 'The Gambia', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
        root.country_ent = ttk.Combobox(ent3y, textvariable=root.country, width=20,
                                        values=countries, state="readonly")
        root.country.set(countries[0])

        lbl4 = Label(frame1, text="Library Website",
                     font=("Arial", 13), bg="white", padx=50)
        root.web = StringVar()
        ent4 = Entry(frame1, textvariable=root.web, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        save_btn = Button(frame2, text="Save", bg="#0D6EFD", fg="white", activebackground=BGCOLOR, padx=5,
                          activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=root.save)
        cancel_btn = Button(frame2, text="Cancel", bg="black", fg="white", activebackground="#6C757D", padx=5,
                            activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=lambda: root.cancel(edit))

        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        save_btn.grid(row=0, column=0, padx=10)
        cancel_btn.grid(row=0, column=1, padx=10)
        root.common.address_packer(add1_lbl, add2_lbl, ent3x, ent3y,
                                   dist_lbl, stt_lbl, pin_lbl, country_lbl)
        for i in range(5):
            eval(f"lbl{i}.grid(row={i}, column=0, sticky=W, pady=10)")
            eval(f"ent{i}.grid(row={i}, column=1, padx=50, pady=10)")
        for i in range(5):
            if i == 3:
                continue
            eval(f"ent{i}.bind('<Return>', root.save)")
        for x in ["add1", "add2", "dist", "stt", "pin", "country"]:
            eval(f"root.{x}_ent.bind('<Return>', root.save)")

        if edit:
            lib = root.cookie[2]
            add = lib['library_address'].split(';')
            root.name.set(lib['library_name'])
            root.email.set(lib['library_email'])
            root.phone.set(lib['library_phone'])
            root.add1.set(add[0])
            root.add2.set(add[1])
            root.dist.set(add[2])
            root.stt.set(add[3])
            root.pin.set(add[4])
            root.country.set(add[5])
            root.web.set(lib['library_url'])

    def display_screen(root):
        LINK = "#0A6EBD"
        frame0 = Frame(root.FRAME, padx=50, pady=30,
                       highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=30, bg="white")
        frame2 = Frame(frame0, bg="white")

        q0 = Label(frame1, text="Library Name",
                   font=("Arial", 13), bg="white", padx=50)
        a0 = Label(frame1, text=root.cookie[2]["library_name"],
                   font=("Arial", 13), bg="white", padx=50)
        q1 = Label(frame1, text="Phone number",
                   font=("Arial", 13), bg="white", padx=50)
        a1 = Label(frame1, text=root.cookie[2]["library_phone"],
                   font=("Arial", 13), bg="white", padx=50)
        q2 = Label(frame1, text="Email",
                   font=("Arial", 13), bg="white", padx=50)
        a2 = Label(frame1, text=root.cookie[2]["library_email"], font=(
            "Arial", 13, 'underline'), bg="white", padx=50, fg=LINK, cursor="hand2")
        q3 = Label(frame1, text="Address",
                   font=("Arial", 13), bg="white", padx=50)
        a3 = Label(frame1, text=root.cookie[2]["library_address"].replace(
            ';;', ';').replace(';', ', '), font=("Arial", 13), bg="white", padx=50)
        q4 = Label(frame1, text="Library Website",
                   font=("Arial", 13), bg="white", padx=50)
        a4 = Label(frame1, text=root.cookie[2]["library_url"],
                   font=("Arial", 13, 'underline'), bg="white", padx=50, fg=LINK, cursor="hand2")
        btn1 = Button(frame2, text="Edit", font="robota 12", bg="black", fg="white", activebackground="grey",
                      activeforeground="white", bd=0, cursor="hand2", padx=5, command=root.edit)
        btn2 = Button(frame2, text="Delete", font="robota 12", bg="#C51605", fg="white", activebackground="grey",
                      activeforeground="white", bd=0, cursor="hand2", padx=5, command=root.delete)

        a2.bind(
            "<Button-1>", lambda e: web.open(f"mailto:{root.cookie[2]['library_email']}"))
        a4.bind("<Button-1>",
                lambda e: web.open(root.cookie[2]['library_url']))

        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        btn1.grid(row=0, column=0, padx=20, pady=10)
        btn2.grid(row=0, column=1, padx=20, pady=10)
        for i in range(5):
            eval(f"q{i}.grid(row={i}, column=0, sticky=W, pady=2)")
            eval(f"a{i}.grid(row={i}, column=1, sticky=W, pady=2)")

    def save(self, ev=0):
        name = self.name.get()
        email = self.email.get()
        phone = self.phone.get()
        add1 = self.add1.get().strip().replace(';', '')
        add2 = self.add2.get().strip().replace(';', '')
        dist = self.dist.get().strip().replace(';', '')
        stt = self.stt.get().strip().replace(';', '')
        pin = self.pin.get().strip().replace(';', '')
        country = self.country.get()
        website = self.web.get()
        address = ';'.join([add1, add2, dist, stt, pin, country])

        if name and email and phone and add1 and dist and stt and pin:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                if validators.url(website):
                    cursor.execute(f'''update logged_users set library_name="{name}",
                                library_email="{email}", library_phone="{phone}",
                                library_address="{address}", library_url="{website}"
                                where id={self.cookie[0]['id']}''')
                    self.common.refresh()
                    self.common.close_all_windows()
                    LibraryDetails()
                else:
                    msg.showwarning("Shelfmate", "Invalid URL!")
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")

    def delete(self):
        if msg.askyesno("Shelfmate", "Are you sure you want to delete your Library Details?"):
            cursor.execute(f'''update logged_users set library_name="",
                           library_email="", library_phone="",
                           library_address="", library_url=""
                           where id={self.cookie[0]['id']}''')
            self.common.refresh()
            self.common.close_all_windows()
            LibraryDetails()

    def edit(self):
        for x in self.FRAME.winfo_children():
            x.destroy()
        self.edit_screen(True)

    def cancel(self, edit):
        if edit:
            for x in self.FRAME.winfo_children():
                x.destroy()
            self.display_screen()
        else:
            self.common.back()


class AddMembers(Tk):
    def __init__(self):
        super().__init__()
        windows["add members"] = self
        self.pic = 0
        self.suggest_clicks = 0
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common = Common(root)
        root.common.set_screen()
        root.title("Add Members")
        root.config(bg="gainsboro")
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']

        title = Label(root, text="Add Members", font=(
            "Verdana", 25, "underline"), pady=40, bg="gainsboro")
        FRAME = Frame(root)
        frame0 = Frame(FRAME, padx=50, pady=20,
                       highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=20, bg="white")
        frame2 = Frame(frame0, bg="white")

        q0 = Label(frame1, text="Name *",
                   font=("Arial", 13), bg="white", padx=50)
        root.name = StringVar()
        a0 = Entry(frame1, textvariable=root.name, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        q1 = Label(frame1, text="Username *",
                   font=("Arial", 13), bg="white", padx=50)
        root.username = StringVar()
        a1 = Entry(frame1, textvariable=root.username, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        suggest = Button(frame1, text="Suggest", cursor="hand2",
                         font=("Arial", 10), padx=10, pady=5, command=root.suggest)

        q2 = Label(frame1, text="Email *",
                   font=("Arial", 13), bg="white", padx=50)
        root.email = StringVar()
        a2 = Entry(frame1, textvariable=root.email, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        q3 = Label(frame1, text="Phone Number",
                   font=("Arial", 13), bg="white", padx=50)
        root.phone = StringVar()
        a3 = Entry(frame1, textvariable=root.phone, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        q3 = Label(frame1, text="Phone Number",
                   font=("Arial", 13), bg="white", padx=50)
        root.phone = StringVar()
        a3 = Entry(frame1, textvariable=root.phone, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        q4 = Label(frame1, text="Address",
                   font=("Arial", 13), bg="white", padx=50)
        root.add1 = StringVar()
        root.add2 = StringVar()
        root.dist = StringVar()
        root.stt = StringVar()
        root.pin = StringVar()
        root.country = StringVar()
        a4 = Frame(frame1, bg="white")
        add1_lbl = Label(a4, text="Address Line 1", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.add1_ent = Entry(a4, textvariable=root.add1, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        add2_lbl = Label(a4, text="Address Line 2", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.add2_ent = Entry(a4, textvariable=root.add2, font=(
            "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        ent3x = Frame(a4, bg="white")
        dist_lbl = Label(ent3x, text="District", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.dist_ent = Entry(ent3x, textvariable=root.dist, font=(
            "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        stt_lbl = Label(ent3x, text="State", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.stt_ent = Entry(ent3x, textvariable=root.stt, font=(
            "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        ent3y = Frame(a4, bg="white")
        pin_lbl = Label(ent3y, text="Postal Code", font=(
            "Arial", 10), fg=LABEL, bg="white")
        root.pin_ent = Entry(ent3y, textvariable=root.pin, font=(
            "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        country_lbl = Label(ent3y, text="Country", font=(
            "Arial", 10), fg=LABEL, bg="white")
        countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'Colombia', 'Comoros', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', "CÃ´te d'Ivoire", 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kingdom of the Netherlands', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                     'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', "People's Republic of China", 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Republic of Ireland', 'Republic of the Congo', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'SÃ£o TomÃ© and PrÃ\xadncipe', 'Tajikistan', 'Tanzania', 'Thailand', 'The Gambia', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
        root.country_ent = ttk.Combobox(ent3y, textvariable=root.country, width=20,
                                        values=countries, state="readonly")
        root.country.set(countries[0])

        q5 = Label(frame1, text="Avatar *",
                   font=("Arial", 13), bg="white", padx=50)
        a5 = Frame(frame1, bg=ENTRY, pady=10, padx=20)
        root.common.load_toggle()
        _avatar = Image.open(
            f"{PATH}/../static/Personal/Images/members/member_0.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)
        left_btn = Button(a5, image=root.common.BEFORE, bd=0, width=100,
                          cursor="hand2", command=lambda: root.common.avatar_toggle(-1, "member"))
        root.avatar = Label(a5, image=AVATAR, width=100)
        right_btn = Button(a5, image=root.common.AFTER, bd=0, width=100,
                           cursor="hand2", command=lambda: root.common.avatar_toggle(1, "member"))
        left_btn.image = root.common.BEFORE
        root.avatar.image = AVATAR
        right_btn.image = root.common.AFTER

        submit_btn = Button(frame2, text="Submit", fg="white", bg="black", activebackground="#111111",
                            activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=root.submit_form)

        title.pack()
        FRAME.pack()
        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        left_btn.grid(row=0, column=0)
        root.avatar.grid(row=0, column=1)
        right_btn.grid(row=0, column=2)
        root.common.address_packer(add1_lbl, add2_lbl, ent3x, ent3y,
                                   dist_lbl, stt_lbl, pin_lbl, country_lbl)
        for i in range(6):
            eval(f"q{i}.grid(row={i//2}, column={2*(i%2)}, sticky=W, pady=10)")
            eval(f"a{i}.grid(row={i//2}, column={2*(i%2)+1}, padx=40, pady=10)")
        suggest.grid(row=0, column=4, sticky=W, pady=10)
        submit_btn.pack(pady=30)

        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("add members"))

    def suggest(self, fetch=True, usernames=None):
        if fetch and not self.suggest_clicks:
            cursor.execute(f'''select username from members_library
                           where user_id={self.user_id}''')
        usernames = [x[0] for x in cursor.fetchall()]
        suggestion = ''.join(random.choices(
            string.ascii_letters+string.digits+'_', k=10))
        if suggestion in usernames:
            self.suggest(False, usernames)
        else:
            self.username.set(suggestion)
            self.suggest_clicks += 1

    def submit_form(form):
        name = form.name.get()
        username = form.username.get().strip()
        email = form.email.get()
        phone = form.phone.get()
        address = ';'.join([form.add1.get().strip().replace(';', ''), form.add2.get().strip().replace(';', ''),
                            form.dist.get().strip().replace(';', ''), form.stt.get().strip().replace(';', ''),
                            form.pin.get().strip().replace(';', ''), form.country.get()])
        avatar = form.pic

        if name and username and email:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                cursor.execute(f'''insert into members_library(name, username, email,
                            phone, address, avatar, user_id, visits)
                            values("{name}", "{username}", "{email}", "{phone}",
                            "{address}", {avatar}, {form.user_id}, 0);''')
                connection.commit()
                msg.showinfo("Shelfmate", "Member added successfully!")
                form.common.close_all_windows()
                AddMembers()
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")


class AllMembers(Tk):
    def __init__(self):
        super().__init__()
        windows["all members"] = self
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        root.common = Common(root)
        root.common.set_screen()
        root.title("All Members")
        root.config(bg="gainsboro")
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(
            f"select * from members_library where user_id={root.user_id}")
        root.members = cursor.fetchall()
        CARDBG = "#94ADD7"

        title = Label(root, text="All Members", font=(
            "Verdana", 25, "underline"), pady=40, bg="gainsboro")

        BIG_FRAME = Frame(root)
        root.canvas = Canvas(BIG_FRAME, bg="gainsboro")
        root.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        root.scrollbar = Scrollbar(
            BIG_FRAME, orient=VERTICAL, command=root.canvas.yview)
        root.scrollbar.pack(side=RIGHT, fill=Y)
        root.canvas.configure(yscrollcommand=root.scrollbar.set)
        root.canvas.bind("<Configure>", lambda e: root.canvas.config(
            scrollregion=root.canvas.bbox(ALL)))
        FRAME = Frame(root.canvas, bg="gainsboro")
        root.canvas.create_window((0, 0), window=FRAME, anchor="nw")
        root.canvas.bind_all("<MouseWheel>", root._on_mousewheel)
        root.bind("<Configure>", root._on_configure)

        for i in range(len(root.members)):
            themember = root.members[i]
            frame = Frame(FRAME, bg=CARDBG, padx=20, pady=10)
            frameX = Frame(frame, bg="white")
            frame0 = Frame(frameX, bg="white", padx=10, pady=5)
            frame1 = Frame(frameX, bg="white", padx=10, pady=5)
            _avatar = Image.open(
                f"{PATH}/../static/Personal/Images/members/member_{themember[6]}.png")
            _avatar = _avatar.resize((100, 100))
            AVATAR = ImageTk.PhotoImage(_avatar)
            avatar = Label(frame0, image=AVATAR, bg="white")
            avatar.image = AVATAR
            username = Label(frame0, text=f"({themember[5]})",
                             font="arial 12", fg="grey", bg="white")
            address = ', '.join([x for x in themember[4].split(';') if x])
            name = themember[1]
            email = themember[3]
            if len(address) > 30:
                address = address[:29]+'...'
            if len(name) > 30:
                name = name[:29]+'...'
            if len(email) > 30:
                email = email[:29]+'...'
            info0 = Label(frame1, text=name,
                          font="comicsans 15 bold", bg="white")
            info1 = Label(frame1, text=address, bg="white", fg="grey")
            info2 = Label(frame1, text=themember[2], bg="white")
            info3 = Label(frame1, text=email, fg="#0A6EBD",
                          font="comicsans 10 underline", bg="white", cursor="hand2")
            info3.bind("<Button-1>",
                       lambda e: web.open(f"mailto:{themember[3]}"))

            frame.grid(row=i//3, column=i % 3, padx=30, pady=20, sticky=W)
            frameX.pack()
            frame0.grid(row=0, column=0)
            frame1.grid(row=0, column=1)
            avatar.grid(row=0, column=0, pady=10)
            username.grid(row=1, column=0)
            for i in range(4):
                if i==2 and not themember[2]:
                    continue
                eval(f"info{i}.grid(row={i}, column=0, sticky=E, pady=5)")

        title.pack()
        BIG_FRAME.pack(fill=BOTH, expand=1)

        root.protocol("WM_DELETE_WINDOW",
                      lambda: root.common.close_window("all members"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.pack_forget()
        self.scrollbar.pack(side=RIGHT, fill=Y)


if __name__ == "__main__":
    try:
        open = Opener()
        cursor.close()
        connection.close()
    except Exception as e:
        print("[APP CLOSED]", e)
