import tkinter
from tkinter import *
from tkinter import Toplevel, messagebox, filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
import sqlite3
import time

def create_main_window():
    root = Tk()
    root.title("Human Resource Management System")
    root.config(bg="light blue")
    root.geometry("1100x700+200+50")
    root.resizable(False, False)

    def table_exists(cursor, table_name):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return cursor.fetchone() is not None

    conn = sqlite3.connect('HumanResourceManagementSystem.db')
    cursor = conn.cursor()
    table_name = 'employeedata1'

    if not table_exists(cursor, table_name):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employeedata1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                mobile TEXT,
                email TEXT,
                address TEXT,
                gender TEXT,
                salary TEXT,
                date TEXT,
                time TEXT
            )
        ''')

        conn.commit()
        
    def addemployee():
        def submitadd():
            id = idval.get()
            name = nameval.get()
            mobile = mobileval.get()
            email = emailval.get()
            address = addressval.get()
            gender = genderval.get()
            salary = salaryval.get()
            addedtime = time.strftime("%H:%M:%S") #to get time
            addeddate = time.strftime("%d/%m/%Y") #to get date
            try:
                conn = sqlite3.connect('HumanResourceManagementSystem.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO employeedata1 (name, mobile, email, address, gender, salary, date, time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, mobile, email, address, gender, salary, addeddate, addedtime))
                conn.commit()
                conn.close()
                res = messagebox.askyesnocancel('Notificatrions','Name {} Added sucessfully.. and want to clean the form'.format(name),
                                                parent=addroot)
                
                if (res == True):
                    nameval.set('')
                    mobileval.set('')
                    emailval.set('')
                    addressval.set('')
                    genderval.set('')
                    salaryval.set('')
            except:
                messagebox.showerror('Notifications', 'Error occurred while adding data', parent=addroot)
            
            showallrecords()
        
        addroot = Toplevel(master=DataEntryFrame)
        addroot.grab_set()
        addroot.geometry('470x540+220+200')
        addroot.title('Add Employee')
        addroot.config(bg='light blue')
        addroot.resizable(False, False) #making window nonresizable
        
        id_label = Label(addroot, text="ID:", font=("verdana", 12, "bold"), bg="lavender")
        id_label.place(x=30, y=30)

        idval = StringVar()
        id_entry = Entry(addroot, textvariable=idval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        id_entry.place(x=180, y=30)

        name_label = Label(addroot, text="Name:", font=("verdana", 12, "bold"), bg="lavender")
        name_label.place(x=30, y=30)

        nameval = StringVar()
        name_entry = Entry(addroot, textvariable=nameval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        name_entry.place(x=180, y=30)

        mobile_label = Label(addroot, text="Mobile:", font=("verdana", 12, "bold"), bg="lavender")
        mobile_label.place(x=30, y=80)

        mobileval = StringVar()
        mobile_entry = Entry(addroot, textvariable=mobileval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        mobile_entry.place(x=180, y=80)

        email_label = Label(addroot, text="Email:", font=("verdana", 12, "bold"), bg="lavender")
        email_label.place(x=30, y=130)

        emailval = StringVar()
        email_entry = Entry(addroot, textvariable=emailval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        email_entry.place(x=180, y=130)

        address_label = Label(addroot, text="Address:", font=("verdana", 12, "bold"), bg="lavender")
        address_label.place(x=30, y=180)

        addressval = StringVar()
        address_entry = Entry(addroot, textvariable=addressval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        address_entry.place(x=180, y=180)

        gender_label = Label(addroot, text="Gender:", font=("verdana", 12, "bold"), bg="lavender")
        gender_label.place(x=30, y=230)

        genderval = StringVar()
        gender_entry = Entry(addroot, textvariable=genderval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        gender_entry.place(x=180, y=230)

        salary_label = Label(addroot, text="Salary:", font=("verdana", 12, "bold"), bg="lavender")
        salary_label.place(x=30, y=280)

        salaryval = StringVar()
        salary_entry = Entry(addroot, textvariable=salaryval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        salary_entry.place(x=180, y=280)

        submit_button = Button(addroot, text="Submit", bd=4, bg="#eb6926", relief="raised", font=("arial", 12, "bold"), command=submitadd)
        submit_button.config(activebackground="red", activeforeground="white")
        submit_button.place(x=180, y=330)

        addroot.mainloop()

    def searchemployee():
        def search():
            id = idval.get()
            name = nameval.get()
            mobile = mobileval.get()
            email = emailval.get()
            address = addressval.get()
            gender = genderval.get()
            salary = salaryval.get()
            date = dateval.get()
            time = timeval.get()

            conn = sqlite3.connect('HumanResourceManagementSystem.db')
            cursor = conn.cursor()

            query = '''
                SELECT * FROM employeedata1 
                WHERE (name LIKE ? OR name IS NULL)
                OR (mobile LIKE ? OR mobile IS NULL)
                OR (email LIKE ? OR email IS NULL)
                OR (address LIKE ? OR address IS NULL)
                OR (gender LIKE ? OR gender IS NULL)
                OR (salary LIKE ? OR salary IS NULL)
                OR (date LIKE ? OR date IS NULL)
                OR (time LIKE ? OR time IS NULL)
            '''

            # Ensure that non-empty and non-None values are used in the query
            params = ('%' + name + '%' if name else None,
                    '%' + mobile + '%' if mobile else None,
                    '%' + email + '%' if email else None,
                    '%' + address + '%' if address else None,
                    '%' + gender + '%' if gender else None,
                    '%' + salary + '%' if salary else None,
                    '%' + date + '%' if date else None,
                    '%' + time + '%' if time else None)

            cursor.execute(query, params)
            data = cursor.fetchall()
            conn.close()


            employeetable.delete(*employeetable.get_children())
            for i in data:
                employeetable.insert('', END, values=i)

        searchroot = Toplevel(master=DataEntryFrame)
        searchroot.grab_set()
        searchroot.geometry('470x540+220+200')
        searchroot.title('Search Records')
        searchroot.config(bg='light blue')
        searchroot.resizable(True, False)
        
        id_label = Label(searchroot, text="ID:", font=("verdana", 12, "bold"), bg="lavender")
        id_label.place(x=30, y=30)

        idval = StringVar()
        id_entry = Entry(searchroot, textvariable=idval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        id_entry.place(x=180, y=30)  # Corrected the coordinates for ID entry

        name_label = Label(searchroot, text="Name:", font=("verdana", 12, "bold"), bg="lavender")
        name_label.place(x=30, y=30)

        nameval = StringVar()
        name_entry = Entry(searchroot, textvariable=nameval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        name_entry.place(x=180, y=30)

        mobile_label = Label(searchroot, text="Mobile:", font=("verdana", 12, "bold"), bg="lavender")
        mobile_label.place(x=30, y=80)

        mobileval = StringVar()
        mobile_entry = Entry(searchroot, textvariable=mobileval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        mobile_entry.place(x=180, y=80)

        email_label = Label(searchroot, text="Email:", font=("verdana", 12, "bold"), bg="lavender")
        email_label.place(x=30, y=130)

        emailval = StringVar()
        email_entry = Entry(searchroot, textvariable=emailval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        email_entry.place(x=180, y=130)

        address_label = Label(searchroot, text="Address:", font=("verdana", 12, "bold"), bg="lavender")
        address_label.place(x=30, y=180)

        addressval = StringVar()
        address_entry = Entry(searchroot, textvariable=addressval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        address_entry.place(x=180, y=180)

        gender_label = Label(searchroot, text="Gender:", font=("verdana", 12, "bold"), bg="lavender")
        gender_label.place(x=30, y=230)

        genderval = StringVar()
        gender_entry = Entry(searchroot, textvariable=genderval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        gender_entry.place(x=180, y=230)

        salary_label = Label(searchroot, text="Salary:", font=("verdana", 12, "bold"), bg="lavender")
        salary_label.place(x=30, y=280)

        salaryval = StringVar()
        salary_entry = Entry(searchroot, textvariable=salaryval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        salary_entry.place(x=180, y=280)

        date_label = Label(searchroot, text="Date (dd/mm/yyyy):", font=("verdana", 12, "bold"), bg="lavender")
        date_label.place(x=30, y=330)

        dateval = StringVar()
        date_entry = Entry(searchroot, textvariable=dateval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        date_entry.place(x=250, y=330)

        time_label = Label(searchroot, text="Time (hh:mm:ss):", font=("verdana", 12, "bold"), bg="lavender")
        time_label.place(x=30, y=380)

        timeval = StringVar()
        time_entry = Entry(searchroot, textvariable=timeval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        time_entry.place(x=250, y=380)

        search_button = Button(searchroot, text="Search", bd=4, bg="#eb6926", relief="raised", font=("arial", 12, "bold"), command=search)
        search_button.config(activebackground="red", activeforeground="white")
        search_button.place(x=180, y=430)

        searchroot.mainloop()

    def deleteemployee():
        cc = employeetable.focus()         #focus on the record which we click and gets data of that record
        content = employeetable.item(cc)
        pp = content['values'][0]          #it gives the id of the particular record to delete 
        conn = sqlite3.connect('HumanResourceManagementSystem.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employeedata1 WHERE id = ?', (pp,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Notifications', 'Id {} deleted successfully...'.format(pp))
        showallrecords()

    def updateemployee():
        def update():
            id = idval.get()
            name = nameval.get()
            mobile = mobileval.get()
            email = emailval.get()
            address = addressval.get()
            gender = genderval.get()
            salary = salaryval.get()
            date = dateval.get()
            time = timeval.get()

            conn = sqlite3.connect('HumanResourceManagementSystem.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE employeedata1 SET name=?, mobile=?, email=?, address=?, gender=?, salary=?, date=?, time=?
                WHERE id=?
            ''', (name, mobile, email, address, gender, salary, date, time, id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Notifications', 'Id {} Modified successfully...'.format(id), parent=updateroot)
            showallrecords()
        
        updateroot = Toplevel(master=DataEntryFrame)
        updateroot.grab_set()
        updateroot.geometry('470x585+220+160')
        updateroot.title('Update Record')
        updateroot.config(bg='light blue')
        updateroot.resizable(False, False)
        
        id_label = Label(updateroot, text="ID:", font=("verdana", 12, "bold"), bg="lavender")
        id_label.place(x=30, y=30)

        idval = StringVar()
        id_entry = Entry(updateroot, textvariable=idval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        id_entry.place(x=180, y=30)

        name_label = Label(updateroot, text="Name:", font=("verdana", 12, "bold"), bg="lavender")
        name_label.place(x=30, y=80)

        nameval = StringVar()
        name_entry = Entry(updateroot, textvariable=nameval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        name_entry.place(x=180, y=80)

        mobile_label = Label(updateroot, text="Mobile:", font=("verdana", 12, "bold"), bg="lavender")
        mobile_label.place(x=30, y=130)

        mobileval = StringVar()
        mobile_entry = Entry(updateroot, textvariable=mobileval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        mobile_entry.place(x=180, y=130)

        email_label = Label(updateroot, text="Email:", font=("verdana", 12, "bold"), bg="lavender")
        email_label.place(x=30, y=180)

        emailval = StringVar()
        email_entry = Entry(updateroot, textvariable=emailval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        email_entry.place(x=180, y=180)

        address_label = Label(updateroot, text="Address:", font=("verdana", 12, "bold"), bg="lavender")
        address_label.place(x=30, y=230)

        addressval = StringVar()
        address_entry = Entry(updateroot, textvariable=addressval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        address_entry.place(x=180, y=230)

        gender_label = Label(updateroot, text="Gender:", font=("verdana", 12, "bold"), bg="lavender")
        gender_label.place(x=30, y=280)

        genderval = StringVar()
        gender_entry = Entry(updateroot, textvariable=genderval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        gender_entry.place(x=180, y=280)

        salary_label = Label(updateroot, text="Salary:", font=("verdana", 12, "bold"), bg="lavender")
        salary_label.place(x=30, y=330)

        salaryval = StringVar()
        salary_entry = Entry(updateroot, textvariable=salaryval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        salary_entry.place(x=180, y=330)

        date_label = Label(updateroot, text="Date (dd/mm/yyyy):", font=("verdana", 12, "bold"), bg="lavender")
        date_label.place(x=30, y=380)

        dateval = StringVar()
        date_entry = Entry(updateroot, textvariable=dateval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        date_entry.place(x=250, y=380)

        time_label = Label(updateroot, text="Time (hh:mm:ss):", font=("verdana", 12, "bold"), bg="lavender")
        time_label.place(x=30, y=430)

        timeval = StringVar()
        time_entry = Entry(updateroot, textvariable=timeval, bd=4, bg="white", relief="raised", font=("verdana", 12))
        time_entry.place(x=250, y=430)

        update_button = Button(updateroot, text="Update", bd=4, bg="#eb6926", relief="raised", font=("arial", 12, "bold"), command=update)
        update_button.config(activebackground="red", activeforeground="white")
        update_button.place(x=180, y=480)

        cc = employeetable.focus()      #this will get all details of existing record when clicked on it and fills in update entryform
        content = employeetable.item(cc)
        pp = content['values']
        if (len(pp) != 0):
            idval.set(pp[0])
            nameval.set(pp[1])
            mobileval.set(pp[2])
            emailval.set(pp[3])
            addressval.set(pp[4])
            genderval.set(pp[5])
            salaryval.set(pp[6])
            dateval.set(pp[7])
            timeval.set(pp[8])

        updateroot.mainloop()

    def showallrecords():
        
        conn = sqlite3.connect('HumanResourceManagementSystem.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employeedata1')
        data = cursor.fetchall()
        conn.close()
        
        employeetable.delete(*employeetable.get_children())
        for i in data:
            employeetable.insert('', END, values=i)

    def exit_window():
        res = messagebox.askyesnocancel('Notification', 'Do you want to exit?')
        if (res == True):
            root.destroy()

    def tick():
        time_string = time.strftime("%H:%M:%S")
        date_string = time.strftime("%d/%m/%Y")
        clock.config(text='Date :' + date_string + "\n" + "Time : " + time_string)
        clock.after(200, tick)

    DataEntryFrame = Frame(root, bg="#eb6926", bd=1, relief="groove")
    DataEntryFrame.place(x=20, y=80, width=500, height=600)

    frontlabel = Label(DataEntryFrame, text="Data Management Functions", relief="groove", bg="#b7b1fc", fg="navy blue",
                    font=("arial", 20, "bold"))
    frontlabel.pack(side="top", fill=BOTH)

    addbtn = Button(DataEntryFrame, text="Add Employee", relief="raised", bg="light blue", font=("verdana", 14, "bold"),
                    width=20, command=addemployee)
    addbtn.place(x=118, y=100)

    updatebtn = Button(DataEntryFrame, text="Update Record", relief="raised", bg="light blue", font=("verdana", 14, "bold"),
                    width=20, command=updateemployee)
    updatebtn.place(x=118, y=180)

    searchbtn = Button(DataEntryFrame, text="Search Record", relief="raised", bg="light blue", font=("verdana", 14, "bold"),
                    width=20, command=searchemployee)
    searchbtn.place(x=118, y=260)

    delete_button = Button(DataEntryFrame, text="Delete Record", relief="raised", bg="light blue",
                        font=("verdana", 14, "bold"), width=20, command=deleteemployee)
    delete_button.place(x=118, y=340)

    showall_button = Button(DataEntryFrame, text="Show All Records", relief="raised", bg="light blue",
                            font=("verdana", 14, "bold"), width=20, command=showallrecords)
    showall_button.place(x=118, y=420)

    exit_button = Button(DataEntryFrame, text="Exit", relief="raised", bg="light blue", font=("verdana", 14, "bold"),
                        width=20, command=exit_window)
    exit_button.place(x=118, y=500)

    ShowDataFrame = Frame(root, bg='Lavender', relief=GROOVE, borderwidth=5)
    ShowDataFrame.place(x=580, y=80, width=500, height=600)

    style = ttk.Style()
    style.configure('Treeview.Heading', font=('verdana', 12, 'bold'), foreground='navy blue')
    style.configure('Treeview', font=('Helvetica', 11, 'bold'), foreground='black', background='lavender')
    scroll_x = Scrollbar(ShowDataFrame, orient=HORIZONTAL)
    scroll_y = Scrollbar(ShowDataFrame, orient=VERTICAL)
    employeetable = Treeview(ShowDataFrame, columns=('Id', 'Name', 'Mobile No', 'Email', 'Address', 'Gender', 'Salary', 'Added Date', 'Added Time'),
                            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=employeetable.xview)
    scroll_y.config(command=employeetable.yview)
    employeetable.heading('Id', text='Id')
    employeetable.heading('Name', text='Name')
    employeetable.heading('Mobile No', text='Mobile No')
    employeetable.heading('Email', text='Email')
    employeetable.heading('Address', text='Address')
    employeetable.heading('Gender', text='Gender')
    employeetable.heading('Salary', text='Salary')
    employeetable.heading('Added Date', text='Added Date')
    employeetable.heading('Added Time', text='Added Time')
    employeetable['show'] = 'headings'
    employeetable.column('Id', width=100)
    employeetable.column('Name', width=200)
    employeetable.column('Mobile No', width=200)
    employeetable.column('Email', width=300)
    employeetable.column('Address', width=200)
    employeetable.column('Gender', width=100)
    employeetable.column('Salary', width=150)
    employeetable.column('Added Date', width=150)
    employeetable.column('Added Time', width=150)
    employeetable.pack(fill=BOTH, expand=1)

    main_label = Label(root, text="Human Resource Management System", relief="groove", bg="#b7b1fc", fg="navy blue",
                    font=("arial", 22, "bold"))
    main_label.pack(side="top")

    clock = Label(root, font=('verdana', 10, 'bold'), relief=RAISED, borderwidth=3, bg='Lavender', fg="black")
    clock.place(x=930, y=5)
    tick()

    root.mainloop()

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == 'admin' and password == 'password':
        login_window.destroy()  # Close the login window
        create_main_window()    # Create the main application window
    else:
        messagebox.showerror('Login Failed', 'Invalid username or password')

login_window = Tk()
login_window.title("Admin Login")
login_window.config(bg="light blue")
login_window.geometry("500x300")
login_window.resizable(False, False)

username_label = Label(login_window, text="Username:")
username_label.pack(pady=20)
username_entry = Entry(login_window)
username_entry.pack()

password_label = Label(login_window, text="Password:")
password_label.pack(pady=20)
password_entry = Entry(login_window, show="*")  # Use show="*" to hide the password
password_entry.pack()

login_button = Button(login_window, text="Login", command=login)
login_button.pack(pady=30)

login_window.mainloop()