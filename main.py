from tkinter import *
from PIL import ImageTk, Image
import database as database
import authentication
import sorter
from tkinter import filedialog, messagebox



#####################################################
# CONNECTION FUNCTIONS                              #
# Serve to connect actions and different GUI frames #
#####################################################

# Connection functions of diary GUIs

def remove_diary(diary, username):
    database.remove_diary(diary, username)
    diaries_window(root, username)


def create_diary(left_frame, frame, entry, username):
    name = entry.get()
    database.create_diary(name, username)
    diaries_window(root,username)


def save_diary(textbox, diary, username):
    text = textbox.get("1.0", 'end-1c')
    database.save_diary(username, diary, text)


def export_diary(textbox):
    text = textbox.get("1.0", 'end-1c')
    path = filedialog.asksaveasfilename(defaultextension='.txt')
    if path is None or path == '':
        return
    file = open(path, 'w')
    print(str(text), file=file)


def toggle_mode(text):
    color = text['bg']
    if color == 'white':
        text.config(fg=left_frame_background, bg='#474745')
    else:
        text.config(fg='black', bg='white')


# Connection functions of authentication GUIs

def login(user_entry, password_entry):
    user = user_entry.get()
    password = password_entry.get()

    if (password is None or password == '') or (user is None or user == ''):
        return

    if authentication.login(user, password):
        diaries_window(root, user)
    else:
        messagebox.showerror('Error','Incorrect password')


def register(user_entry, password_entry, email_entry):
    user = user_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    result = database.register_user(user, password, email)
    if result:
        login(user_entry, password_entry)


def update_password(username, password_entry):
    result = authentication.update_password(username, password_entry)
    print(result)
    if result is True:
        print('enter')
        diaries_window(root, username)
    else:
        print('Error')

#####################################################
# AUTHENTICATION GUIS                               #
# Includes login, signup and account recovery       #
#####################################################


# Function in charge of login frame GUI
def login_frame(frame, leftframe):
    for children in frame.winfo_children():
        children.destroy()

    for i in range(6):
        frame.rowconfigure(index=i, weight=1)
        frame.columnconfigure(index=i, weight=1)

    label_font = ('Consolas', 20, 'bold')

    login_label = Label(frame, text='Login', font=('Constantia', 50, 'bold'), bg='white')
    login_label.grid(row=0, column=3, sticky='w')

    username_label = Label(frame, text='Username: ', font=label_font, bg='white')
    username_label.grid(row=1, column=2, sticky='se')

    username_entry = Entry(frame, font=('Arial', 18, 'bold'))
    username_entry.grid(row=1, column=3, sticky='sw')

    password_label = Label(frame, text='Password: ', font=label_font, bg='white')
    password_label.grid(row=2, column=2, sticky='se')

    password_entry = Entry(frame, font=('Arial', 18, 'bold'), bg='white', show='*')
    password_entry.grid(row=2, column=3, sticky='sw')

    login_button = Button(frame, text='Login', font=('Consolas', 15, 'bold'), bg=left_frame_background,
                          fg='white',
                          width=23, height=2, command=lambda x=username_entry, y=password_entry:login(x,y))
    login_button.grid(row=4, column=3, sticky='sw')

    forgot_button = Button(frame, text='Forgot password?', font=('Consolas', 10, 'bold'),
                           fg=left_frame_background,
                           bg='white', relief=FLAT,
                           activebackground='white',
                           activeforeground=left_frame_background,
                           command=lambda x=frame,y=leftframe: recover_frame_part1(x,y),
                           bd=0)
    forgot_button.grid(row=3, column=3, sticky='nw')

    for children in leftframe.winfo_children():
        if type(children) is Button:
            children.config(text='Sign Up', command=lambda x=frame, y=leftframe: signup_frame(x, y))


def signup_frame(frame, leftframe):
    for children in frame.winfo_children():
        children.destroy()

    label_font = ('Consolas', 20, 'bold')
    entry_font = ('Arial', 18, 'bold')

    sign_label = Label(frame, text='Sign Up', font=('Constantia', 50, 'bold'), bg='white', fg='#03fc13')
    sign_label.grid(row=0, column=3, sticky='w')

    user_label = Label(frame, text='Username: ', font=label_font, bg='white')
    user_label.grid(row=1, column=2, sticky='se')

    user_entry = Entry(frame, font=entry_font)
    user_entry.grid(row=1, column=3, sticky='sw')

    pass_label = Label(frame, text='Password: ', font=label_font, bg='white')
    pass_label.grid(row=2, column=2, sticky='se')

    pass_entry = Entry(frame, font=entry_font, bg='white', show='*')
    pass_entry.grid(row=2, column=3, sticky='sw')

    email_label = Label(frame, text='E-mail: ', font=label_font, bg='white')
    email_label.grid(row=3, column=2, sticky='se')

    email_entry = Entry(frame, font=entry_font, bg='white',)
    email_entry.grid(row=3, column=3, sticky='sw')

    sign_button = Button(frame, text='Create', font=('Consolas', 15, 'bold'), bg=left_frame_background,
                         fg='white', width=23, height=2,
                         command=lambda x=user_entry, y=pass_entry, z=email_entry: register(x, y, z))
    sign_button.grid(row=4, column=3, sticky='sw')

    for children in leftframe.winfo_children():
        if type(children) is Button:
            children.config(text='Log in', command=lambda x=frame,y=leftframe:login_frame(x,y))


# GUIs in charge of account recovery
# Prompts for username input
def recover_frame_part1(frame, leftframe):
    clear_window(frame)
    for i in range(6):
        frame.rowconfigure(index=i, weight=1)
        frame.columnconfigure(index=i, weight=1)

    login_label = Label(frame, text='Recovery', font=('Constantia', 50, 'bold'), bg='white')
    login_label.grid(row=0, column=3, sticky='w')

    username_label = Label(frame, text='Username: ', font=('Consolas', 20, 'bold'), bg='white')
    username_label.grid(row=1, column=2, sticky='se')

    username_entry = Entry(frame, font=('Arial', 18, 'bold'))
    username_entry.grid(row=1, column=3, sticky='sw')

    recovery_button = Button(frame, text='Recover', font=('Consolas', 15, 'bold'), bg=left_frame_background,
                          fg='white',
                          width=23, height=2,
                          command=lambda r=frame,l=leftframe,u=username_entry: recover_frame_part2(r, l, u))

    recovery_button.grid(row=3, column=3, sticky='nw')


# Prompts user to enter access code sent by email
def recover_frame_part2(frame,leftframe,user_entry):

    username = user_entry.get()
    if username is None or username == '':
        return

    result = authentication.send_recover_email(username)

    if result is False:
        return

    clear_window(frame)

    for i in range(6):
        frame.rowconfigure(index=i, weight=1)
        frame.columnconfigure(index=i, weight=1)

    login_label = Label(frame, text='Recovery', font=('Constantia', 50, 'bold'), bg='white')
    login_label.grid(row=0, column=3, sticky='w')

    info_label = Label(frame, text='Check your email for the access code', font=('Constantia',13),
                       bg='white')
    info_label.grid(row=1, column=3, sticky='sw')

    code_label = Label(frame, text='Access code: ', font=('Consolas', 20, 'bold'), bg='white')
    code_label.grid(row=2, column=2, sticky='ne')

    code_entry = Entry(frame, font=('Arial', 18, 'bold'))
    code_entry.grid(row=2,column=3,sticky='nw')

    recovery_button = Button(frame, text='Recover', font=('Consolas', 15, 'bold'), bg=left_frame_background,
                             fg='white',
                             width=23, height=2,
                             command=lambda f=frame, l=leftframe, u=username, c=code_entry: change_password(f, l, u, c))
    recovery_button.grid(row=3, column=3, sticky='nw')


def change_password(frame,left_frame,user,code_entry):

    if not authentication.verify_access_code(user, code_entry):
        return

    clear_window(frame)

    for i in range(6):
        frame.rowconfigure(index=i, weight=1)
        frame.columnconfigure(index=i, weight=1)

    recovery_label = Label(frame, text='Recovery', font=('Constantia', 50, 'bold'), bg='white')
    recovery_label.grid(row=0, column=3, sticky='w')

    pass_label = Label(frame, text='New password: ', font=('Consolas', 20, 'bold'), bg='white')
    pass_label.grid(row=2, column=2, sticky='ne')

    pass_entry = Entry(frame, font=('Arial', 18, 'bold'))
    pass_entry.grid(row=2, column=3, sticky='nw')

    recovery_button = Button(frame, text='Update', font=('Consolas', 15, 'bold'), bg=left_frame_background,
                             fg='white',
                             width=23, height=2,
                             command=lambda u=user, e=pass_entry: update_password(u, e))
    recovery_button.grid(row=3, column=3, sticky='nw')


#####################################################
# DIARY GUIS                                        #
# Includes diary menu and editors                   #
#####################################################


def open_diary(left_frame,right_frame,diary,username,content):
    clear_window(left_frame)
    clear_window(right_frame)

    root.title('Editing '+diary+" "+username)
    edit_label = Label(left_frame, text=diary,bg=left_frame_background,fg='white',
                       font=('Consolas', 40, 'bold'))
    edit_label.grid(row=0, column=0)
    parsed_content = content.replace('{end_line}', '\n')
    textbox = Text(right_frame, width=80, height=40, font=('Times News Roman', 14),bg='white')
    textbox.grid(row=3, column=3)
    textbox.insert(INSERT, parsed_content)

    button_width = 20
    button_relief = FLAT
    button_font = ('Consolas', 20, 'bold')

    save_button = Button(left_frame, text='Save changes', font=button_font, width=button_width,
                         relief=button_relief,
                         command=lambda t=textbox,d=diary,u=username: save_diary(t, d, u))
    save_button.grid(row=1, column=0)

    exit_button = Button(left_frame, text='Exit',font=button_font, width=button_width,
                         relief=button_relief,
                         command=lambda u=username: diaries_window(root, u))
    exit_button.grid(row=2, column=0)

    delete_button = Button(left_frame,text='Remove',font=button_font, width=button_width,
                           relief=button_relief,
                          command=lambda d=diary, u=username: remove_diary(d, u))
    delete_button.grid(row=4, column=0)

    toggle_button = Button(left_frame, text='Switch mode', font=button_font, width=button_width,
                           relief=button_relief,
                           command=lambda t=textbox: toggle_mode(t))
    toggle_button.grid(row=3, column=0)

    export_button = Button(left_frame, text='Export', font=button_font, width=button_width,
                           relief=button_relief, command=lambda t=textbox: export_diary(t))
    export_button.grid(row=5, column=0)


def get_diaries_positions(size):

    #       SCHEMA
    # [1,1] [1,3] [1,5]
    # [3,1] [3,3] [3,5]
    # [5,1] [5,3] [5,5]
    # <-            ->

    if size == 1:
        return [[3, 3]]
    elif size == 2:
        return [3, 1], [3, 5]
    elif size == 3:
        return [3, 1], [3, 3], [3, 5]
    elif size == 4:
        return [1, 1], [1, 5], [5, 1], [5, 5]
    elif size == 5:
        return [1, 1], [1, 5], [3, 3], [5, 1], [5, 5]
    elif size == 6:
        return [1, 1], [1, 3], [1, 5], [5, 1], [5,3], [5, 5]
    elif size == 7:
        return [1, 1], [1, 3], [1, 5], [3, 3], [5, 1], [5, 3], [5, 5]
    elif size == 8:
        return [1, 1], [1, 3], [1, 5], [3, 1], [3, 5], [5, 1], [5, 3], [5, 5]
    else:
        return [1, 1], [1, 3], [1, 5], [3, 1], [3, 3], [3, 5], [5, 1], [5, 3], [5, 5]


def clear_window(window):
    for children in window.winfo_children():
        children.destroy()


def diaries_window(window, username):
    window.title('MyDiary | '+username)
    # Clear previous widgets in window
    for children in window.winfo_children():
        children.destroy()

    window.deiconify()

    window.rowconfigure(index=0, weight=1)
    window.columnconfigure(index=0, weight=1)
    window.columnconfigure(index=1,weight=1)

    menu_frame = Frame(window,bg=left_frame_background)
    menu_frame.grid(row=0,column=0, sticky='NSEW')

    for i in range(6):
        menu_frame.rowconfigure(index=i, weight=1)

    menu_frame.columnconfigure(index=0, weight=1)
    menu_frame.columnconfigure(index=1, weight=1)

    diaries_frame = Frame(window, bg='gray')
    diaries_frame.grid(row=0, column=1, columnspan=2, sticky='NSEW')
    build_diaries_frame(menu_frame, diaries_frame, username, 0)

    welcome_label = Label(menu_frame,text='Welcome back, {}!'.format(username),
                          bg=left_frame_background, fg='white', font=('Verdana', 25, 'bold'))
    welcome_label.grid(row=0,column=0,pady=5)

    button_font = ('Arial', 25, 'bold')
    button_relief = FLAT

    new_diary_button = Button(menu_frame, text='New Diary', width=10, font=button_font, relief=button_relief,
                              command=lambda x=diaries_frame, y=username: diary_maker_frame(menu_frame, x, y))
    new_diary_button.grid(row=1, column=0, sticky='NSEW', pady=10)

    diaries_button = Button(menu_frame, text='Diaries', width=10, font=button_font, relief=button_relief,
                            command=lambda d=diaries_frame, y=username: build_diaries_frame(menu_frame, d, y, 0))
    diaries_button.grid(row=2, column=0, sticky='NSEW', pady=10)

    logout_button = Button(menu_frame, text='Logout', command=main_window, width=10, font=button_font,
                           relief=button_relief)
    logout_button.grid(row=3, column=0, sticky='NSEW', pady=10)

    sort_options = ('alphabetical', 'content', 'date')
    sort_selection = OptionMenu(menu_frame, sort_by, *sort_options,
                                command=lambda u=username: diaries_window(window, username))

    print(type(sort_selection))
    sort_selection.grid(row=4, column=0, sticky='NSEW', pady=10)


def diary_maker_frame(left_frame, frame, username):
    clear_window(frame)

    frame.rowconfigure(index=0,weight=1)
    frame.rowconfigure(index=1,weight=1)
    frame.rowconfigure(index=2, weight=1)
    frame.columnconfigure(index=0,weight=1)

    name_label= Label(frame, text='Give it a name ', bg='gray',fg='white',font=('Constantia',40,'bold'))
    name_label.grid(row=0, column=0, sticky='s', padx=5)

    name_entry = Entry(frame, bg='white', fg='gray', font=('Arial', 30, 'bold'), justify=CENTER)
    name_entry.grid(row=1, column=0, sticky='n', padx=5)

    create_button = Button(frame, bg=left_frame_background, text='Create'
                           , fg='white', font=('Consolas', 25, 'bold'), width=10,
                           command=lambda x=frame, y=name_entry, z=username: create_diary(left_frame,x, y, z))
    create_button.grid(row=2, column=0, sticky='NSEW', pady=270, padx=350)


def build_diaries_frame(left_frame, frame,username,page):

    print(frame)

    clear_window(frame)

    diaries = database.get_user_diaries(username)
    if diaries is None:
        frame.rowconfigure(index=0,weight=1)
        frame.columnconfigure(index=0,weight=1)
        Label(frame,text='It is pretty empty here!',font=('Constantia',40,'bold'),bg='gray',fg='white')\
            .grid(row=0,column=0,sticky='NSEW')
    else:
        if len(diaries) == 0:
            frame.rowconfigure(index=0, weight=1)
            frame.columnconfigure(index=0, weight=1)
            Label(frame, text='It is pretty empty here!', font=('Constantia', 40, 'bold'), bg='gray', fg='white') \
                .grid(row=0, column=0, sticky='NSEW')
            return

        diaries = (sorter.bubble_sort(diaries, sort_by.get()))
        diaries = diaries[page*9:]
        length = len(diaries)
        positions = get_diaries_positions(length)
        for i in range(7):
            frame.rowconfigure(index=i, weight=1)
            frame.columnconfigure(index=i, weight=1)

        index = 0
        for pos in positions:
            row = pos[0]
            column = pos[1]
            name = (diaries[index])[0]
            date = (diaries[index])[3]
            contents =(diaries[index])[2]
            Button(frame,text=name,font=('Consolas',20,'bold'),width=20,relief=FLAT,
            command=lambda lf=left_frame, rf=frame, n=name, u=username, con=contents
                   : open_diary(lf, rf, n, u, con), bg=left_frame_background, fg='white',
                   activebackground=left_frame_background,activeforeground='white')\
            .grid(row=row,column=column,sticky='NSEW')
            Label(frame,text='Created on '+date,font=('Consolas', 14), bg=left_frame_background,
                  fg='white')\
            .grid(row=row,column=column,sticky='s')

            index += 1

            if page > 0:
                Button(frame, image=left_arrow,
                       command=lambda l=left_frame, r=frame, u=username, p=page - 1:
                       build_diaries_frame(l, r, u, p),
                       relief=FLAT, highlightcolor="gray", bg="gray",
                       activebackground="gray", bd=0).grid(row=6, column=1, sticky="NSEW")

            if length > 9:
                Button(frame, image=right_arrow,
                       command=lambda l=left_frame, r=frame, u=username, p=page + 1:
                       build_diaries_frame(l, r, u, p),
                       relief=FLAT, highlightcolor="gray", bg="gray",
                       activebackground="gray", bd=0).grid(row=6, column=5, sticky="NSEW")


def clear_window(window):
    for children in window.winfo_children():
        children.destroy()


database.init()
root = Tk()
root.title('MyDiary')



logo = Image.open('assets/book_icon.png')
logo = logo.resize((80, 80), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)

left_arrow = Image.open('assets/arrow_left.png')
left_arrow = left_arrow.resize((90, 70), Image.ANTIALIAS)
left_arrow = ImageTk.PhotoImage(left_arrow)

right_arrow = Image.open('assets/arrow_right.png')
right_arrow = right_arrow.resize((90, 70), Image.ANTIALIAS)
right_arrow = ImageTk.PhotoImage(right_arrow)

sort_by = StringVar()


left_frame_background = '#03fc13'



def main_window():
    sort_by.set('date')
    root.title('MyDiary | Login Page')
    clear_window(root)
    root.rowconfigure(index=0, weight=1)
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=1)
    left_frame = Frame(root, bg=left_frame_background)
    left_frame.grid(row=0, column=0, sticky="NSEW")

    left_frame.rowconfigure(index=0, weight=1)
    left_frame.columnconfigure(index=0, weight=1)
    left_frame.rowconfigure(index=1, weight=1)
    left_frame.rowconfigure(index=2, weight=1)

    title_label = Label(left_frame, text="MyDiary", bg=left_frame_background, fg='white',
                        font=('Consolas', 40, 'bold'), image=logo, compound=BOTTOM)
    title_label.grid(row=0, column=0, sticky='s')

    description_label = Label(left_frame, text="Keeping your secrets safe", bg=left_frame_background,
                              fg='white', font=('Consolas', 20, 'bold'))
    description_label.grid(row=1, column=0, sticky='n')

    right_frame = Frame(root, bg='white')
    right_frame.grid(row=0, column=1, columnspan=2, sticky='NSEW')

    signup_button = Button(left_frame, text='Sign Up', font=('Constantia', 15, 'bold'), bg='white',
                           command=lambda x=right_frame, y=left_frame: signup_frame(x, y), relief=FLAT,
                           width=23, height=2)
    signup_button.grid(row=2, column=0, sticky='n')

    login_frame(right_frame, left_frame)



main_window()
root.mainloop()




