#the tkinter module as backbone and PIL for image handling
from tkinter import *
from tkinter import messagebox as msg, ttk
from PIL import Image, ImageTk

#python-sql connection maker
import mysql.connector as conn

#for getting book info from ISBN
from isbnlib import meta
from isbnlib.registry import bibformatters

#supporting modules
import webbrowser as web #for opening external websites
import password_hasher as ph #for hashing the login password of user
from urllib.request import urlopen #for checking internet connection
from datetime import datetime #for time and date related purpose
import re, os, json #re for searches, os for folder path, json for handling .json file
import random, string #for getting random generated strings
from io import BytesIO #for decoding image from websites
import threading #to load images outside the main window
import validators, requests #validators to check URL, requests to get redirected URLs
import time #to delay background functions
from tkcalendar import Calendar #to create date picker

#connecting the database to python
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
    #exiting application in case of connection issue
    print("[CONNECTION ERROR]")
    exit()

#setting some global constants and variables
PATH = os.path.dirname(__file__) #the path to this file
hasher = ph.PasswordHasher() #object to let hash passwords
windows = {} #dictionary to store the currently active tkinter windows
#some constant colours
BGCOLOR = "#7895CB"
ENTRY = "#EEEEEE"
LABEL = "#777777"
CARDBG = "#94ADD7"
#list of all countries (for address fields)
COUNTRIES = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'Colombia', 'Comoros', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', "CÃ´te d'Ivoire", 'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 'Gabon', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kingdom of the Netherlands', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
            'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', "People's Republic of China", 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Republic of Ireland', 'Republic of the Congo', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'SÃ£o TomÃ© and PrÃ\xadncipe', 'Tajikistan', 'Tanzania', 'Thailand', 'The Gambia', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']
#list of all abbreviated months (for date fields)
MONTHS = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#class with functions that are required in various windows
class Common():
    def __init__(self, root=None):
        if root:
            self.root = root #to recognize the active window
            self.SCREEN = (root.winfo_screenwidth(), root.winfo_screenheight())

    #sets a common screen
    def set_screen(self, wl=60, back=True):
        #loading the Shelfmate logo
        _logo = Image.open(f"{PATH}/../static/Personal/Images/display/logo.png")
        _logo = _logo.resize((wl, wl))
        self.LOGO = ImageTk.PhotoImage(_logo)
        #loading the back button image
        _back = Image.open(f"{PATH}/../static/Personal/Images/display/back.png")
        _back = _back.resize((50, 50))
        self.BACK = ImageTk.PhotoImage(_back)
        #setting the screen
        self.root.iconphoto(0, self.LOGO)
        self.root.minsize(self.SCREEN[0], self.SCREEN[1])
        self.root.after(0, lambda: self.root.state("zoomed"))
        #places the back button on demand
        back_btn = Button(self.root, image=self.BACK, command=self.back, cursor="hand2")
        if back:
            back_btn.place(x=0, y=0)

    #checks internet connection in background
    def check_conn(self):
        printer = 0
        while True:
            try:
                urlopen("https://www.google.com")
            except Exception as e:
                #kills the program, if offline
                print("[OFFLINE]", e)
                msg.showerror("Connection", "No internet access, restart after connecting to internet!")
                Common().close_all_windows()
            else:
                #shows running status
                if not printer:
                    print("[ONLINE] running...")
            time.sleep(1)
            #ensures that ONLINE message is printed after every 10 seconds
            printer = (printer+1)%10

    #closes a particular window (x) and removes it from the 'windows' dictionary
    def close_window(self, x):
        windows[x].destroy()
        del windows[x]
        for mini in ["picker", "login", "signup", "author", "category", "publisher", "resources", "language"]:
            if mini in windows:
                self.close_window(mini)

    #closes all active windows the same way to make way for a new one
    def close_all_windows(self):
        while len(windows):
            self.close_window(list(windows.keys())[0])

    #the back button takes the user to the main page
    def back(self):
        self.close_all_windows()
        Dashboard()

    #updates the cookie.json and logged.txt files
    def refresh(self):
        #fetches the user id
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            user_id = json.load(cookie)[0]['id']
        #gets the updated data
        cursor.execute(f"select * from logged_users where id={user_id}")
        arr = cursor.fetchall()[0]
        #decorates the data accordingly
        user = {'id': arr[0], 'name': arr[1], 'email': arr[2], 'username': arr[6], 'avatar': arr[7], 'phone': arr[8]}
        library = {'author': arr[9], 'category': arr[10], 'language': arr[11], 'publisher': arr[12]}
        library_offline = {'library_name': arr[13], 'library_email': arr[14], 'library_phone': arr[15], 'library_address': arr[16], 'library_url': arr[17]}
        #overwrites the updated data in both files
        with open(f'{PATH}/../static/Personal/Data/cookie.json', 'w') as cookie:
            cookie.write(json.dumps([user, library, library_offline], indent=4))
        with open(f'{PATH}/../static/Personal/Data/logged.txt', 'w') as f:
            f.write(arr[5])

    #packs all the address fields whenever required
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

    #loading the 'image toggle button' images
    def load_toggle(self, size=70):
        _right = Image.open(f"{PATH}/../static/Personal/Images/display/right.png")
        _right = _right.resize((size, size))
        _left = _right.rotate(180)
        self.AFTER = ImageTk.PhotoImage(_right)
        self.BEFORE = ImageTk.PhotoImage(_left)

    #common function to toggle the avatars for both 'members' and 'users'
    def avatar_toggle(self, dir, task):
        size = len(os.listdir(f"{PATH}/../static/Personal/Images/{task}s"))-1
        self.root.pic = self.root.pic+dir
        if self.root.pic < 0:
            self.root.pic = size
        elif self.root.pic > size:
            self.root.pic = 0
        _avatar = Image.open(f"{PATH}/../static/Personal/Images/{task}s/{task}_{self.root.pic}.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)
        self.root.avatar.config(image=AVATAR)
        self.root.avatar.image = AVATAR
    
    #returns a formatted current time
    def get_time(self):
        now = datetime.now()
        return f"{[f'0{now.day}' if int(now.day)<10 else now.day][0]} {MONTHS[now.month]}, {now.year}  {[f'0{now.hour}' if int(now.hour)<10 else now.hour][0]}:{[f'0{now.minute}' if int(now.minute)<10 else now.minute][0]}"

#the opening window (without login)
class Opener(Tk):
    def __init__(self):
        network_thread = threading.Thread(target=Common().check_conn)
        network_thread.daemon = True
        network_thread.start()
        super().__init__()
        windows["opener"] = self
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            try:
                #checks if data is present in cookie.json
                cookies = json.load(cookie)
            except:
                #if not, continues to normal screen
                pass
            else:
                #if yes, switches to Dashboard
                cursor.execute(f"select user_hash from logged_users where username = '{cookies[0]['username']}'")
                user_hash = cursor.fetchone()[0]
                with open(f'{PATH}/../static/Personal/Data/logged.txt') as log:
                    #final authentication by matching cookie.json and logged.txt data
                    if log.read() == user_hash:
                        Common(self).close_all_windows()
                        Dashboard()
        self.create_screen()
        self.mainloop()

    #creates the tkinter screen
    def create_screen(root):
        #general configurations
        root.config(bg=BGCOLOR)
        root.title("Shelfmate")
        common = Common(root)
        common.set_screen(back=False)

        #packing frames
        frame1 = Frame(root, bg=BGCOLOR)
        frame1.pack(ipady=100)
        frame2 = Frame(root, bg=BGCOLOR)
        frame2.pack()

        #creating and placing the header
        img = Label(frame1, image=common.LOGO, bg=BGCOLOR)
        img.image = common.LOGO
        name = Label(frame1, text="Shelfmate", font="Arial 30", bg=BGCOLOR, fg="white")
        img.grid(row=0, column=0)
        name.grid(row=0, column=1)

        #creating and placing the button frame elements
        log_btn = Button(frame2, text="Log In", font=("Arial", 15), bg="#AAC8A7", cursor="hand2", activebackground="#C3EDC0", bd=0, padx=10, pady=5, command=lambda: Login())
        sign_btn = Button(frame2, text="Sign Up", font=("Arial", 15), bg="#AAC8A7", cursor="hand2", activebackground="#C3EDC0", bd=0, padx=10, pady=5, command=lambda: Signup())
        log_btn.grid(row=1, column=0, padx=50, pady=50)
        sign_btn.grid(row=1, column=2, padx=50, pady=50)

        #creating link to Shelfmate website
        link = Button(root, text="Try our website for a better interface..", command=lambda: web.open_new_tab("https://shelfmate.onrender.com"), bg=BGCOLOR, bd=0, activebackground=BGCOLOR, activeforeground="red", font=("Arial", 15, "underline"), cursor="hand2")
        link.pack(side=BOTTOM, ipady=30)

        #terminating window calls this function
        root.protocol("WM_DELETE_WINDOW", lambda: common.close_window("opener"))

#the login window (floating)
class Login(Tk):
    def __init__(self):
        #window appears only if it is not opened
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
            self.protocol("WM_DELETE_WINDOW", lambda: common.close_window("login"))
            self.mainloop()

    #making the screen
    def create_screen(root):
        #creating all elements
        frame = Frame(root, bg=root.BGCOLOR)
        login_label = Label(root, text="Login", bg=root.BGCOLOR, fg="#FF3399", font=("Arial", 30))
        username_label = Label(frame, text="Username/\nEmail", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.username = Entry(frame, font=("Arial", 16))
        root.username.focus()
        root.password = Entry(frame, show="*", font=("Arial", 16))
        password_label = Label(frame, text="Password", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        login_button = Button(root, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=root.login)

        #placing all elements
        login_label.pack(ipady=30)
        frame.pack()
        username_label.grid(row=0, column=0, padx=50)
        root.username.grid(row=0, column=1, pady=20)
        password_label.grid(row=1, column=0, padx=50)
        root.password.grid(row=1, column=1, pady=20)
        login_button.pack(pady=30)

        #binding the entries to the login button
        root.username.bind("<Return>", root.login)
        root.password.bind("<Return>", root.login)

    #after pressing the login button
    def login(root, ev=0):
        username = root.username.get()
        password = root.password.get()
        if username and password:
            cursor.execute("select username, email, pswd_hash from logged_users")
            all_users = cursor.fetchall()
            #checks if user gives email or username
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
                        #gets all data
                        cursor.execute(f"select * from logged_users where {typeof}='{username}'")
                        arr = cursor.fetchall()[0]
                        user = {'id': arr[0], 'name': arr[1], 'email': arr[2], 'username': arr[6], 'avatar': arr[7], 'phone': arr[8]}
                        library = {'author': arr[9], 'category': arr[10], 'language': arr[11], 'publisher': arr[12]}
                        library_offline = {'library_name': arr[13], 'library_email': arr[14], 'library_phone': arr[15], 'library_address': arr[16], 'library_url': arr[17]}
                        #saves the data in file
                        Common(root).close_all_windows()
                        with open(f'{PATH}/../static/Personal/Data/cookie.json', 'w') as cookie:
                            cookie.write(json.dumps([user, library, library_offline], indent=4))
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

#the signup window (floating)
class Signup(Tk):
    def __init__(self):
        #window appears only if it is not opened
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
            self.protocol("WM_DELETE_WINDOW", lambda: common.close_window("signup"))
            self.mainloop()

    #making the screen
    def create_screen(root):
        #creating all elements
        frame = Frame(root, bg=root.BGCOLOR)
        signup_label = Label(root, text="Signup", bg=root.BGCOLOR, fg="#FF3399", font=("Arial", 30))
        email_label = Label(frame, text="Email", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.email = Entry(frame, font=("Arial", 16))
        root.email.focus()
        name_label = Label(frame, text="Full Name", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.name = Entry(frame, font=("Arial", 16))
        username_label = Label(frame, text="Username", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.username = Entry(frame, font=("Arial", 16))
        password_label = Label(frame, text="Password", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.password = Entry(frame, show="*", font=("Arial", 16))
        confirm_label = Label(frame, text="Confirm Password", bg=root.BGCOLOR, fg="#FFFFFF", font=("Arial", 16))
        root.confirm = Entry(frame, show="*", font=("Arial", 16))
        signup_btn = Button(root, text="Signup", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=root.signup)

        #placing all elements
        signup_label.pack(ipady=30)
        frame.pack()
        email_label.grid(row=0, column=0, padx=50)
        root.email.grid(row=0, column=1, pady=20)
        name_label.grid(row=1, column=0, padx=50)
        root.name.grid(row=1, column=1, pady=20)
        username_label.grid(row=2, column=0, padx=50)
        root.username.grid(row=2, column=1, pady=20)
        password_label.grid(row=3, column=0, padx=50)
        root.password.grid(row=3, column=1, pady=20)
        confirm_label.grid(row=5, column=0, padx=50)
        root.confirm.grid(row=5, column=1, pady=20)
        signup_btn.pack(pady=30)

        #binding entries to signup button
        root.email.bind("<Return>", root.signup)
        root.name.bind("<Return>", root.signup)
        root.username.bind("<Return>", root.signup)
        root.password.bind("<Return>", root.signup)
        root.confirm.bind("<Return>", root.signup)

    #after pressing the Signup button
    def signup(root, ev=0):
        email = root.email.get()
        name = root.name.get()
        username = root.username.get()
        password = root.password.get()
        confirm = root.confirm.get()
        #checks all the inputs' validity
        if email and name and username and password and confirm:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): #email validity using "re"
                if re.search(r"[^a-zA-Z0-9_\s]", username) == None: #username validity using "re"
                    if len(username) >= 5: #username should be greater than 5
                        if len(password) >= 8: #password should be greater than 8
                            if password == confirm:
                                #inserts new user data to Database
                                cursor.execute(f'''insert into logged_users (name, email, pswd_hash, date_created, user_hash, username, avatar, phone, author, category, language, publisher, library_name, library_email, library_phone, library_address, library_url)
                                    values ("{name}", "{email}", "{hasher.get_hash(password)}", "{datetime.now()}", "{hasher.get_hash(username)}", "{username}", 0, "", "", "", "", "", "", "", "", "", "");''')
                                connection.commit()
                                #redirects you to Login window
                                Common(root).close_all_windows()
                                msg.showinfo("Success", "You have signed up successfully. Now log in to your account.")
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

#dashboard of user (after login)
class Dashboard(Tk):
    def __init__(self):
        super().__init__()
        self.common = Common(self)
        windows["dashboard"] = self
        #gets all user data from cookie.json
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        cursor.execute(f"select user_hash from logged_users where username = '{cookies[0]['username']}'")
        user_hash = cursor.fetchone()[0]
        with open(f'{PATH}/../static/Personal/Data/logged.txt') as log:
            if log.read() != user_hash:
                #if logged.txt doesn't match cookie.json redirects to Opener
                self.common.close_all_windows()
                Opener()
        #globalises all required user data inside the class
        self.user = cookies[0]
        self.library = cookies[1]
        self.library_offline = cookies[2]
        #sets the screen
        self.title(f"Dashboard @{self.user['username']}")
        self.create_screen()
        self.mainloop()

    #makes the screen
    def create_screen(root):
        #general configuration
        root.common.set_screen(30, False)
        root.config(bg=BGCOLOR)
        #loads the user avatar
        _avatar = Image.open(f"{PATH}/../static/Personal/Images/avatars/avatar_{root.user['avatar']}.png")
        _avatar = _avatar.resize((60, 60))
        AVATAR = ImageTk.PhotoImage(_avatar)
        #creating the header
        frame1 = Frame(root, pady=20, bg=BGCOLOR, cursor="hand2")
        avatar = Label(frame1, image=AVATAR)
        avatar.image = AVATAR
        user_head = Label(frame1, text=root.user["name"], font=("Verdana", 20), padx=20, bg=BGCOLOR, fg="white")
        log_out_btn = Button(root, text="Log Out", font="Comicsans 14", fg="red", cursor="hand2", padx=10, pady=5, command=root.log_out)
        #creating the navigation buttons
        frame2 = Frame(root, bg=BGCOLOR, pady=100)
        btn1 = Button(frame2, text="Add Resources", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(AddResources))
        btn2 = Button(frame2, text="All Resources", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(AllResources))
        btn3 = Button(frame2, text="Borrow Request", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(BorrowRequest))
        btn4 = Button(frame2, text="Check-In User", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(CheckInUser))
        btn5 = Button(frame2, text="Checked-In Readers", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(CheckedInReaders))
        btn6 = Button(frame2, text="Readers History", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn7 = Button(frame2, text="Add Member", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(AddMembers))
        btn8 = Button(frame2, text="All Members", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(AllMembers))
        btn9 = Button(frame2, text="Requests To Borrow", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn10 = Button(frame2, text="Borrowed Requests", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        btn11 = Button(frame2, text="Library Details", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2", command=lambda: root.navigate(LibraryDetails))
        btn12 = Button(frame2, text="Minor Settings", font=("Comicsans", 15), padx=10, pady=10, width=20, activebackground="#A0BFE0", bg="#C5DFF8", bd=1, cursor="hand2")
        #creating the link to Shelfmate website
        frame3 = Frame(root, bg=BGCOLOR, pady=20)
        logo = Label(frame3, image=root.common.LOGO, bg=BGCOLOR)
        logo.image = root.common.LOGO
        shelf = Label(frame3, text="Shelfmate", font=("Comicsans", 15), bg=BGCOLOR, fg="#2D4356", cursor="hand2")

        #placing all elements
        log_out_btn.place(x=0, y=0)
        frame1.pack()
        frame2.pack()
        frame3.pack(side=BOTTOM)
        avatar.grid(row=0, column=0)
        user_head.grid(row=0, column=1)
        logo.grid(row=0, column=0)
        shelf.grid(row=0, column=1)
        #special way to place the navigators
        for i in range(12):
            eval(f"btn{i+1}.grid(row=i//4, column=i%4)")

        #binding the required labels
        avatar.bind("<Button-1>", lambda e: root.navigate(AccountSettings))
        user_head.bind("<Button-1>", lambda e: root.navigate(AccountSettings))
        shelf.bind("<Button-1>", lambda e: web.open_new_tab("https://shelfmate.onrender.com"))
        root.protocol("WM_DELETE_WINDOW", lambda: root.common.close_window("dashboard"))

    #clears all saved data from device
    def log_out(self):
        if msg.askyesno("Shelfmate", "Do you really want to log out?"):
            with open(f'{PATH}/../static/Personal/Data/logged.txt', 'w') as log:
                log.write("")
            with open(f'{PATH}/../static/Personal/Data/cookie.json', 'w') as cookie:
                cookie.write("")
            self.common.close_all_windows()
            Opener()

    #functioning all the navigators
    def navigate(self, navigator, ev=0):
        self.common.close_all_windows()
        navigator()

#settings window for user
class AccountSettings(Tk):
    def __init__(self):
        super().__init__()
        windows["account settings"] = self
        self.create_screen()
        self.mainloop()

    #makes the screen
    def create_screen(root):
        #general configurations
        root.common = Common(root)
        root.common.set_screen()
        root.title("Account Settings")
        root.config(bg="white")
        #initialising constants and variables
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        root.user = cookies[0]
        root.pic = root.user['avatar']
        _avatar = Image.open(f"{PATH}/../static/Personal/Images/avatars/avatar_{root.pic}.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)

        #creating the elements
        title = Label(root, text="Account Settings", font=("Verdana", 30, "underline"), pady=50, bg="white")
        avatar_label = Label(root, text="Profile Photo", font=("Arial", 10, "bold"), bg="white")
        frame0 = Frame(root, padx=50, pady=30, highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=20, padx=50)
        frame2 = Frame(frame0, pady=30, bg="white")
        frame3 = Frame(frame0, pady=30, bg="white")
        root.common.load_toggle()
        left_btn = Button(frame1, image=root.common.BEFORE, bd=0, width=100, cursor="hand2", command=lambda: root.common.avatar_toggle(-1, "avatar"))
        root.avatar = Label(frame1, image=AVATAR, width=100)
        right_btn = Button(frame1, image=root.common.AFTER, bd=0, width=100, cursor="hand2", command=lambda: root.common.avatar_toggle(1, "avatar"))
        left_btn.image = root.common.BEFORE
        root.avatar.image = AVATAR
        right_btn.image = root.common.AFTER

        #creating the entry elements and conjugate labels
        name_label = Label(frame2, text="Your Name", font=("Arial", 10), fg=LABEL, bg="white")
        root.name = StringVar()
        root.name_entry = Entry(frame2, textvariable=root.name, font=("Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.name.set(root.user["name"])
        root.name_entry.focus()
        username_label = Label(frame2, text="Your Username", font=("Arial", 10), fg=LABEL, bg="white")
        root.username = StringVar()
        root.username_entry = Entry(frame2, textvariable=root.username, font=("Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.username.set(root.user["username"])
        email_label = Label(frame2, text="Email Address", font=("Arial", 10), fg=LABEL, bg="white")
        root.email = StringVar()
        root.email_entry = Entry(frame2, textvariable=root.email, font=("Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.email.set(root.user["email"])
        phone_label = Label(frame2, text="Phone Number (Optional)", font=("Arial", 10), fg=LABEL, bg="white")
        root.phone = StringVar()
        root.phone_entry = Entry(frame2, textvariable=root.phone, font=("Comicsans", 12), width=30, bd=10, relief=FLAT, bg=ENTRY)
        root.phone.set(root.user["phone"])
        #creating the form buttons
        save_btn = Button(frame3, text="Save Changes", bg="#0D6EFD", fg="white", activebackground=BGCOLOR, activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=root.save_changes)
        cancel_btn = Button(frame3, text="Cancel", bg="black", fg="white", activebackground="#6C757D", activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=root.common.back)

        #placing all elements
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

        #binding all entries to Save button
        root.name_entry.bind("<Return>", root.save_changes)
        root.username_entry.bind("<Return>", root.save_changes)
        root.email_entry.bind("<Return>", root.save_changes)
        root.phone_entry.bind("<Return>", root.save_changes)
        root.protocol("WM_DELETE_WINDOW", lambda: root.common.close_window("account settings"))

    #after pressing Save button
    def save_changes(self, ev=0):
        name = self.name.get().strip()
        username = self.username.get().strip()
        email = self.email.get()
        phone = self.phone.get().strip()
        #checks validity of inputs
        if name and username and email:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): #email validity using "re"
                if re.search(r"[^a-zA-Z0-9_\s]", username) == None: #username validity using "re"
                    if len(username) >= 5:
                        #updates the user data and refreshes cookie.json and logged.txt
                        extra = ""
                        if username != self.user["username"]:
                            extra = f', user_hash="{hasher.get_hash(username)}"'
                        cursor.execute(f'''update logged_users set name="{name}", username="{username}", email="{email}", avatar="{self.pic}", phone="{phone}"{extra} where id={self.user["id"]}''')
                        connection.commit()
                        self.common.refresh()
                        self.common.back()
                    else:
                        msg.showwarning("Shelfmate", "Username should be atleast 5 characters!")
                else:
                    msg.showwarning("Shelfmate", "Username can contain numbers, letters and underscore (_) only!")
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all required fields!")

#library function (Add Resources)
class AddResources(Tk):
    def __init__(self):
        super().__init__()
        windows["add resources"] = self
        self.last_isbn = ""
        self.url = "../static/Personal/Images/display/book_cover.png"
        self.create_screen()
        self.mainloop()

    #makes the screen
    def create_screen(root):
        #general configurations
        root.common = Common(root)
        root.common.set_screen()
        root.title("Add Resources")
        root.config(bg="gainsboro")
        #getting user data
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            cookies = json.load(cookie)
        root.user = cookies[0]
        root.library = cookies[1]

        #creating the frames and header
        FRAME = Frame(root)
        frame0 = Frame(FRAME, padx=50, pady=30, highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=30, bg="white")
        frame2 = Frame(frame0, bg="white")
        root.frame00 = Frame(FRAME, bg="white")
        frame01 = Frame(root.frame00, bg="white")
        frame02 = Frame(root.frame00, bg="white")
        title = Label(root, text="Add Resources", font=("Verdana", 25, "underline"), pady=50, bg="gainsboro")

        #creating the entries and conjugate labels
        #book ISBN
        isbn_label = Label(frame1, text="ISBN *", font=("Arial", 13), bg="white", padx=50)
        root.isbn = StringVar()
        root.isbn_entry = Entry(frame1, textvariable=root.isbn, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.isbn_entry.focus()
        #book title
        title_label = Label(frame1, text="Title *", font=("Arial", 13), bg="white", padx=50)
        root.title = StringVar()
        root.title_entry = Entry(frame1, textvariable=root.title, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #book edition
        edition_label = Label(frame1, text="Edition", font=( "Arial", 13), bg="white", padx=50)
        root.edition = StringVar()
        root.edition_entry = Entry(frame1, textvariable=root.edition, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #book author
        root.author_label = Label(frame1, text="Authors (0) *", font=("Arial", 13), bg="white", padx=50, cursor="hand2")
        root.author = StringVar()
        root.author_entry = Entry(frame1, textvariable=root.author, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.author_add_btn = Button(frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(0))
        root.author_sel = []
        #book category
        root.category_label = Label(frame1, text="Category (0) *", font=("Arial", 13), bg="white", padx=50, cursor="hand2")
        root.category = StringVar()
        root.category_entry = Entry(frame1, textvariable=root.category, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.category_add_btn = Button(frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(1))
        root.category_sel = []
        #book publisher
        root.publisher_label = Label(frame1, text="Publisher (0) *", font=("Arial", 13), bg="white", padx=50, cursor="hand2")
        root.publisher = StringVar()
        root.publisher_entry = Entry(frame1, textvariable=root.publisher, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.publisher_add_btn = Button(frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(2))
        root.publisher_sel = []
        #book language
        root.language_label = Label(frame1, text="Language (0) *", font=("Arial", 13), bg="white", padx=50, cursor="hand2")
        root.language = StringVar()
        root.language_entry = Entry(frame1, textvariable=root.language, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        root.language_add_btn = Button(frame1, text="Add", padx=20, pady=4, cursor="hand2", command=lambda: root.add_option(3))
        root.language_sel = []
        #book quantity
        quantity_label = Label(frame1, text="Quantity *", font=("Arial", 13), bg="white", padx=50)
        root.quantity = StringVar()
        root.quantity_entry = Entry(frame1, textvariable=root.quantity, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #submit button
        submit_btn = Button(frame2, text="Submit", fg="white", bg="black", activebackground="#111111", activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=root.submit_form)

        #creating book info displayer by ISBN
        root.book = Label(frame01)
        book_title_label = Label(frame02, font="arial 14", bg="white", text="Title: ")
        book_author_label = Label(frame02, font="arial 14", bg="white", text="Author: ")
        book_year_label = Label(frame02, font="arial 14", bg="white", text="Year: ")
        book_publisher_label = Label(frame02, font="arial 14", bg="white", text="Publisher: ")
        root.book_title = Label(frame02, font="comicsans 12", bg="white")
        root.book_author = Label(frame02, font="comicsans 12", bg="white")
        root.book_year = Label(frame02, font="comicsans 12", bg="white")
        root.book_publisher = Label(frame02, font="comicsans 12", bg="white")

        #placing all elements
        #the frames
        title.pack()
        FRAME.pack()
        frame0.grid(row=0, column=0)
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        frame01.grid(row=0, column=0)
        frame02.grid(row=2, column=0)
        #the entries and labels
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
        #the book info displayer
        root.book.grid(row=0, column=0)
        book_title_label.grid(row=1, column=0, sticky=W)
        book_author_label.grid(row=2, column=0, sticky=W)
        book_year_label.grid(row=3, column=0, sticky=W)
        book_publisher_label.grid(row=4, column=0, sticky=W)
        root.book_title.grid(row=1, column=1, sticky=W)
        root.book_author.grid(row=2, column=1, sticky=W)
        root.book_year.grid(row=3, column=1, sticky=W)
        root.book_publisher.grid(row=4, column=1, sticky=W)

        #binding all required elements
        root.author_label.bind("<Button-1>", lambda e: root.view_selected(0))
        root.category_label.bind("<Button-1>", lambda e: root.view_selected(1))
        root.publisher_label.bind("<Button-1>", lambda e: root.view_selected(2))
        root.language_label.bind("<Button-1>", lambda e: root.view_selected(3))
        root.author_entry.bind("<Return>", lambda e: root.add_option(0))
        root.category_entry.bind("<Return>", lambda e: root.add_option(1))
        root.publisher_entry.bind("<Return>", lambda e: root.add_option(2))
        root.language_entry.bind("<Return>", lambda e: root.add_option(3))
        root.isbn_entry.bind("<FocusOut>", root.find_book)
        root.isbn_entry.bind("<Return>", root.find_book)
        root.title_entry.bind("<Return>", root.submit_form)
        root.edition_entry.bind("<Return>", root.submit_form)
        root.quantity_entry.bind("<Return>", root.submit_form)
        root.protocol("WM_DELETE_WINDOW", lambda: root.common.close_window("add resources"))

    #viewer window (floating) for "author", "category", "publisher" and "language"
    def view_selected(self, type):
        #some initials
        types = ["author", "category", "publisher", "language"]
        type = types[type]
        viewer = Tk()
        common = Common(viewer)
        #decodes the type user wants to view
        if type in windows:
            common.close_window(type)
        else:
            types.remove(type)
            for t in types:
                if t in windows:
                    common.close_window(t)
        #sets the window
        windows[type] = viewer
        viewer.title(type.capitalize())
        viewer.geometry("400x200")
        viewer.resizable(0, 0)
        Label(viewer, text="Double click to delete an item", font="arial 10", fg="blue").pack()
        #creating and placing the scrollbar and listbox
        scroller = Scrollbar(viewer, width=20)
        self.tree = ttk.Treeview(viewer, yscrollcommand=scroller.set, column=type, show='headings', selectmode="browse")
        self.tree.column("# 1", anchor=CENTER, width=380)
        self.tree.heading("# 1", text=type.capitalize())
        for x in eval(f"self.{type}_sel"):
            self.tree.insert('', 'end', text=x, values=[x])
        scroller.config(command=self.tree.yview)
        self.tree.bind("<Double-1>", lambda e: self.delete_option(e, self.tree['column'][0]))
        self.tree.pack(side=LEFT, fill=Y)
        scroller.pack(side=RIGHT, fill=Y)
        #finishing
        viewer.protocol("WM_DELETE_WINDOW",lambda: common.close_window(type))
        viewer.mainloop()

    #updates the counter for the 4 categories as user updates it
    def update_count(self):
        self.author_label.config(text=f"Authors ({len(self.author_sel)}) *")
        self.category_label.config(text=f"Category ({len(self.category_sel)}) *")
        self.publisher_label.config(text=f"Publisher ({len(self.publisher_sel)}) *")
        self.language_label.config(text=f"Language ({len(self.language_sel)}) *")

    #adds values to the category user wants to among 4
    def add_option(self, type):
        types = ["author", "category", "publisher", "language"]
        type = types[type]
        value = eval(f"self.{type}_entry.get()")
        value = value.strip().replace(';', '')
        if value not in eval(f"self.{type}_sel") and value:
            eval(f"self.{type}_sel.append(value)")
        eval(f"self.{type}.set('')")
        self.update_count()

    #removes values from the category user wants to among 4
    def delete_option(self, ev, type):
        item_id = ev.widget.focus()
        item = ev.widget.item(item_id)
        data = item['values'][0]
        self.tree.delete(item_id)
        eval(f"self.{type}_sel.remove('{data}')")
        self.update_count()

    #gets the book info based on ISBN
    def find_book(self, ev=0):
        isbn = self.isbn.get()
        if isbn != self.last_isbn and isbn.strip():
            cursor.execute(f"select isbn from resources_library where user_id={self.user['id']}")
            all_isbn = cursor.fetchall()
            isbns = []
            for x in all_isbn:
                isbns.append(''.join(re.findall(r"\d+", x[0])))
            if ''.join(re.findall(r"\d+", isbn)) in isbns:
                #if book already in resources
                self.title.set("")
                self.title_entry.config(state="normal")
                msg.showwarning("Shelfmate", "This book is already in your resources!")
                self.isbn.set("")
            else:
                SERVICE = "openl"
                bibtex = bibformatters["bibtex"]
                self.last_isbn = isbn
                try:
                    urlopen('https://www.google.com') #checks network connection
                except Exception as e:
                    self.title.set("")
                    self.title_entry.config(state="normal")
                    print("[POOR CONNECTION]", e)
                else:
                    try:
                        if not any(char.isalpha() for char in isbn):
                            #extracts book info
                            res = bibtex(meta(isbn, SERVICE))
                            title = re.findall("title = {(.*)}", res)[0].replace(' and ', ", ")
                            author = ', '.join(set(re.findall("author = {(.*)}", res)[0].replace(' and ', ", ").split(', ')))
                            year = re.findall("year = {(.*)}", res)[0].replace(' and ', ", ")
                            publisher = re.findall("publisher = {(.*)}", res)[0].replace(' and ', ", ")
                            isbn = re.findall("isbn = {(.*)}", res)[0]
                            #other jobs
                            self.title.set(title)
                            self.title_entry.config(state="readonly")
                            self.author_sel = author.split(", ")
                            self.publisher_sel = [publisher]
                            self.update_count()
                            self.frame00.grid(row=0, column=1, sticky=N)
                            try:
                                #tries to fetch book image if available
                                u = requests.get(f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg")
                                self.url = u.url
                                _cover = Image.open(BytesIO(u.content))
                                if _cover.width < 10:
                                    raise ValueError
                            except:
                                #if not available sets default cover as book image
                                self.url = "../static/Personal/Images/display/book_cover.png"
                                _cover = Image.open(f"{PATH}/{self.url}")
                            #updates the book cover in info displayer
                            _cover = _cover.resize((300, 400))
                            COVER = ImageTk.PhotoImage(_cover)
                            self.book.config(image=COVER)
                            self.book.image = COVER
                            #adjusts the book info to show in displayer
                            if len(title) > 50:
                                title = title[:47]+'...'
                            if len(author) > 50:
                                author = author[:47]+'...'
                            if len(publisher) > 50:
                                publisher = publisher[:47]+'...'
                            #updates book info displayer
                            self.book_title.config(text=title)
                            self.book_author.config(text=author)
                            self.book_year.config(text=year)
                            self.book_publisher.config(text=publisher)
                        else:
                            #vanishes the displayer
                            self.frame00.grid_forget()
                            self.title.set("")
                            self.title_entry.config(state="normal")
                            print("[BAD ISBN]")
                    except Exception as e:
                        #vanishes the displayer
                        self.frame00.grid_forget()
                        self.title.set("")
                        self.title_entry.config(state="normal")
                        print("[ISBN UNTRACKABLE]", e)

    #after submitting the form
    def submit_form(form, ev=0):
        #gets all inputs
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
        #adjusts the 4 special inputs
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

        #adds the resource and updates 4 special inputs in user data
        if isbn and title and author and category and publisher and language and category and quantity:
            if msg.askyesno("Confirm", "Do you want to submit?"):
                cursor.execute(f'''insert into resources_library(isbn, title, edition, author, category, publisher, language, quantity, user_id, book_cover, borrowed, reading)
                            values ("{isbn}", "{title}", "{edition}", "{';'.join(author)};", "{';'.join(category)};", "{';'.join(publisher)};", "{';'.join(language)};", {quantity}, {cookies[0]['id']}, "{book}", 0, 0);''')
                connection.commit()
                cursor.execute(f'''update logged_users set author="{all_author}", category="{all_category}", publisher="{all_publisher}", language="{all_language}" where id={cookies[0]['id']}''')
                connection.commit()
                common = Common(form)
                common.refresh()
                msg.showinfo("Shelfmate", "Book added successfully!")
                common.close_all_windows()
                AddResources()
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")

#library function (All Resources)
class AllResources(Tk):
    def __init__(self):
        super().__init__()
        windows["all resources"] = self
        _cover = Image.open(f"{PATH}/../static/Personal/Images/display/book_cover.png")
        _cover = _cover.resize((150, 200))
        self.INIT_COVER = ImageTk.PhotoImage(_cover)
        self.create_screen()
        self.mainloop()

    def create_screen(root):
        #general configurations
        root.common = Common(root)
        root.common.set_screen()
        root.title("All Resources")
        root.config(bg="gainsboro")
        #getting resources of user
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(f"select * from resources_library where user_id={root.user_id}")
        root.books = cursor.fetchall()

        #creating, packing and binding the scrollable canvas (mainly copy-pasted)
        BIG_FRAME = Frame(root)
        root.canvas = Canvas(BIG_FRAME, bg="gainsboro")
        root.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        root.scrollbar = Scrollbar(BIG_FRAME, orient=VERTICAL, command=root.canvas.yview)
        root.scrollbar.pack(side=RIGHT, fill=Y)
        root.canvas.configure(yscrollcommand=root.scrollbar.set)
        root.canvas.bind("<Configure>", lambda e: root.canvas.config(scrollregion=root.canvas.bbox(ALL)))
        FRAME = Frame(root.canvas, bg="gainsboro")
        root.canvas.create_window((0, 0), window=FRAME, anchor="nw")
        root.canvas.bind_all("<MouseWheel>", root._on_mousewheel)
        root.bind("<Configure>", root._on_configure)
        #the header
        title = Label(root, text="All Resources", font=("Verdana", 25, "underline"), pady=20, bg="gainsboro")

        #initialising some global variables
        root.book_holders = [] #used to change the default cover with the book cover after it's loaded
        root.frame0_holders = [] #stores all the book frames (used to switch between edit and display mode)
        root.buttons = [] #stores the function buttons for each book (used to switch button jobs in two modes)
        root.book_cards = {} #used to target the book to be deleted
        root.STATUS = [] #flag storage for each book that whether it is in display or edit mode

        #loop run to create each resource card
        for i in range(len(root.books)):
            #creating all elements
            thebook = root.books[i]
            frame = Frame(FRAME, bg=CARDBG, padx=20, pady=10)
            frame0 = Frame(frame, bg="white", padx=10, pady=5)
            frame1 = Frame(frame)
            frame2 = Frame(frame0)
            book = Label(frame1, image=root.INIT_COVER)
            book.image = root.INIT_COVER
            name = Label(frame, text=thebook[2], font="comicsans 15", bg=CARDBG, wraplength=300)
            btn1 = Button(frame2, text="Edit", font="robota 12", bg="black", fg="white", activebackground="grey", activeforeground="white", bd=0, cursor="hand2", command=lambda e=(thebook[0], i): root.edit_res(*e))
            btn2 = Button(frame2, text="Delete", font="robota 12", bg="#C51605", fg="white", activebackground="grey", activeforeground="white", bd=0, cursor="hand2", command=lambda e=(thebook[0], i): root.delete_res(*e))

            #updating the global storage variables
            root.book_cards[thebook[0]] = frame
            root.book_holders.append(book)
            root.frame0_holders.append(frame0)
            root.buttons.append((btn1, btn2))
            root.STATUS.append(1)

            #placing all elements
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

        #final packing of whole screen
        root.show_card_set() #starts all resources in display mode
        title.pack()
        BIG_FRAME.pack(fill=BOTH, expand=1)

        #loads image in background without freezing main window (using threads)
        image_loading_thread = threading.Thread(target=root.load_covers)
        image_loading_thread.daemon = True #exits automatically without error on closing application
        image_loading_thread.start()
        root.protocol("WM_DELETE_WINDOW",lambda: root.common.close_window("all resources"))

    #functioning mousewheel to scroll the canvas (copy-pasted)
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    #properly binding the canvas with scroller (copy-pasted)
    def _on_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.pack_forget()
        self.scrollbar.pack(side=RIGHT, fill=Y)

    #designs the display mode of resources
    def adjust_card(self, frame0, thebook):
        #destroys the edit mode
        for content in frame0.winfo_children()[1:]:
            content.destroy()
        
        #creating all elements
        lbl0 = Label(frame0, text=f"ISBN - {thebook[1]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl1 = Label(frame0, text=f"Authors - {thebook[4].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl2 = Label(frame0, text=f"Publisher - {thebook[6].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl3 = Label(frame0, text=f"Category - {thebook[5].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl4 = Label(frame0, text=f"Language - {thebook[7].replace(';', ', ')[:-2]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl5 = Label(frame0, text=f"Edition - {thebook[3]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl6 = Label(frame0, text=f"Available - {thebook[8]-thebook[11]-thebook[12]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl7 = Label(frame0, text=f"Borrowed - {thebook[11]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)
        lbl8 = Label(frame0, text=f"Reading - {thebook[12]}", bg="white", font="comicsans 13", wraplength=300, justify=RIGHT)

        #placing all elements
        for i in range(9):
            eval(f"lbl{i}.grid(row={i}, column=0, sticky=W)")

    #triggers display mode for a target book
    def show_card_set(root, target=None, thebook=None):
        if target == None: #for making the beginning screen
            for i in range(len(root.books)):
                frame0 = root.frame0_holders[i]
                thebook = root.books[i]
                root.adjust_card(frame0, thebook)
        else: #for switching to display mode from edit mode (specific target)
            frame0 = root.frame0_holders[target]
            if thebook == None:
                thebook = root.books[target]
            root.adjust_card(frame0, thebook)
            root.STATUS[target] = 1
            #changing button texts
            root.buttons[target][0].config(text="Edit")
            root.buttons[target][1].config(text="Delete")

    #triggers edit mode for a target book
    def edit_card_set(root, target, thebook=None):
        #destroys the display mode
        frame0 = root.frame0_holders[target]
        for content in frame0.winfo_children()[1:]:
            content.destroy()
        root.STATUS[target] = 0

        #creating all elements
        l0_frame = Frame(frame0)
        l0_lbl = Label(l0_frame, text="Authors - ", bg="white", font="comicsans 13")
        root.aut_var = StringVar()
        root.aut_var.set(thebook[4].replace(';', ', ')[:-2])
        l0 = Entry(l0_frame, bg="white", font="comicsans 13", textvariable=root.aut_var)
        l1_frame = Frame(frame0)
        l1_lbl = Label(l1_frame, text="Publisher - ", bg="white", font="comicsans 13")
        root.pub_var = StringVar()
        root.pub_var.set(thebook[6].replace(';', ', ')[:-2])
        l1 = Entry(l1_frame, bg="white", font="comicsans 13", textvariable=root.pub_var)
        l2_frame = Frame(frame0)
        l2_lbl = Label(l2_frame, text="Category - ", bg="white", font="comicsans 13")
        root.cat_var = StringVar()
        root.cat_var.set(thebook[5].replace(';', ', ')[:-2])
        l2 = Entry(l2_frame, bg="white", font="comicsans 13", textvariable=root.cat_var)
        l3_frame = Frame(frame0)
        l3_lbl = Label(l3_frame, text="Language - ", bg="white", font="comicsans 13")
        root.lan_var = StringVar()
        root.lan_var.set(thebook[7].replace(';', ', ')[:-2])
        l3 = Entry(l3_frame, bg="white", font="comicsans 13", textvariable=root.lan_var)
        l4_frame = Frame(frame0)
        l4_lbl = Label(l4_frame, text="Edition - ", bg="white", font="comicsans 13")
        root.edi_var = StringVar()
        root.edi_var.set(thebook[3])
        l4 = Entry(l4_frame, bg="white", font="comicsans 13", textvariable=root.edi_var)
        l5_frame = Frame(frame0)
        l5_lbl = Label(l5_frame, text="Available - ", bg="white", font="comicsans 13")
        root.avail_var = StringVar()
        root.avail_var.set(thebook[8]-thebook[11]-thebook[12])
        l5 = Entry(l5_frame, bg="white", font="comicsans 13", textvariable=root.avail_var)

        #placing all elements
        for i in range(6):
            eval(f"l{i}_frame.grid(row={i}, column=0, sticky=W)")
            eval(f"l{i}_lbl.grid(row={i}, column=0, sticky=W)")
            eval(f"l{i}.grid(row={i}, column=1, sticky=W)")
        
        #changing button texts
        root.buttons[target][0].config(text="Save")
        root.buttons[target][1].config(text="Cancel")

    #loads the book covers in separate thread from external website
    def load_covers(self):
        try:
            for i in range(len(self.books)):
                book = self.books[i]
                _url = book[10]
                if _url.startswith('../static'):
                    cover = self.INIT_COVER
                else:
                    cover = ImageTk.PhotoImage(Image.open(BytesIO(requests.get(_url).content)).resize((150, 200)))
                self.book_holders[i].config(image=cover)
                self.book_holders[i].image = cover
        except Exception as e:
            print("[BOOK DELETED]", e)

    #function of second button
    def delete_res(self, book, target):
        if self.STATUS[target]: #delete function (in display mode)
            if msg.askyesno("Shelfmate", "Do you really want to delete this book?"):
                cursor.execute(f"delete from resources_library where id={book}")
                connection.commit()
                for content in self.book_cards[book].winfo_children():
                    content.destroy()
                Label(self.book_cards[book], text="(Deleted)", font="comicsans 30", bg="#94ADD7", fg="#C51605").pack()
        else: #cancel function (in edit mode)
            self.show_card_set(target)

    #function of first button
    def edit_res(self, book, target):
        if self.STATUS[target]: #edit function (in display mode)
            cursor.execute(f"select * from resources_library where user_id={self.user_id} and id={book}")
            thebook = cursor.fetchone()
            self.edit_card_set(target, thebook)
        else: #save function (in edit mode)
            #gets the user inputs
            aut = self.aut_var.get()
            pub = self.pub_var.get()
            cat = self.cat_var.get()
            lan = self.lan_var.get()
            edi = self.edi_var.get()

            #calculates the available books
            cursor.execute(f"select borrowed, reading, quantity from resources_library where id={book}")
            bor, read, prev = cursor.fetchone()
            try:
                avail = int(self.avail_var.get())
                1/(avail >= 0)
            except:
                avail = prev-bor-read

            #updates the values
            cursor.execute(f'''update resources_library
                           set author="{aut.replace(', ', ';')};", publisher="{pub.replace(', ', ';')};", category="{cat.replace(', ', ';')};", language="{lan.replace(', ', ';')};", edition="{edi}", quantity={avail+bor+read}
                           where id={book}''')
            connection.commit()
            #displays the updated book
            cursor.execute(f"select * from resources_library where user_id={self.user_id} and id={book}")
            thebook = cursor.fetchone()
            self.show_card_set(target, thebook)

#library function (Library Details)
class LibraryDetails(Tk):
    def __init__(self):
        super().__init__()
        windows["library details"] = self
        self.create_screen()
        self.mainloop()

    #makes the screen
    def create_screen(root):
        #general configuration
        root.common = Common(root)
        root.common.set_screen()
        root.title("Library Details")
        root.config(bg="gainsboro")
        #gets user data
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.cookie = json.load(cookie)
        
        #creating and packing header and main frame
        title = Label(root, text="Library Details", font=("Verdana", 25, "underline"), pady=40, bg="gainsboro")
        root.FRAME = Frame(root)
        title.pack()
        root.FRAME.pack()

        #if-else condition for whether to show display window or edit window
        if root.cookie[2]['library_name']:
            root.display_screen()
        else:
            root.edit_screen()
        root.protocol("WM_DELETE_WINDOW",lambda: root.common.close_window("library details"))

    #the edit window
    def edit_screen(root, edit=False):
        #creating the frames
        frame0 = Frame(root.FRAME, padx=50, pady=20, highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=20, bg="white")
        frame2 = Frame(frame0, bg="white")

        #creating the entries and conjugate labels
        #library name
        lbl0 = Label(frame1, text="Library Name *", font=("Arial", 13), bg="white", padx=50)
        root.name = StringVar()
        ent0 = Entry(frame1, textvariable=root.name, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        ent0.focus()
        #library email
        lbl1 = Label(frame1, text="Email *", font=("Arial", 13), bg="white", padx=50)
        root.email = StringVar()
        ent1 = Entry(frame1, textvariable=root.email, font=( "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #library phone number
        lbl2 = Label(frame1, text="Phone number *", font=("Arial", 13), bg="white", padx=50)
        root.phone = StringVar()
        ent2 = Entry(frame1, textvariable=root.phone, font=( "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #library address
        lbl3 = Label(frame1, text="Address *", font=("Arial", 13), bg="white", padx=50)
        root.add1 = StringVar()
        root.add2 = StringVar()
        root.dist = StringVar()
        root.stt = StringVar()
        root.pin = StringVar()
        root.country = StringVar()
        ent3 = Frame(frame1, bg="white")
        add1_lbl = Label(ent3, text="Address Line 1", font=( "Arial", 10), fg=LABEL, bg="white")
        root.add1_ent = Entry(ent3, textvariable=root.add1, font=( "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        add2_lbl = Label(ent3, text="Address Line 2", font=( "Arial", 10), fg=LABEL, bg="white")
        root.add2_ent = Entry(ent3, textvariable=root.add2, font=( "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        ent3x = Frame(ent3, bg="white")
        dist_lbl = Label(ent3x, text="District", font=( "Arial", 10), fg=LABEL, bg="white")
        root.dist_ent = Entry(ent3x, textvariable=root.dist, font=( "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        stt_lbl = Label(ent3x, text="State", font=( "Arial", 10), fg=LABEL, bg="white")
        root.stt_ent = Entry(ent3x, textvariable=root.stt, font=( "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        ent3y = Frame(ent3, bg="white")
        pin_lbl = Label(ent3y, text="Postal Code", font=( "Arial", 10), fg=LABEL, bg="white")
        root.pin_ent = Entry(ent3y, textvariable=root.pin, font=( "Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        country_lbl = Label(ent3y, text="Country", font=( "Arial", 10), fg=LABEL, bg="white")
        root.country_ent = ttk.Combobox(ent3y, textvariable=root.country, width=20, values=COUNTRIES, state="readonly")
        root.country.set(COUNTRIES[0])
        lbl4 = Label(frame1, text="Library Website", font=("Arial", 13), bg="white", padx=50)
        root.web = StringVar()
        ent4 = Entry(frame1, textvariable=root.web, font=( "Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)

        #creating the buttons
        save_btn = Button(frame2, text="Save", bg="#0D6EFD", fg="white", activebackground=BGCOLOR, padx=5, activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=root.save)
        cancel_btn = Button(frame2, text="Cancel", bg="black", fg="white", activebackground="#6C757D", padx=5, activeforeground="white", font=("Comicsans", 13), relief=FLAT, cursor="hand2", command=lambda: root.cancel(edit))

        #placing all elements
        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        save_btn.grid(row=0, column=0, padx=10)
        cancel_btn.grid(row=0, column=1, padx=10)
        root.common.address_packer(add1_lbl, add2_lbl, ent3x, ent3y, dist_lbl, stt_lbl, pin_lbl, country_lbl)
        for i in range(5):
            eval(f"lbl{i}.grid(row={i}, column=0, sticky=W, pady=10)")
            eval(f"ent{i}.grid(row={i}, column=1, padx=50, pady=10)")
        for i in range(5):
            if i == 3:
                continue
            eval(f"ent{i}.bind('<Return>', root.save)")
        for x in ["add1", "add2", "dist", "stt", "pin", "country"]:
            eval(f"root.{x}_ent.bind('<Return>', root.save)")

        #if not inputing values for first time the entries are set to the previous values from cookie.json
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

    #the display window
    def display_screen(root):
        LINK = "#0A6EBD"
        #creating all frames
        frame0 = Frame(root.FRAME, padx=50, pady=30, highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=30, bg="white")
        frame2 = Frame(frame0, bg="white")

        #creating all display elements and buttons
        q0 = Label(frame1, text="Library Name", font=("Arial", 13), bg="white", padx=50)
        a0 = Label(frame1, text=root.cookie[2]["library_name"], font=("Arial", 13), bg="white", padx=50)
        q1 = Label(frame1, text="Phone number", font=("Arial", 13), bg="white", padx=50)
        a1 = Label(frame1, text=root.cookie[2]["library_phone"], font=("Arial", 13), bg="white", padx=50)
        q2 = Label(frame1, text="Email", font=("Arial", 13), bg="white", padx=50)
        a2 = Label(frame1, text=root.cookie[2]["library_email"], font=( "Arial", 13, 'underline'), bg="white", padx=50, fg=LINK, cursor="hand2")
        q3 = Label(frame1, text="Address", font=("Arial", 13), bg="white", padx=50)
        a3 = Label(frame1, text=root.cookie[2]["library_address"].replace( ';;', ';').replace(';', ', '), font=("Arial", 13), bg="white", padx=50)
        q4 = Label(frame1, text="Library Website", font=("Arial", 13), bg="white", padx=50)
        a4 = Label(frame1, text=root.cookie[2]["library_url"], font=("Arial", 13, 'underline'), bg="white", padx=50, fg=LINK, cursor="hand2")
        btn1 = Button(frame2, text="Edit", font="robota 12", bg="black", fg="white", activebackground="grey", activeforeground="white", bd=0, cursor="hand2", padx=5, command=root.edit)
        btn2 = Button(frame2, text="Delete", font="robota 12", bg="#C51605", fg="white", activebackground="grey", activeforeground="white", bd=0, cursor="hand2", padx=5, command=root.delete)

        #binding email and website links to open externally
        a2.bind("<Button-1>", lambda e: web.open(f"mailto:{root.cookie[2]['library_email']}"))
        a4.bind("<Button-1>", lambda e: web.open(root.cookie[2]['library_url']))

        #placing all elements
        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        btn1.grid(row=0, column=0, padx=20, pady=10)
        btn2.grid(row=0, column=1, padx=20, pady=10)
        for i in range(5):
            eval(f"q{i}.grid(row={i}, column=0, sticky=W, pady=2)")
            eval(f"a{i}.grid(row={i}, column=1, sticky=W, pady=2)")
    
    #after clicking the Save button
    def save(self, ev=0):
        #gets all user inputs
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

        #checks validity of inputs
        if name and email and phone and add1 and dist and stt and pin:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): #email validity using "re"
                if validators.url(website): #website validity using "validators"
                    #updates the database with new values
                    cursor.execute(f'''update logged_users
                                set library_name="{name}", library_email="{email}", library_phone="{phone}", library_address="{address}", library_url="{website}"
                                where id={self.cookie[0]['id']}''')
                    self.common.refresh() #refreshes cookie.json
                    self.common.close_all_windows()
                    LibraryDetails()
                else:
                    msg.showwarning("Shelfmate", "Invalid URL!")
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")

    #deletes all library details
    def delete(self):
        if msg.askyesno("Shelfmate", "Are you sure you want to delete your Library Details?"):
            #clears the library details from database
            cursor.execute(f'''update logged_users
                           set library_name="", library_email="", library_phone="", library_address="", library_url=""
                           where id={self.cookie[0]['id']}''')
            self.common.refresh() #refreshes cookie.json
            self.common.close_all_windows()
            LibraryDetails()
    
    #on clicking the Edit button (in display window)
    def edit(self):
        for x in self.FRAME.winfo_children():
            x.destroy()
        self.edit_screen(True)

    #on clicking the Cancel button (in edit window)
    def cancel(self, edit):
        if edit: #if data already added then returns to display window
            for x in self.FRAME.winfo_children():
                x.destroy()
            self.display_screen()
        else: #else returns to dashboard
            self.common.back()

#library function (Add Members)
class AddMembers(Tk):
    def __init__(self, mode=0, member=None):
        super().__init__()
        windows["add members"] = self
        #initializing global variables
        self.pic = 0
        self.suggest_clicks = 0
        #mode is a flag (0 = adding new member, 1 = editing an existing member)
        self.create_screen(mode)
        if mode:
            self.mode_work(member)
        self.mainloop()

    #makes the screen
    def create_screen(root, mode):
        #general configurations
        root.common = Common(root)
        root.common.set_screen(back=not mode)
        root.title("Add Members")
        root.config(bg="gainsboro")
        #gets user data
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        
        #creating header and frames
        title = Label(root, text="Add Members", font=("Verdana", 25, "underline"), pady=40, bg="gainsboro")
        FRAME = Frame(root)
        frame0 = Frame(FRAME, padx=50, pady=20, highlightthickness=1, bg="white")
        frame1 = Frame(frame0, pady=20, bg="white")
        frame2 = Frame(frame0, bg="white")

        #creating entries and conjugate labels
        #member name
        q0 = Label(frame1, text="Name *", font=("Arial", 13), bg="white", padx=50)
        root.name = StringVar()
        a0 = Entry(frame1, textvariable=root.name, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #member username
        q1 = Label(frame1, text="Username *", font=("Arial", 13), bg="white", padx=50)
        root.username = StringVar()
        a1 = Entry(frame1, textvariable=root.username, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #suggest button to suggest username
        suggest = Button(frame1, text="Suggest", cursor="hand2", font=("Arial", 10), padx=10, pady=5, command=root.suggest)
        #member email
        q2 = Label(frame1, text="Email *", font=("Arial", 13), bg="white", padx=50)
        root.email = StringVar()
        a2 = Entry(frame1, textvariable=root.email, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #member phone number
        q3 = Label(frame1, text="Phone Number", font=("Arial", 13), bg="white", padx=50)
        root.phone = StringVar()
        a3 = Entry(frame1, textvariable=root.phone, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        #member address
        q4 = Label(frame1, text="Address", font=("Arial", 13), bg="white", padx=50)
        root.add1 = StringVar()
        root.add2 = StringVar()
        root.dist = StringVar()
        root.stt = StringVar()
        root.pin = StringVar()
        root.country = StringVar()
        a4 = Frame(frame1, bg="white")
        add1_lbl = Label(a4, text="Address Line 1", font=("Arial", 10), fg=LABEL, bg="white")
        root.add1_ent = Entry(a4, textvariable=root.add1, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        add2_lbl = Label(a4, text="Address Line 2", font=("Arial", 10), fg=LABEL, bg="white")
        root.add2_ent = Entry(a4, textvariable=root.add2, font=("Comicsans", 12), width=30, bd=5, relief=FLAT, bg=ENTRY)
        ent3x = Frame(a4, bg="white")
        dist_lbl = Label(ent3x, text="District", font=("Arial", 10), fg=LABEL, bg="white")
        root.dist_ent = Entry(ent3x, textvariable=root.dist, font=("Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        stt_lbl = Label(ent3x, text="State", font=("Arial", 10), fg=LABEL, bg="white")
        root.stt_ent = Entry(ent3x, textvariable=root.stt, font=("Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        ent3y = Frame(a4, bg="white")
        pin_lbl = Label(ent3y, text="Postal Code", font=("Arial", 10), fg=LABEL, bg="white")
        root.pin_ent = Entry(ent3y, textvariable=root.pin, font=("Comicsans", 12), width=14, bd=5, relief=FLAT, bg=ENTRY)
        country_lbl = Label(ent3y, text="Country", font=("Arial", 10), fg=LABEL, bg="white")
        root.country_ent = ttk.Combobox(ent3y, textvariable=root.country, width=20, values=COUNTRIES, state="readonly")
        root.country.set(COUNTRIES[0])

        #creating member avatar and its controls
        q5 = Label(frame1, text="Avatar *", font=("Arial", 13), bg="white", padx=50)
        a5 = Frame(frame1, bg=ENTRY, pady=10, padx=20)
        root.common.load_toggle()
        _avatar = Image.open(f"{PATH}/../static/Personal/Images/members/member_0.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)
        left_btn = Button(a5, image=root.common.BEFORE, bd=0, width=100, cursor="hand2", command=lambda: root.common.avatar_toggle(-1, "member"))
        root.avatar = Label(a5, image=AVATAR, width=100)
        right_btn = Button(a5, image=root.common.AFTER, bd=0, width=100, cursor="hand2", command=lambda: root.common.avatar_toggle(1, "member"))
        left_btn.image = root.common.BEFORE
        root.avatar.image = AVATAR
        right_btn.image = root.common.AFTER

        #creating the buttons
        submit_btn = Button(frame2, text="Submit", fg="white", bg="#1D5D9B", activebackground="#111111", activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=lambda: root.submit_form(mode))
        cancel_btn = Button(frame2, text="Cancel", fg="white", bg="black", activebackground="#111111", activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=root.cancel_form)

        #placing all elements
        title.pack()
        FRAME.pack()
        frame0.pack()
        frame1.grid(row=0, column=0)
        frame2.grid(row=1, column=0)
        left_btn.grid(row=0, column=0)
        root.avatar.grid(row=0, column=1)
        right_btn.grid(row=0, column=2)
        root.common.address_packer(add1_lbl, add2_lbl, ent3x, ent3y, dist_lbl, stt_lbl, pin_lbl, country_lbl)
        for i in range(6):
            eval(f"q{i}.grid(row={i//2}, column={2*(i%2)}, sticky=W, pady=10)")
            eval(f"a{i}.grid(row={i//2}, column={2*(i%2)+1}, padx=40, pady=10)")
        suggest.grid(row=0, column=4, sticky=W, pady=10)
        submit_btn.grid(row=0, column=0, pady=30, padx=10)

        #if in editing mode, username is not chnageable
        if mode:
            cancel_btn.grid(row=0, column=1, pady=30, padx=10)
            a1.config(state=DISABLED)
            suggest.destroy()
        root.protocol("WM_DELETE_WINDOW", lambda: root.common.close_window("add members"))

    #username suggestion function
    def suggest(self, fetch=True, usernames=None):
        #fetch is a flag (True = it asks database for all usernames, False = no contact with database)
        #gets all used usernames by the user for members
        if fetch and not self.suggest_clicks:
            cursor.execute(f"select username from members_library where user_id={self.user_id}")
        usernames = [x[0] for x in cursor.fetchall()]

        #creates a random suggestion ("random" for random choice, "string" for getting ASCII character set)
        suggestion = ''.join(random.choices(string.ascii_letters+string.digits+'_', k=10))
        #checks if username is already used
        if suggestion in usernames:
            #recurssion until username is new
            self.suggest(False, usernames)
        else:
            #sets the username value to entry field for user to see
            self.username.set(suggestion)
            self.suggest_clicks += 1

    #after clicking the Submit button
    def submit_form(form, mode):
        #gets all user inputs
        name = form.name.get()
        username = form.username.get().strip()
        email = form.email.get()
        phone = form.phone.get()
        address = ';'.join([form.add1.get().strip().replace(';', ''), form.add2.get().strip().replace(';', ''), form.dist.get().strip().replace(';', ''), form.stt.get().strip().replace(';', ''), form.pin.get().strip().replace(';', ''), form.country.get()])
        avatar = form.pic

        #checks validity of inputs
        if name and username and email:
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): #email validity using "re"
                if mode:
                    #if in edit mode, updates the member
                    cursor.execute(f'''update members_library
                                   set name="{name}", email="{email}", phone="{phone}", address="{address}", avatar={avatar}
                                   where user_id={form.user_id} and username="{username}";''')
                else:
                    #if in add mode, adds a new member to database
                    cursor.execute(f'''insert into members_library(name, username, email, phone, address, avatar, user_id, visits)
                                values("{name}", "{username}", "{email}", "{phone}", "{address}", {avatar}, {form.user_id}, 0);''')
                    msg.showinfo("Shelfmate", "Member added successfully!")
                connection.commit()
                form.common.close_all_windows()
                #opens new window depending on mode value
                if mode:
                    AllMembers()
                else:
                    AddMembers()
            else:
                msg.showwarning("Shelfmate", "Invalid email!")
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")

    #on clicking Cancel button (in edit mode)
    def cancel_form(form):
        form.common.close_all_windows()
        AllMembers()

    #fills entries with old values (in edit mode)
    def mode_work(form, member):
        form.name.set(member[1])
        form.username.set(member[5])
        form.email.set(member[3])
        form.phone.set(member[2])
        address = member[4].split(';')
        form.add1.set(address[0])
        form.add2.set(address[1])
        form.dist.set(address[2])
        form.stt.set(address[3])
        form.pin.set(address[4])
        form.country.set(address[5])
        form.pic = member[6]
        _avatar = Image.open(f"{PATH}/../static/Personal/Images/members/member_{form.pic}.png")
        _avatar = _avatar.resize((70, 70))
        AVATAR = ImageTk.PhotoImage(_avatar)
        form.avatar.config(image=AVATAR)
        form.avatar.image = AVATAR

#library function (All Members)
class AllMembers(Tk):
    def __init__(self):
        super().__init__()
        windows["all members"] = self
        self.create_screen()
        self.mainloop()

    #makes the screen
    def create_screen(root):
        #general configurations
        root.common = Common(root)
        root.common.set_screen()
        root.title("All Members")
        root.config(bg="gainsboro")
        #gets user data
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(f"select * from members_library where user_id={root.user_id}")
        root.members = cursor.fetchall()

        #creating header
        title = Label(root, text="All Members", font=("Verdana", 25, "underline"), pady=40, bg="gainsboro")

        #creating, packing and binding the scrollable canvas (mainly copy-pasted)
        BIG_FRAME = Frame(root)
        root.canvas = Canvas(BIG_FRAME, bg="gainsboro")
        root.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        root.scrollbar = Scrollbar(BIG_FRAME, orient=VERTICAL, command=root.canvas.yview)
        root.scrollbar.pack(side=RIGHT, fill=Y)
        root.canvas.configure(yscrollcommand=root.scrollbar.set)
        root.canvas.bind("<Configure>", lambda e: root.canvas.config(scrollregion=root.canvas.bbox(ALL)))
        FRAME = Frame(root.canvas, bg="gainsboro")
        root.canvas.create_window((0, 0), window=FRAME, anchor="nw")
        root.canvas.bind_all("<MouseWheel>", root._on_mousewheel)
        root.bind("<Configure>", root._on_configure)

        root.member_cards = {} #disctionary to store all member card frames
        #creates display card for each member using loop
        for i in range(len(root.members)):
            themember = root.members[i]
            #creating the frames
            frame = Frame(FRAME, bg=CARDBG, padx=20, pady=10)
            frameX = Frame(frame, bg="white")
            frame0 = Frame(frameX, bg="white", padx=10, pady=5)
            frame1 = Frame(frameX, bg="white", padx=10, pady=5)
            #gets and sets the member image
            _avatar = Image.open(f"{PATH}/../static/Personal/Images/members/member_{themember[6]}.png")
            _avatar = _avatar.resize((100, 100))
            AVATAR = ImageTk.PhotoImage(_avatar)
            avatar = Label(frame0, image=AVATAR, bg="white")
            avatar.image = AVATAR

            #adding values to the dictionary during loop
            root.member_cards[themember] = frameX

            #gets all other info
            username = Label(frame0, text=f"({themember[5]})",font="arial 12", fg="grey", bg="white")
            address = ', '.join([x for x in themember[4].split(';') if x])
            name = themember[1]
            email = themember[3]
            #adjusts the member info as space friendly
            if len(address) > 30:
                address = address[:29]+'...'
            if len(name) > 30:
                name = name[:29]+'...'
            if len(email) > 30:
                email = email[:29]+'...'
            
            #creating all elements
            info0 = Label(frame1, text=name, font="comicsans 15 bold", bg="white")
            info1 = Label(frame1, text=address, bg="white", fg="grey")
            info2 = Label(frame1, text=themember[2], bg="white")
            info3 = Label(frame1, text=email, fg="#0A6EBD", font="comicsans 10 underline", bg="white", cursor="hand2")
            info4 = Frame(frame1, bg="white")
            btn1 = Button(info4, text="Edit", font="robota 12", bg="black", fg="white", activebackground="grey", activeforeground="white", bd=0, cursor="hand2", command=lambda e=themember: root.edit_mem(e))
            btn2 = Button(info4, text="Delete", font="robota 12", bg="#C51605", fg="white", activebackground="grey", activeforeground="white", bd=0, cursor="hand2", command=lambda e=themember: root.delete_mem(e))
            #binding the email to open a link
            info3.bind("<Button-1>", lambda e: web.open(f"mailto:{themember[3]}"))

            #placing all elements
            frame.grid(row=i//3, column=i % 3, padx=30, pady=20, sticky=W)
            frameX.pack()
            frame0.grid(row=0, column=0)
            frame1.grid(row=0, column=1)
            avatar.grid(row=0, column=0, pady=10)
            username.grid(row=1, column=0)
            btn1.grid(row=0, column=0, padx=5, pady=2)
            btn2.grid(row=0, column=1, padx=5, pady=2)
            for i in range(5):
                if i == 2 and not themember[2]:
                    continue
                eval(f"info{i}.grid(row={i}, column=0, sticky=E, pady=5)")

        #packing the main elements
        title.pack()
        BIG_FRAME.pack(fill=BOTH, expand=1)
        root.protocol("WM_DELETE_WINDOW",lambda: root.common.close_window("all members"))

    #functioning mousewheel to scroll the canvas (copy-pasted)
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    #properly binding the canvas with scroller (copy-pasted)
    def _on_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.pack_forget()
        self.scrollbar.pack(side=RIGHT, fill=Y)
    
    #opens edit screen for a target member
    def edit_mem(self, member):
        self.common.close_all_windows()
        AddMembers(1, member)

    #deletes a target member
    def delete_mem(self, member):
        if msg.askyesno("Shelfmate", "Do you really want to remove this member?"):
            #deletes the member from database
            cursor.execute(f"delete from members_library where id={member[0]};")
            connection.commit()
            #destroys all elements inside frame
            for content in self.member_cards[member].winfo_children():
                content.destroy()
            #packs a DELETE text in place of that
            Label(self.member_cards[member], text="(Deleted)", font="comicsans 30", bg="#94ADD7", fg="#C51605").pack()

#library function (Check In User)
class CheckInUser(Tk):
    def __init__(self):
        super().__init__()
        windows["check in"] = self
        self.create_screen()
        self.mainloop()
    
    #makes the screen
    def create_screen(root):
        #general configuration
        root.common = Common(root)
        root.common.set_screen()
        root.title("Check-In User")
        root.config(bg="gainsboro")
        #gets user data
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(f"select id, name from members_library where user_id={root.user_id}")
        MEMBERS = [f"{x[0]} - {x[1]}" for x in cursor.fetchall()]
        cursor.execute(f"select isbn, title, quantity from resources_library where user_id={root.user_id}")
        RESOURCES = [f"{x[1]} ({x[0]})" for x in cursor.fetchall() if x[2]>0]
        
        #creating header and frames
        title = Label(root, text="Check-In Member", font=("Verdana", 25, "underline"), pady=40, bg="gainsboro")
        FRAME = Frame(root, bg="white")
        root.frame0 = Frame(FRAME, bg="white")
        frame1 = Frame(FRAME, bg="white")

        #creating all entries and respective labels
        root.q0 = Label(root.frame0, text="Member *", font=("Arial", 18), bg="white", padx=50)
        root.member = StringVar()
        a0 = ttk.Combobox(root.frame0, textvariable=root.member, width=20, values=MEMBERS, state="readonly", font=("Arial", 15))
        root.q1 = Label(root.frame0, text="In Time *", font=("Arial", 18), bg="white", padx=50)
        root.intime = StringVar()
        a1 = Entry(root.frame0, textvariable=root.intime, font=("Comicsans", 15), width=21, bd=5, relief=FLAT, bg=ENTRY, state="readonly")
        root.set_current_time()
        root.q2 = Label(root.frame0, text="Resources (0) *", font=("Arial", 18), bg="white", padx=50, cursor="hand2")
        root.resource = StringVar()
        root.resources_sel = [] #stores selected resources
        a2 = ttk.Combobox(root.frame0, textvariable=root.resource, width=20, values=RESOURCES, state="readonly", font=("Arial", 15))
        root.q3 = Label(root.frame0, text="Purpose", font=("Arial", 18), bg="white", padx=50)
        a3 = Frame(root.frame0, bg="white")
        root.text = Text(a3, width=21, height=4, font=("Arial", 15), bg=ENTRY)
        root.counter = Label(root.frame0, text="0/100", font=("Roboto", 10), bg="white")
        submit = Button(frame1, text="Submit", fg="white", bg="black", activebackground="#111111", activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=root.submit_form)
        
        #placing all elements
        title.pack()
        FRAME.pack()
        root.frame0.grid(row=0, column=0, padx=100, pady=50)
        frame1.grid(row=1, column=0, pady=30)
        root.text.grid(row=0, column=0)
        root.counter.grid(row=3, column=2, sticky=SW, pady=10)
        submit.pack()
        for i in range(4):
            eval(f"root.q{i}.grid(row={i}, column=0, sticky=W, pady=10)")
            eval(f"a{i}.grid(row={i}, column=1, padx=40, pady=10)")

        #binding some elements
        a1.bind("<Button-1>", root.pick_time)
        a2.bind("<<ComboboxSelected>>", root.add_option)
        root.q2.bind("<Button-1>", root.view_selected)
        root.text.bind("<KeyPress>", root.check_words)
        root.text.bind("<KeyRelease>", root.check_words)
        root.protocol("WM_DELETE_WINDOW", lambda: root.common.close_window("check in"))

    #sets current time
    def set_current_time(root, close=0):
        #sets current time by default
        root.intime.set(root.common.get_time())
        if close:
            root.common.close_window("picker")

    #creates the date-time picker box
    def pick_time(self, ev=0):
        #restarts if already opened
        if "picker" in windows:
            self.common.close_window("picker")
        #general configuration
        root = Tk()
        root.title("Date Time Picker")
        root.resizable(0, 0)
        windows["picker"] = root
        time_now = datetime.now() #current time

        #some constant arrays
        HOURS = [f"0{i}" if i<10 else i for i in range(24)]
        MINUTES = [f"0{i}" if i<10 else i for i in range(60)]

        #creating all elements
        calender_lbl = Label(root, text="Date", font=("Helvetica", 12), justify=CENTER)
        self.calender = Calendar(root, selectmode='day', year=time_now.year, month=time_now.month, day=time_now.day)
        timer = Frame(root)
        submit = Frame(root)
        hours_lbl = Label(timer, text="Hours", font=("Helvetica", 12), justify=CENTER)
        minutes_lbl = Label(timer, text="Minutes", font=("Helvetica", 12), justify=CENTER)
        hours_ent = Spinbox(timer, values= HOURS, wrap=True, justify=CENTER, font=("Comicsans", 18), width=9)
        minutes_ent = Spinbox(timer, values= MINUTES, wrap=True, justify=CENTER, font=("Comicsans", 18), width=9)
        submit1 = Button(submit, text="Now", fg="white", bg="black", bd=0, width=7, font="arial 13", cursor="hand2", command=lambda:self.set_current_time(1))
        submit2 = Button(submit, text="Done", fg="white", bg="black", bd=0, width=7, font="arial 13", cursor="hand2", command=lambda:self.set_time(hours_ent.get(), minutes_ent.get()))

        #placing all elements
        calender_lbl.pack()
        self.calender.pack()
        timer.pack()
        submit.pack(pady=3)
        submit1.grid(row=0, column=0, padx=3)
        submit2.grid(row=0, column=1, padx=3)
        hours_lbl.grid(row=0, column=0)
        minutes_lbl.grid(row=0, column=1)
        hours_ent.grid(row=1, column=0)
        minutes_ent.grid(row=1, column=1)
        
        #finishing
        root.protocol("WM_DELETE_WINDOW", lambda: self.common.close_window("picker"))
        root.mainloop()
    
    #sets the time in entry box
    def set_time(self, hour, minute):
        self.common.close_window("picker")
        month, day, year = map(int, self.calender.get_date().split('/'))
        self.intime.set(f"{['0'+str(day) if day<10 else day][0]} {MONTHS[month]}, 20{year}  {hour}:{minute}")
    
    #viewer window (floating) for resources
    def view_selected(self, ev=0):
        #some initials
        viewer = Tk()
        common = Common(viewer)
        if "resources" in windows:
            common.close_window("resources")
        #sets the window
        windows["resources"] = viewer
        viewer.title("Resources")
        viewer.geometry("400x200")
        viewer.resizable(0, 0)
        Label(viewer, text="Double click to delete an item", font="arial 10", fg="blue").pack()
        #creating and placing the scrollbar and listbox
        scroller = Scrollbar(viewer)
        self.tree = ttk.Treeview(viewer, yscrollcommand=scroller.set, column='res', show='headings', selectmode="browse")
        self.tree.column("# 1", anchor=CENTER, width=380)
        self.tree.heading("# 1", text="Resources")
        for x in self.resources_sel:
            self.tree.insert('', 'end', text=x, values=[x])
        scroller.config(command=self.tree.yview)
        self.tree.bind("<Double-1>", self.delete_option)
        self.tree.pack(side=LEFT, fill=Y)
        scroller.pack(side=RIGHT, fill=Y)
        #finishing
        viewer.protocol("WM_DELETE_WINDOW",lambda: common.close_window("resources"))
        viewer.mainloop()
    
    #adds resources to list
    def add_option(self, ev=0):
        value = self.resource.get()
        if value not in self.resources_sel:
            self.resources_sel.append(value)
        self.q2.config(text= f"Resources ({len(self.resources_sel)}) *")
    
    #deletes resources from list
    def delete_option(self, ev=0):
        item_id = ev.widget.focus()
        item = ev.widget.item(item_id)
        data = item['values'][0]
        self.tree.delete(item_id)
        self.resources_sel.remove(data)
        self.q2.config(text= f"Resources ({len(self.resources_sel)}) *")

    #counts the number of characters in purpose
    def check_words(self, ev=0):
        #by default, the text widget has an invisible chracter at the beginning
        if len(self.text.get(1.0, END))>101:
            self.text.delete('end-2c')
        self.counter.config(text=f"{len(self.text.get(1.0, END))-1}/100")

    #submits the form and saves the data if legal
    def submit_form(form):
        #getting all the datas
        member = form.member.get().split(' - ')
        intime = form.intime.get()
        resources = [re.findall(r"\(([^()]*)\)$", x)[0] for x in form.resources_sel]
        purpose = form.text.get(1.0, END)[:-1]
        readings = {}
        for isbn in resources: #probs here
            cursor.execute(f"select reading from resources_library where isbn='{isbn}' and user_id={form.user_id}")
            readings[isbn] = cursor.fetchone()[0]

        #saving the data
        if member[0] and form.resources_sel:
            if msg.askyesno("Shelfmate", "Do you really want to submit?"):
                cursor.execute(f'''insert into checked_members(user_id, member_id, in_time, out_time, books, purpose, name)
                            values({form.user_id}, {member[0]}, "{intime}", "", "{';'.join(resources)+';'}", "{purpose}", "{member[1]}")''')
                connection.commit()
                for isbn in resources:
                    cursor.execute(f"update resources_library set reading={readings[isbn]+1} where isbn='{isbn}' and user_id={form.user_id}")
                    connection.commit()
                msg.showinfo("Shelfmate", "Submitted successfully!")
                form.common.close_all_windows()
                CheckInUser()
        else:
            msg.showwarning("Shelfmate", "Fill all required fields!")

#library function (Checked In Readers)
class CheckedInReaders(Tk):
    def __init__(self):
        super().__init__()
        windows["checked in"] = self
        self.create_screen()
        self.mainloop()
    
    #makes the screen
    def create_screen(root):
        #general configuration
        root.common = Common(root)
        root.common.set_screen()
        root.title("Checked-In Readers")
        root.config(bg="gainsboro")
        #gets the data to be shown
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(f"select * from checked_members where user_id={root.user_id} and out_time=''")
        CHECKED = cursor.fetchall()

        #creating header
        title = Label(root, text="Checked-In Readers", font=("Verdana", 25, "underline"), pady=40, bg="gainsboro")

        #creating, packing and binding the scrollable canvas (mainly copy-pasted)
        BIG_FRAME = Frame(root)
        root.canvas = Canvas(BIG_FRAME, bg="gainsboro")
        root.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        root.scrollbar = Scrollbar(BIG_FRAME, orient=VERTICAL, command=root.canvas.yview)
        root.scrollbar.pack(side=RIGHT, fill=Y)
        root.canvas.configure(yscrollcommand=root.scrollbar.set)
        root.canvas.bind("<Configure>", lambda e: root.canvas.config(scrollregion=root.canvas.bbox(ALL)))
        FRAME = Frame(root.canvas, bg="gainsboro")
        root.canvas.create_window((0, 0), window=FRAME, anchor="nw")
        root.canvas.bind_all("<MouseWheel>", root._on_mousewheel)
        root.bind("<Configure>", root._on_configure)

        #creating each card with for loop
        COLOURS = ("#F1F0E8", "#D8D9DA") #for zebra look of the cards
        root.CARDS = {} #to store all card frames
        for i, x in enumerate(CHECKED):
            #creating all the outline elements
            frame = Frame(FRAME, bg="#445069")
            info0 = Label(frame, text=f"Member - {x[7]} ({x[2]})", font=("Comicsans", 14), width=30, anchor=W)
            info1 = Label(frame, text=f"In Time - {x[3]}", font=("Comicsans", 14), width=30, anchor=W)
            info2 = Label(frame, text=f"Out Time - {x[4]}", font=("Comicsans", 14), width=30, anchor=W)
            info3 = Frame(frame)
            info4 = Frame(frame)
            root.CARDS[x[0]] = frame
            
            #creating the resorces part
            label = Label(info3, text="Resources -", font=("Comicsans", 14), anchor=W, bg=COLOURS[1], width=10)
            label.grid(row=0, column=0)
            table = Frame(info3, bg=COLOURS[1])
            table.grid(row=0, column=1)
            for j, res in enumerate(x[5].split(';')[:-1]):
                try: #in case the book that was being read is deleted from resources_library
                    cursor.execute(f"select title from resources_library where isbn='{res}' and user_id={root.user_id}")
                    name = cursor.fetchone()[0]
                except Exception as e:
                    name = "(BOOK DELETED)"
                    print("[RESOURCE DELETED]", e)
                #showing all the resources using Text widget
                book = Text(table, wrap="word", bg=COLOURS[j%2], width=22, height=2, font=("Arial", 13))
                book.insert(1.0, name)
                book.config(state="disabled")
                book.pack(padx=5)

            #creating the purpose part
            purp_lbl = Label(info4, text="Purpose -", font=("Comicsans", 14), anchor=W, bg=COLOURS[0], width=8)
            purp_lbl.grid(row=0, column=0)
            #showing the purpose using Text widget
            purpose = Text(info4, wrap="word", bg=COLOURS[0], width=22, height=3, font=("Verdana", 12))
            purp = x[6]
            if not purp:
                purp = "(None)"
            purpose.insert(1.0, purp)
            purpose.config(state="disabled")
            purpose.grid(row=0, column=1, padx=5)
            #creating and placing the buttons
            btns = Frame(frame, bg="#445069")
            btn1 = Button(btns, text="Check Out", fg="white", bg="black", activebackground="#111111", bd=0, width=10, font="arial 13", cursor="hand2", command=lambda e=x:root.check_out(e))
            btn2 = Button(btns, text="Delete", fg="white", bg="#B31312", activebackground="#B31312", bd=0, width=7, font="arial 13", cursor="hand2", command=lambda e=x:root.del_record(e))
            btn1.pack(side=LEFT, padx=5)
            btn2.pack(side=RIGHT, padx=5)
            
            #placing all outline elements
            frame.grid(row=i//3, column=i%3, padx=50, pady=20)
            for j in range(5):
                eval(f"info{j}.pack(padx=10, pady=5)")
                #setting the zebra pattern
                eval(f"info{j}.config(bg='{COLOURS[j%2]}')")
            btns.pack(pady=10)

        #packing main elements
        title.pack()
        BIG_FRAME.pack(fill=BOTH, expand=1)
    
    #functioning mousewheel to scroll the canvas (copy-pasted)
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    #properly binding the canvas with scroller (copy-pasted)
    def _on_configure(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scrollbar.pack_forget()
        self.scrollbar.pack(side=RIGHT, fill=Y)

    #checks out a member
    def check_out(self, data):
        if msg.askyesno("Confirm", "Are you sure to check out this member?"):
            #locates the card
            widgets = self.CARDS[data[0]].winfo_children()
            #displays the time in card
            now = self.common.get_time()
            widgets[2].config(text=f"Out Time - {now}")
            widgets[5].winfo_children()[0].destroy()
            #updates the value in database
            cursor.execute(f"update checked_members set out_time='{now}' where id={data[0]}")
            connection.commit()
            self.update_book_read(data)
    
    #deletes a record
    def del_record(self, data):
        if msg.askyesno("Confirm", "Are you sure to delete this record?"):
            #locates the card
            frame = self.CARDS[data[0]]
            #displays (Deleted) message on card
            for x in frame.winfo_children():
                x.destroy()
            Label(frame, text="(Deleted)", font="comicsans 30", bg="#445069", fg="#D25380").pack()
            #deletes the record from database
            cursor.execute(f"delete from checked_members where id={data[0]}")
            connection.commit()
            if not data[4]:
                self.update_book_read(data)
    
    #updates the reading value of resources
    def update_book_read(self, data):
        for x in data[5].split(';')[:-1]:
                cursor.execute(f"select reading from resources_library where user_id={self.user_id} and isbn='{x}'")
                reading = cursor.fetchone()[0]
                cursor.execute(f"update resources_library set reading={reading-1} where user_id={self.user_id} and isbn='{x}'")
                connection.commit()

#library function (Borrow Requests)
class BorrowRequest(Tk):
    def __init__(self):
        super().__init__()
        windows["borrow request"] = self
        self.create_screen()
        self.mainloop()
    
    #makes the screen
    def create_screen(root):
        #general configurations
        root.common = Common(root)
        root.common.set_screen()
        root.title("Borrow Resource")
        root.config(bg="gainsboro")
        #gets user data
        with open(f'{PATH}/../static/Personal/Data/cookie.json') as cookie:
            root.user_id = json.load(cookie)[0]['id']
        cursor.execute(f"select id, name from members_library where user_id={root.user_id}")
        MEMBERS = cursor.fetchall()
        cursor.execute(f"select isbn, title, book_cover, edition, language from resources_library where user_id={root.user_id} and quantity-reading-borrowed>0")
        root.BOOKS = cursor.fetchall()

        #creating the header, frames and button
        title = Label(root, text="Borrow Resource", font=("Verdana", 25, "underline"), pady=20, bg="gainsboro")
        FRAME = Frame(root, bg="white")
        root.frame0 = Frame(FRAME, bg="white")
        root.cover = Label(FRAME)
        submit = Button(FRAME, text="Submit", fg="white", bg="black", activebackground="#111111", activeforeground="white", bd=0, width=7, font="arial 12", cursor="hand2", command=root.submit_form)

        #creating labels and entries
        q0 = Label(root.frame0, text="Member *", font=("Arial", 14), bg="white", padx=50)
        root.member = StringVar()
        a0 = ttk.Combobox(root.frame0, textvariable=root.member, width=20, values=[f"{x[0]} - {x[1]}" for x in MEMBERS], state="readonly", font=("Arial", 15))
        q1 = Label(root.frame0, text="ISBN *", font=("Arial", 14), bg="white", padx=50)
        root.isbn = StringVar()
        a1 = ttk.Combobox(root.frame0, textvariable=root.isbn, width=20, values=[x[0] for x in root.BOOKS], state="readonly", font=("Arial", 15))
        q2 = Label(root.frame0, text="Title *", font=("Arial", 14), bg="white", padx=50)
        root.title = StringVar()
        a2 = ttk.Combobox(root.frame0, textvariable=root.title, width=20, values=[x[1] for x in root.BOOKS], state="readonly", font=("Arial", 15))
        q3 = Label(root.frame0, text="Edition", font=("Arial", 14), bg="white", padx=50)
        root.edition = StringVar()
        a3 = Entry(root.frame0, textvariable=root.edition, font=("Comicsans", 15), width=21, bd=5, relief=FLAT, bg=ENTRY, state="readonly")
        q4 = Label(root.frame0, text="Language", font=("Arial", 14), bg="white", padx=50)
        root.language = StringVar()
        a4 = Entry(root.frame0, textvariable=root.language, font=("Comicsans", 15), width=21, bd=5, relief=FLAT, bg=ENTRY, state="readonly")
        q5 = Label(root.frame0, text="From Date *", font=("Arial", 14), bg="white", padx=50)
        root.fromdate = StringVar()
        a5 = Entry(root.frame0, textvariable=root.fromdate, font=("Comicsans", 15), width=21, bd=5, relief=FLAT, bg=ENTRY, state="readonly")
        q6 = Label(root.frame0, text="To Date *", font=("Arial", 14), bg="white", padx=50)
        root.todate = StringVar()
        a6 = Entry(root.frame0, textvariable=root.todate, font=("Comicsans", 15), width=21, bd=5, relief=FLAT, bg=ENTRY, state="readonly")
        q7 = Label(root.frame0, text="No Of Days", font=("Arial", 14), bg="white", padx=50)
        root.days = StringVar()
        a7 = Entry(root.frame0, textvariable=root.days, font=("Comicsans", 15), width=21, bd=5, relief=FLAT, bg=ENTRY, state="readonly")

        #placing the labels and entries
        for i in range(8):
            eval(f"q{i}.grid(row={i}, column=0, padx=30, pady=10, sticky=W)")
            eval(f"a{i}.grid(row={i}, column=1, padx=30, pady=10, sticky=W)")
        
        #placing the header, frames and button
        title.pack()
        FRAME.pack(fill=BOTH, padx=100, pady=50)
        root.frame0.pack(padx=40, pady=30)
        submit.pack(side=BOTTOM, pady=40)

        #binding some widgets
        root.POSITIONS = [root.fromdate, root.todate]
        a1.bind("<<ComboboxSelected>>", lambda ev: root.toggle_combo(ev, 0))
        a2.bind("<<ComboboxSelected>>", lambda ev: root.toggle_combo(ev, 1))
        a5.bind("<Button-1>", lambda ev: root.pick_date(ev, 0))
        a6.bind("<Button-1>", lambda ev: root.pick_date(ev, 1))
        root.protocol("WM_DELETE_WINDOW",lambda: root.common.close_window("borrow request"))

    #loads the book covers in separate thread from external website
    def load_covers(self, _url):
        try:
            #adjusting the onscreen positions when image is shown
            self.frame0.pack_forget()
            self.frame0.pack(side=LEFT, padx=40, pady=30)
            self.cover.pack(side=RIGHT, padx=100, pady=30)
            #showing the image
            SIZE = (300, 400)
            _cover = Image.open(f"{PATH}/../static/Personal/Images/display/book_cover.png")
            _cover = _cover.resize(SIZE)
            cover = ImageTk.PhotoImage(_cover)
            self.cover.config(image=cover)
            self.cover.image = cover
            if not _url.startswith('../static'):
                cover = ImageTk.PhotoImage(Image.open(BytesIO(requests.get(_url).content)).resize(SIZE))
            self.cover.config(image=cover)
            self.cover.image = cover
        except Exception as e:
            print("[WINDOW DESTROYED]", e)
    
    #automatically sets all book values
    def toggle_combo(self, ev, position):
        POSITIONS = [(self.isbn, [x[0] for x in self.BOOKS]), (self.title, [x[1] for x in self.BOOKS])]
        access = POSITIONS[position]
        access_not = POSITIONS[1-position]
        value = access[1].index(access[0].get())
        access_not[0].set(access_not[1][value])
        target = self.BOOKS[value]
        self.edition.set(target[3])
        self.language.set(target[4].replace(';', ', ')[:-2])
        #loads image in background without freezing main window (using threads)
        cover_thread = threading.Thread(target=lambda:self.load_covers(target[2]))
        cover_thread.daemon = True #exits automatically without error on closing application
        cover_thread.start()
    
    #sets current date
    def set_current_date(root, pos):
        root.common.close_window("picker")
        root.POSITIONS[pos].set(root.common.get_time()[:-7])
        root.check_date(pos)

    #creates the date picker box
    def pick_date(self, ev, pos):
        #restarts if already opened
        if "picker" in windows:
            self.common.close_window("picker")
        #general configuration
        root = Tk()
        root.title("Date Picker")
        root.resizable(0, 0)
        windows["picker"] = root
        time_now = datetime.now() #current time

        #some constant arrays
        HOURS = [f"0{i}" if i<10 else i for i in range(24)]
        MINUTES = [f"0{i}" if i<10 else i for i in range(60)]

        #creating all elements
        calender_lbl = Label(root, text="Date", font=("Helvetica", 12), justify=CENTER)
        self.calender = Calendar(root, selectmode='day', year=time_now.year, month=time_now.month, day=time_now.day)
        submit = Frame(root)
        submit1 = Button(submit, text="Today", fg="white", bg="black", bd=0, width=7, font="arial 13", cursor="hand2", command=lambda:self.set_current_date(pos))
        submit2 = Button(submit, text="Done", fg="white", bg="black", bd=0, width=7, font="arial 13", cursor="hand2", command=lambda:self.set_date(pos))

        #placing all elements
        calender_lbl.pack()
        self.calender.pack()
        submit.pack(pady=3)
        submit1.grid(row=0, column=0, padx=3)
        submit2.grid(row=0, column=1, padx=3)
        
        #finishing
        root.protocol("WM_DELETE_WINDOW", lambda: self.common.close_window("picker"))
        root.mainloop()
    
    #sets the date in entry box
    def set_date(self, pos):
        self.common.close_window("picker")
        month, day, year = map(int, self.calender.get_date().split('/'))
        self.POSITIONS[pos].set(f"{['0'+str(day) if day<10 else day][0]} {MONTHS[month]}, 20{year}")
        self.check_date(pos)
    
    #checks validity of from and to dates
    def check_date(self, pos):
        TIMES = [0, 0]
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for i in range(2):
            value = self.POSITIONS[i].get()
            if value:
                month = re.findall(r" ([a-zA-Z]*),", value)[0]
                time_str = value.replace(month, str(MONTHS.index(month)))
                time_format = "%d %m, %Y"
                TIMES[i] = datetime.strptime(time_str, time_format)
        if pos: #if value entered for TO
            if TIMES[0]: #if FROM value entered already
                if TIMES[0]>TIMES[1]: #if FROM value is more than TO value
                    msg.showwarning("Bad Time", "Give a valide 'To' date corresponding to 'From' date!")
                    self.todate.set("")
                    self.days.set("")
                #calculates the number of days
                elif TIMES[0]==TIMES[1]:
                    self.days.set(1)
                else:
                    self.days.set(int(str(TIMES[1]-TIMES[0]).split(' day')[0])+1)
            else: #if no FROM value entered
                msg.showwarning("Too Early", "First enter a valid 'From' date!")
                self.todate.set("")
        else: #if value entered for FROM
            if TIMES[pos]<now:
                msg.showwarning("Bad Time", "Give a valide future date!")
                self.fromdate.set("")
            else:
                self.todate.set("")

    #after submitting the form
    def submit_form(form):
        member = form.member.get()
        isbn = form.isbn.get()
        title = form.title.get()
        fromdate = form.fromdate.get()
        todate = form.todate.get()
        days = form.days.get()

        if member and isbn and fromdate and todate:
            member_id, member_name = member.split(' - ')
            cursor.execute(f"select username from members_library where id='{member_id}'")
            member = cursor.fetchone()[0]
            cursor.execute(f"select quantity from borrow_requests where user_id={form.user_id} and member='{member}' and isbn='{isbn}'")
            try:
                quantity = cursor.fetchone()[0]
            except:
                cursor.execute(f'''insert into borrow_requests(user_id, isbn, member, from_date, to_date, quantity, status, member_name, item, days, renew_date)
                            values({form.user_id}, "{isbn}", "{member}", "{fromdate}", "{todate}", 1, "pending", "{member_name}", "{title}", "{days}", "")''')
            else:
                cursor.execute(f'''update borrow_requests set quantity={quantity+1}, from_date="{fromdate}", to_date="{todate}", status="pending", days={days} where user_id={form.user_id} and member="{member}" and isbn="{isbn}"''')
            connection.commit()
            msg.showinfo("Success", "Borrow requested successfully!")
            form.common.close_all_windows()
            BorrowRequest()
        else:
            msg.showwarning("Shelfmate", "Fill all the required fields!")

#ensures that this block is not called on importing this file (safe coding)
if __name__ == "__main__":
    try:
        open = Opener() #runs the application
        #closes connection with database after app is closed
        cursor.close()
        connection.close()
    except Exception as e:
        #shows error if app crashes unexpectedly in beginning
        print("[APP CLOSED]", e)