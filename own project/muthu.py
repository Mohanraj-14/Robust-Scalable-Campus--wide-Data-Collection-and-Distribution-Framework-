from tkinter import *
import time
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas
from tkcalendar import DateEntry
import os
from datetime import datetime
from PIL import Image, ImageTk

# Global list to store departments
department_list = [
    'BE(CSE)', 'BE(ECE)', 'BE(EEE)', 'BE(Mechanical)', 'BE(PETRO CHEMICAL)', 
    'BE(CIVIL)', 'B.TECH(Textile Technology)', 'MCA', 'MBA'
]

# Custom styles for the application
def apply_styles():
    style = ttk.Style()
    style.configure('Yellow.TButton', font=('Helvetica', 14, 'bold'), background='#FFCA28', foreground='black', borderwidth=0)
    style.map('Yellow.TButton', background=[('active', '#FFD54F')], foreground=[('active', 'black')])
    
    style.configure('FormYellow.TButton', font=('Helvetica', 14, 'bold'), background='#FFFF00', foreground='black', borderwidth=0)
    style.map('FormYellow.TButton', background=[('active', '#FFFF99')], foreground=[('active', 'black')])
    
    style.configure('Custom.Treeview', font=('Helvetica', 14), rowheight=40, background='skyblue', foreground='black', fieldbackground='#87CEEB')
    style.configure('Custom.Treeview.Heading', font=('Helvetica', 16, 'bold'), background='#0288D1', foreground='red')
    style.map('Custom.Treeview', background=[('selected', 'skyblue')])
    
    style.configure('Custom.TCombobox', font=('Helvetica', 14), background='#FFFF00', fieldbackground='#FFFF00', foreground='black')
    style.map('Custom.TCombobox', fieldbackground=[('readonly', '#FFFF00')], selectbackground=[('readonly', '#FFFF00')], selectforeground=[('readonly', 'black')])

# Function to set background image for windows
def set_background(window, image_path='college_background.jpg'):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file {image_path} not found")
        img = Image.open(image_path)
        img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        bg_label = Label(window, image=photo)
        bg_label.image = photo  # Keep reference
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Failed to load window background image: {e}")
        window.configure(bg='#E0F7FA')  # Fallback color

# Toggle full-screen mode
def toggle_fullscreen(event=None, window=None):
    if window is None:
        window = root
    window.is_fullscreen = not getattr(window, 'is_fullscreen', False)
    window.attributes('-fullscreen', window.is_fullscreen)

# Exit full-screen mode
def exit_fullscreen(event=None, window=None):
    if window is None:
        window = root
    window.is_fullscreen = False
    window.attributes('-fullscreen', False)

def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?', icon='question')
    if result:
        root.destroy()

def download_pdf():
    indexing = participantTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a participant to download their PDF!', icon='error')
        return
    
    content = participantTable.item(indexing)
    content_id = content['values'][0]
    
    try:
        query = 'SELECT pdf_file FROM participant WHERE register_no=%s'
        mycursor.execute(query, (content_id,))
        pdf_data = mycursor.fetchone()
        
        if not pdf_data or not pdf_data['pdf_file']:
            messagebox.showerror('Error', 'No PDF file found for this participant!', icon='error')
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])
        if file_path:
            with open(file_path, 'wb') as file:
                file.write(pdf_data['pdf_file'])
            messagebox.showinfo('Success', 'PDF downloaded successfully!', icon='info')
    
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database error: {str(e)}', icon='error')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to download PDF: {str(e)}', icon='error')

def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = participantTable.get_children()
    newlist = []
    for index in indexing:
        content = participantTable.item(index)
        datalist = content['values']
        newlist.append(datalist)
    table = pandas.DataFrame(newlist, columns=['Register_no', 'Name', 'Department', 'Event_Name', 'From_Date', 'To_Date', 'Event_Location', 'Mobile_no', 'Email', 'Address', 'Gender', 'Added_Date', 'Added_Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully', icon='info')

def update_department():
    def add_department():
        dept_name = dept_entry.get().strip()
        if not dept_name:
            messagebox.showerror('Error', 'Department name cannot be empty!', parent=update_dept_window, icon='error')
            return
        if dept_name in department_list:
            messagebox.showerror('Error', 'Department already exists!', parent=update_dept_window, icon='error')
            return
        department_list.append(dept_name)
        dept_entry.delete(0, END)
        messagebox.showinfo('Success', f'Department {dept_name} added successfully!', parent=update_dept_window, icon='info')
        delete_dept_combobox['values'] = department_list

    def delete_department():
        dept_name = delete_dept_combobox.get()
        if not dept_name:
            messagebox.showerror('Error', 'Please select a department to delete!', parent=update_dept_window, icon='error')
            return
        query = 'SELECT COUNT(*) FROM participant WHERE department=%s'
        mycursor.execute(query, (dept_name,))
        count = mycursor.fetchone()['COUNT(*)']
        if count > 0:
            messagebox.showerror('Error', f'Cannot delete {dept_name}. It is assigned to {count} participant(s)!', parent=update_dept_window, icon='error')
            return
        department_list.remove(dept_name)
        delete_dept_combobox.set('')
        delete_dept_combobox['values'] = department_list
        messagebox.showinfo('Success', f'Department {dept_name} deleted successfully!', parent=update_dept_window, icon='info')

    update_dept_window = Toplevel()
    update_dept_window.title('Update Department')
    update_dept_window.grab_set()
    update_dept_window.state('zoomed')
    set_background(update_dept_window)

    update_dept_window.is_fullscreen = False
    update_dept_window.bind('<F11>', lambda event: toggle_fullscreen(event, update_dept_window))
    update_dept_window.bind('<Escape>', lambda event: exit_fullscreen(event, update_dept_window))

    form_frame = Frame(update_dept_window, bg='green')
    form_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    add_label = Label(form_frame, text='Add Department', font=('Helvetica', 20, 'bold'), fg='black')
    add_label.pack(pady=20)

    dept_entry = Entry(form_frame, font=('Helvetica', 16), width=30, bg='white', fg='black', bd=2, relief=FLAT)
    dept_entry.pack(pady=20)

    add_button = ttk.Button(form_frame, text='Add Department', style='FormYellow.TButton', command=add_department)
    add_button.pack(pady=20)

    delete_frame = Frame(form_frame, bg='red')
    delete_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    delete_label = Label(delete_frame, text='Delete Department', font=('Helvetica', 20, 'bold'), bg='white', fg='black')
    delete_label.pack(pady=20)

    delete_dept_combobox = ttk.Combobox(delete_frame, style='Custom.TCombobox', width=28, values=department_list)
    delete_dept_combobox.pack(pady=20)

    delete_button = ttk.Button(delete_frame, text='Delete Department', style='FormYellow.TButton', command=delete_department)
    delete_button.pack(pady=20)

def update_participant():
    def update_data():
        required_fields = [nameEntry.get(), departmentEntry.get(), eventnameEntry.get(), fromdateEntry.get(),
                          todateEntry.get(), eventlocationEntry.get(), addressEntry.get(), genderEntry.get()]
        if not all(required_fields):
            messagebox.showerror('Error', 'All fields except Mobile Number, Email, and PDF are required', parent=update_window, icon='error')
            return
        
        try:
            new_register_no = idEntry.get()
            if not new_register_no:
                messagebox.showerror('Error', 'Register Number is required!', parent=update_window, icon='error')
                return
            try:
                new_register_no = int(new_register_no)
                if new_register_no < 0 or new_register_no > 9999999999999999999999:
                    messagebox.showerror('Error', 'Register Number must be between 0 and 9999999999999999999999!', parent=update_window, icon='error')
                    return
            except ValueError:
                messagebox.showerror('Error', 'Register Number must be an integer!', parent=update_window, icon='error')
                return

            if new_register_no != original_register_no:
                query = 'SELECT COUNT(*) FROM participant WHERE register_no=%s'
                mycursor.execute(query, (new_register_no,))
                count = mycursor.fetchone()['COUNT(*)']
                if count > 0:
                    messagebox.showerror('Error', f'Register Number {new_register_no} already exists!', parent=update_window, icon='error')
                    return

            try:
                from_date = datetime.strptime(fromdateEntry.get(), '%Y-%m-%d').strftime('%Y-%m-%d')
                to_date = datetime.strptime(todateEntry.get(), '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror('Error', 'Invalid date format! Use YYYY-MM-DD.', parent=update_window, icon='error')
                return

            mobile_value = mobileEntry.get().strip() if mobileEntry.get().strip() else None
            event_name_upper = eventnameEntry.get().upper()

            pdf_data = None
            update_pdf = False
            if hasattr(update_window, 'pdf_path') and update_window.pdf_path:
                file_size = os.path.getsize(update_window.pdf_path)
                if file_size > 20 * 1024 * 1024:
                    messagebox.showerror('Error', 'PDF file size exceeds 20 MB limit!', parent=update_window, icon='error')
                    return
                with open(update_window.pdf_path, 'rb') as file:
                    pdf_data = file.read()
                update_pdf = True
            
            if update_pdf:
                query = '''UPDATE participant 
                          SET register_no=%s, name=%s, department=%s, event_name=%s, from_date=%s, to_date=%s, event_location=%s, 
                              mobile_no=%s, email=%s, address=%s, gender=%s, pdf_file=%s 
                          WHERE register_no=%s'''
                params = (
                    new_register_no, nameEntry.get(), departmentEntry.get(), event_name_upper, from_date,
                    to_date, eventlocationEntry.get(), mobile_value, emailEntry.get(),
                    addressEntry.get(), genderEntry.get(), pdf_data, original_register_no
                )
            else:
                query = '''UPDATE participant 
                          SET register_no=%s, name=%s, department=%s, event_name=%s, from_date=%s, to_date=%s, event_location=%s, 
                              mobile_no=%s, email=%s, address=%s, gender=%s 
                          WHERE register_no=%s'''
                params = (
                    new_register_no, nameEntry.get(), departmentEntry.get(), event_name_upper, from_date,
                    to_date, eventlocationEntry.get(), mobile_value, emailEntry.get(),
                    addressEntry.get(), genderEntry.get(), original_register_no
                )

            mycursor.execute(query, params)
            con.commit()
            messagebox.showinfo('Success', f'Register No. {new_register_no} is modified successfully', parent=update_window, icon='info')
            update_window.destroy()
            show_participant()
        except pymysql.IntegrityError as e:
            messagebox.showerror('Error', f'Invalid data or Register Number: {str(e)}', parent=update_window, icon='error')
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Database error: {str(e)}', parent=update_window, icon='error')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to update: {str(e)}', parent=update_window, icon='error')

    def upload_pdf():
        file_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        if file_path:
            file_size = os.path.getsize(file_path)
            if file_size > 20 * 1024 * 1024:
                messagebox.showerror('Error', 'PDF file size exceeds 20 MB limit!', parent=update_window, icon='error')
                return
            update_window.pdf_path = file_path
            pdfLabel.config(text=f'Selected PDF: {os.path.basename(file_path)}', fg='black')

    indexing = participantTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a participant to update!', icon='error')
        return

    content = participantTable.item(indexing)
    listdata = content['values']
    original_register_no = int(listdata[0])

    update_window = Toplevel()
    update_window.title('Update Participant')
    update_window.grab_set()
    update_window.state('zoomed')
    set_background(update_window)

    update_window.is_fullscreen = False
    update_window.bind('<F11>', lambda event: toggle_fullscreen(event, update_window))
    update_window.bind('<Escape>', lambda event: exit_fullscreen(event, update_window))

    form_frame = Frame(update_window, bg='skyblue', bd=2, relief=RIDGE)
    form_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    canvas = Canvas(form_frame, bg='#09F4D1')
    scrollbar = Scrollbar(form_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#09F4D1')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    idLabel = Label(scrollable_frame, text='Register Number', font=('Helvetica', 20, 'bold'), fg='black')
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    idEntry.grid(row=0, column=1, pady=15, padx=20, sticky=EW)

    nameLabel = Label(scrollable_frame, text='Name', font=('Helvetica', 20, 'bold'), fg='black')
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    nameEntry.grid(row=1, column=1, pady=15, padx=20, sticky=EW)

    departmentLabel = Label(scrollable_frame, text='Department', font=('Helvetica', 20, 'bold'), fg='black')
    departmentLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    departmentEntry = ttk.Combobox(scrollable_frame, style='Custom.TCombobox', width=28, values=department_list)
    departmentEntry.grid(row=2, column=1, pady=15, padx=20, sticky=EW)

    eventnameLabel = Label(scrollable_frame, text='Event Name', font=('Helvetica', 20, 'bold'), fg='black')
    eventnameLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    eventnameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    eventnameEntry.grid(row=3, column=1, pady=15, padx=20, sticky=EW)

    fromdateLabel = Label(scrollable_frame, text='From Date', font=('Helvetica', 20, 'bold'), fg='black')
    fromdateLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    fromdateEntry = DateEntry(scrollable_frame, font=('Helvetica', 16), width=28, background='#FFFF00',
                              foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
    fromdateEntry.grid(row=4, column=1, pady=15, padx=20, sticky=EW)

    todateLabel = Label(scrollable_frame, text='To Date', font=('Helvetica', 20, 'bold'), fg='black')
    todateLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    todateEntry = DateEntry(scrollable_frame, font=('Helvetica', 16), width=28, background='#FFFF00',
                            foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
    todateEntry.grid(row=5, column=1, pady=15, padx=20, sticky=EW)

    eventlocationLabel = Label(scrollable_frame, text='Event Location', font=('Helvetica', 20, 'bold'), fg='black')
    eventlocationLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    eventlocationEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    eventlocationEntry.grid(row=6, column=1, pady=15, padx=20, sticky=EW)

    mobileLabel = Label(scrollable_frame, text='Mobile Number (opt)', font=('Helvetica', 20, 'bold'), fg='black')
    mobileLabel.grid(row=7, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    mobileEntry.grid(row=7, column=1, pady=15, padx=20, sticky=EW)

    emailLabel = Label(scrollable_frame, text='Email (opt)', font=('Helvetica', 20, 'bold'), fg='black')
    emailLabel.grid(row=8, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    emailEntry.grid(row=8, column=1, pady=15, padx=20, sticky=EW)

    addressLabel = Label(scrollable_frame, text='Address', font=('Helvetica', 20, 'bold'), fg='black')
    addressLabel.grid(row=9, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    addressEntry.grid(row=9, column=1, pady=15, padx=20, sticky=EW)

    genderLabel = Label(scrollable_frame, text='Gender', font=('Helvetica', 20, 'bold'), fg='black')
    genderLabel.grid(row=10, column=0, padx=30, pady=15, sticky=W)
    genderEntry = ttk.Combobox(scrollable_frame, style='Custom.TCombobox', width=28, values=['Male', 'Female', 'Others'])
    genderEntry.grid(row=10, column=1, pady=15, padx=20, sticky=EW)

    pdfLabel = Label(scrollable_frame, text='Upload PDF (opt)', font=('Helvetica', 20, 'bold'), fg='black')
    pdfLabel.grid(row=11, column=0, padx=30, pady=15, sticky=W)
    pdfButton = ttk.Button(scrollable_frame, text='Upload PDF', style='FormYellow.TButton', command=upload_pdf)
    pdfButton.grid(row=11, column=1, pady=15, padx=20, sticky=EW)

    update_participant_button = ttk.Button(scrollable_frame, text='Update', style='Yellow.TButton', command=update_data)
    update_participant_button.grid(row=12, columnspan=2, pady=30)

    idEntry.insert(0, listdata[0])
    nameEntry.insert(0, listdata[1] or '')
    departmentEntry.set(listdata[2] or '')
    eventnameEntry.insert(0, listdata[3] or '')
    fromdateEntry.delete(0, END)
    fromdateEntry.insert(0, listdata[4] or '')
    todateEntry.delete(0, END)
    todateEntry.insert(0, listdata[5] or '')
    eventlocationEntry.insert(0, listdata[6] or '')
    mobileEntry.insert(0, listdata[7] or '')
    emailEntry.insert(0, listdata[8] or '')
    addressEntry.insert(0, listdata[9] or '')
    genderEntry.set(listdata[10] or '')

def show_participant():
    try:
        query = 'SELECT register_no, name, department, event_name, from_date, to_date, event_location, mobile_no, email, address, gender, date, time FROM participant'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        participantTable.delete(*participantTable.get_children())
        for i, data in enumerate(fetched_data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            values = [data[col] for col in ['register_no', 'name', 'department', 'event_name', 'from_date', 'to_date', 'event_location', 'mobile_no', 'email', 'address', 'gender', 'date', 'time']]
            participantTable.insert('', END, values=values, tags=(tag,))
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database error: {str(e)}', icon='error')

def delete_participant():
    indexing = participantTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a participant to delete!', icon='error')
        return
    content = participantTable.item(indexing)
    content_id = content['values'][0]
    try:
        query = 'DELETE FROM participant WHERE register_no=%s'
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'Register No. {content_id} deleted successfully', icon='info')
        show_participant()
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database error: {str(e)}', icon='error')

def search_participant():
    def search_data():
        conditions = []
        params = []
        
        try:
            # Register Number
            reg_no = idEntry.get().strip()
            if reg_no:
                try:
                    reg_no = int(reg_no)
                    if reg_no < 0 or reg_no > 999999999999999999999999999:
                        messagebox.showerror('Error', 'Register Number must be between 0 and 999999999999999999999999999999!', parent=search_window, icon='error')
                        return
                    conditions.append("register_no=%s")
                    params.append(reg_no)
                except ValueError:
                    messagebox.showerror('Error', 'Register Number must be an integer!', parent=search_window, icon='error')
                    return
                
            
            # Name
            name = nameEntry.get().strip()
            if name:
                conditions.append("name LIKE %s")
                params.append(f"%{name.upper()}%")

            # Department
            department = departmentEntry.get().strip()
            if department:
                conditions.append("department LIKE %s")
                params.append(f"%{department}%")

            # Event Name
            event_name = eventnameEntry.get().strip()
            if event_name:
                conditions.append("event_name LIKE %s")
                params.append(f"%{event_name.upper()}%")

            # Event Location
            event_location = eventlocationEntry.get().strip()
            if event_location:
                conditions.append("event_location LIKE %s")
                params.append(f"%{event_location}%")

            # name=event_name.get().strip()
            # if name:
            #     conditions.append('name LIKE %s')
            #     params.append(f'%{name}')


            # From Date and To Date
            from_date = fromdateEntry.get().strip()
            to_date = todateEntry.get().strip()
            if from_date or to_date:
                try:
                    if from_date:
                        from_date = datetime.strptime(from_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                    if to_date:
                        to_date = datetime.strptime(to_date, '%Y-%m-%d').strftime('%Y-%m-%d')
                    
                    if from_date and to_date:
                        conditions.append("from_date BETWEEN %s AND %s")
                        conditions.append("to_date BETWEEN %s AND %s")
                        params.extend([from_date, to_date, from_date, to_date])
                    elif from_date:
                        conditions.append("from_date >= %s")
                        params.append(from_date)
                    elif to_date:
                        conditions.append("to_date <= %s")
                        params.append(to_date)
                except ValueError:
                    messagebox.showerror('Error', 'Invalid date format! Use YYYY-MM-DD.', parent=search_window, icon='error')
                    return

            if not conditions:
                messagebox.showerror('Error', 'Please enter at least one search criterion!', parent=search_window, icon='error')
                return
            
            query = "SELECT register_no, name, department, event_name, from_date, to_date, event_location, mobile_no, email, address, gender, date, time FROM participant"
            query += " WHERE " + " OR ".join(conditions)
            
            mycursor.execute(query, params)
            fetched_data = mycursor.fetchall()
            participantTable.delete(*participantTable.get_children())
            for i, data in enumerate(fetched_data):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                values = [data[col] for col in ['register_no', 'name', 'department', 'event_name', 'from_date', 'to_date', 'event_location', 'mobile_no', 'email', 'address', 'gender', 'date', 'time']]
                participantTable.insert('', END, values=values, tags=(tag,))
            
            if not fetched_data:
                messagebox.showinfo('No Results', 'No participants found matching the criteria.', parent=search_window, icon='info')
            else:
                messagebox.showinfo('Result','Data is founded inside the table',parent=search_window,icon='info')

        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Database error: {str(e)}', parent=search_window, icon='error')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to search: {str(e)}', parent=search_window, icon='error')

    search_window = Toplevel()
    search_window.title('Search Participant')
    search_window.grab_set()
    search_window.state('zoomed')
    set_background(search_window)

    search_window.is_fullscreen = False
    search_window.bind('<F11>', lambda event: toggle_fullscreen(event, search_window))
    search_window.bind('<Escape>', lambda event: exit_fullscreen(event, search_window))

    form_frame = Frame(search_window, bg="#A61BE6", bd=2, relief=RIDGE)
    form_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    canvas = Canvas(form_frame, bg="#12EBF7")
    scrollbar = Scrollbar(form_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#12EBF7')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    idLabel = Label(scrollable_frame, text='Register Number', font=('Helvetica', 20, 'bold'), fg='black')
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    idEntry.grid(row=0, column=1, pady=15, padx=20, sticky=EW)

    nameLabel = Label(scrollable_frame, text='Name', font=('Helvetica', 20, 'bold'), fg='black')
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    nameEntry.grid(row=1, column=1, pady=15, padx=20, sticky=EW)

    departmentLabel = Label(scrollable_frame, text='Department', font=('Helvetica', 20, 'bold'), fg='black')
    departmentLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    departmentEntry = ttk.Combobox(scrollable_frame, style='Custom.TCombobox', width=28, values=[''] + department_list)
    departmentEntry.grid(row=2, column=1, pady=15, padx=20, sticky=EW)

    eventnameLabel = Label(scrollable_frame, text='Event Name', font=('Helvetica', 20, 'bold'), fg='black')
    eventnameLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    eventnameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    eventnameEntry.grid(row=3, column=1, pady=15, padx=20, sticky=EW)

    fromdateLabel = Label(scrollable_frame, text='From Date', font=('Helvetica', 20, 'bold'), fg='black')
    fromdateLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    fromdateEntry = DateEntry(scrollable_frame, font=('Helvetica', 16), width=28, background='#FFFF00',
                              foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
    fromdateEntry.grid(row=4, column=1, pady=15, padx=20, sticky=EW)

    todateLabel = Label(scrollable_frame, text='To Date', font=('Helvetica', 20, 'bold'), fg='black')
    todateLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    todateEntry = DateEntry(scrollable_frame, font=('Helvetica', 16), width=28, background='#FFFF00',
                            foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
    todateEntry.grid(row=5, column=1, pady=15, padx=20, sticky=EW)

    eventlocationLabel = Label(scrollable_frame, text='Event Location', font=('Helvetica', 20, 'bold'), fg='black')
    eventlocationLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    eventlocationEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    eventlocationEntry.grid(row=6, column=1, pady=15, padx=20, sticky=EW)



  

    search_participant_button = ttk.Button(scrollable_frame, text='Search', style='FormYellow.TButton', command=search_data)
    search_participant_button.grid(row=11, columnspan=2, pady=30)

def add_student():
    def add_data():
        required_fields = [idEntry.get(), nameEntry.get(), departmentEntry.get(), eventnameEntry.get(),
                          fromdateEntry.get(), todateEntry.get(), eventlocationEntry.get(), addressEntry.get(), genderEntry.get()]
        if not all(required_fields):
            messagebox.showerror('Error', 'All fields except Mobile Number, Email, and PDF are required', parent=add_window, icon='error')
            return
        
        try:
            try:
                register_no = int(idEntry.get())
                if register_no < 1 or register_no > 99999999999999999999 or len(str(register_no)) > 20:
                    messagebox.showerror('Error', 'Register Number must be between 1 and 20 digits (max 99999999999999999999)!', parent=add_window, icon='error')
                    return
            except ValueError:
                messagebox.showerror('Error', 'Register Number must be an integer!', parent=add_window, icon='error')
                return

            try:
                from_date = datetime.strptime(fromdateEntry.get(), '%Y-%m-%d').strftime('%Y-%m-%d')
                to_date = datetime.strptime(todateEntry.get(), '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror('Error', 'Invalid date format! Use YYYY-MM-DD.', parent=add_window, icon='error')
                return

            pdf_data = None
            if hasattr(add_window, 'pdf_path') and add_window.pdf_path:
                file_size = os.path.getsize(add_window.pdf_path)
                if file_size > 20 * 1024 * 1024:
                    messagebox.showerror('Error', 'PDF file size exceeds 20 MB limit!', parent=add_window, icon='error')
                    return
                with open(add_window.pdf_path, 'rb') as file:
                    pdf_data = file.read()
                
            query = '''INSERT INTO student (
                    register_no, name, department, event_name, from_date, to_date, event_location, 
                    mobile_no, email, address, gender, pdf_file, date, time
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            current_date = time.strftime('%Y-%m-%d')
            current_time = time.strftime('%H:%M:%S')
            mobile_value = mobileEntry.get().strip() if mobileEntry.get().strip() else None
            email_value = emailEntry.get().strip() if emailEntry.get().strip() else None
            mycursor.execute(query, (
                register_no, nameEntry.get(), departmentEntry.get(), eventnameEntry.get(),
                from_date, to_date, eventlocationEntry.get(), mobile_value,
                email_value, addressEntry.get(), genderEntry.get(), pdf_data, current_date, current_time
            ))
            con.commit()
            messagebox.showinfo('Success', 'Student added successfully!', parent=add_window, icon='info')
            idEntry.delete(0, END)
            nameEntry.delete(0, END)
            departmentEntry.set('')
            eventnameEntry.delete(0, END)
            fromdateEntry.delete(0, END)
            todateEntry.delete(0, END)
            eventlocationEntry.delete(0, END)
            mobileEntry.delete(0, END)
            emailEntry.delete(0, END)
            addressEntry.delete(0, END)
            genderEntry.set('')
            if hasattr(add_window, 'pdf_path'):
                pdfLabel.config(text='Upload PDF (opt)', fg='black')
                del add_window.pdf_path
            show_participant()

        except pymysql.IntegrityError:
            messagebox.showerror('Error', 'Register number already exists!', parent=add_window, icon='error')
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Database Error: {str(e)}', parent=add_window, icon='error')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to add: {str(e)}', parent=add_window, icon='error')

    def upload_pdf():
        file_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        if file_path:
            file_size = os.path.getsize(file_path)
            if file_size > 20 * 1024 * 1024:
                messagebox.showerror('Error', 'PDF file size exceeds 20 MB limit!', parent=add_window, icon='error')
                return
            add_window.pdf_path = file_path
            pdfLabel.config(text=f'Selected PDF: {os.path.basename(file_path)}', fg='black')

    add_window = Toplevel()
    add_window.title('Add Student')
    add_window.grab_set()
    add_window.state('zoomed')
    add_window.configure(bg='#E0F7FA')
    set_background(add_window) 

    add_window.is_fullscreen = False
    add_window.bind('<F11>', lambda event: toggle_fullscreen(event, add_window))
    add_window.bind('<Escape>', lambda event: exit_fullscreen(event, add_window))

    form_frame = Frame(add_window, bg='#FFFF00', bd=2, relief=RIDGE)
    form_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    canvas = Canvas(form_frame, bg="#517AE3")
    scrollbar = Scrollbar(form_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#517AE3")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    idLabel = Label(scrollable_frame, text='Register Number', font=('Helvetica', 20, 'bold'), fg='black')
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    idEntry.grid(row=0, column=1, pady=15, padx=20, sticky=EW)

    nameLabel = Label(scrollable_frame, text='Name', font=('Helvetica', 20, 'bold'), fg='black')
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    nameEntry.grid(row=1, column=1, pady=15, padx=20, sticky=EW)

    departmentLabel = Label(scrollable_frame, text='Department', font=('Helvetica', 20, 'bold'), fg='black')
    departmentLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    departmentEntry = ttk.Combobox(scrollable_frame, style='Custom.TCombobox', width=28, values=department_list)
    departmentEntry.grid(row=2, column=1, pady=15, padx=20, sticky=EW)

    eventnameLabel = Label(scrollable_frame, text='Event Name', font=('Helvetica', 20, 'bold'), fg='black')
    eventnameLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    eventnameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    eventnameEntry.grid(row=3, column=1, pady=15, padx=20, sticky=EW)

    fromdateLabel = Label(scrollable_frame, text='From Date', font=('Helvetica', 20, 'bold'), fg='black')
    fromdateLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    fromdateEntry = DateEntry(scrollable_frame, font=('Helvetica', 16), width=28, background='#FFFF00',
                              foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
    fromdateEntry.grid(row=4, column=1, pady=15, padx=20, sticky=EW)

    todateLabel = Label(scrollable_frame, text='To Date', font=('Helvetica', 20, 'bold'), fg='black')
    todateLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    todateEntry = DateEntry(scrollable_frame, font=('Helvetica', 16), width=28, background='#FFFF00',
                            foreground='black', borderwidth=2, date_pattern='yyyy-mm-dd')
    todateEntry.grid(row=5, column=1, pady=15, padx=20, sticky=EW)

    eventlocationLabel = Label(scrollable_frame, text='Event Location', font=('Helvetica', 20, 'bold'), fg='black')
    eventlocationLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    eventlocationEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    eventlocationEntry.grid(row=6, column=1, pady=15, padx=20, sticky=EW)

    mobileLabel = Label(scrollable_frame, text='Mobile Number (opt)', font=('Helvetica', 20, 'bold'), fg='black')
    mobileLabel.grid(row=7, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    mobileEntry.grid(row=7, column=1, pady=15, padx=20, sticky=EW)

    emailLabel = Label(scrollable_frame, text='Email (opt)', font=('Helvetica', 20, 'bold'), fg='black')
    emailLabel.grid(row=8, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    emailEntry.grid(row=8, column=1, pady=15, padx=20, sticky=EW)

    addressLabel = Label(scrollable_frame, text='Address', font=('Helvetica', 20, 'bold'), fg='black')
    addressLabel.grid(row=9, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    addressEntry.grid(row=9, column=1, pady=15, padx=20, sticky=EW)

    genderLabel = Label(scrollable_frame, text='Gender', font=('Helvetica', 20, 'bold'), fg='black')
    genderLabel.grid(row=10, column=0, padx=30, pady=15, sticky=W)
    genderEntry = ttk.Combobox(scrollable_frame, style='Custom.TCombobox', width=28, values=['Male', 'Female', 'Others'])
    genderEntry.grid(row=10, column=1, pady=15, padx=20, sticky=EW)

    pdfLabel = Label(scrollable_frame, text='Upload PDF (opt)', font=('Helvetica', 20, 'bold'), fg='black')
    pdfLabel.grid(row=11, column=0, padx=30, pady=15, sticky=W)
    pdfButton = ttk.Button(scrollable_frame, text='Upload PDF', style='FormYellow.TButton', command=upload_pdf)
    pdfButton.grid(row=11, column=1, pady=15, padx=20, sticky=EW)

    add_student_button = ttk.Button(scrollable_frame, text='Add Student', style='Yellow.TButton', command=add_data)
    add_student_button.grid(row=12, columnspan=2, pady=30)

def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(
                host=hostEntry.get(),
                user=usernameEntry.get(),
                password=passwordEntry.get(),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            mycursor = con.cursor()
            
            mycursor.execute('CREATE DATABASE IF NOT EXISTS participant')
            mycursor.execute('USE participant')
            
            mycursor.execute('SHOW TABLES LIKE "participant"')
            if not mycursor.fetchone():
                mycursor.execute(''' 
                    CREATE TABLE participant (
                        register_no BIGINT NOT NULL PRIMARY KEY CHECK (register_no BETWEEN 0 AND 9999999999999999999999),
                        name VARCHAR(30),
                        department VARCHAR(50),
                        event_name VARCHAR(35),
                        from_date VARCHAR(15),
                        to_date VARCHAR(15),
                        event_location VARCHAR(50),
                        mobile_no BIGINT,
                        email VARCHAR(50),
                        address VARCHAR(100),
                        gender VARCHAR(10),
                        pdf_file LONGBLOB,
                        date VARCHAR(10),
                        time VARCHAR(10)
                    )
                ''')
                con.commit()
            
            messagebox.showinfo('Success', 'Database connection successful!', parent=connect_window, icon='info')
            connect_window.destroy()
            addparticipantButton.config(state=NORMAL)
            searchparticipantButton.config(state=NORMAL)
            deleteparticipantButton.config(state=NORMAL)
            updateparticipantButton.config(state=NORMAL)
            showparticipantButton.config(state=NORMAL)
            exportdataparticipantButton.config(state=NORMAL)
            downloadpdfButton.config(state=NORMAL)
            updatedeptButton.config(state=NORMAL)
            show_participant()
            
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Database Error: {str(e)}', parent=connect_window, icon='error')

    connect_window = Toplevel()
    connect_window.title('Database Connection')
    connect_window.grab_set()
    connect_window.state('zoomed')
    set_background(connect_window)

    connect_window.is_fullscreen = False
    connect_window.bind('<F11>', lambda event: toggle_fullscreen(event, connect_window))
    connect_window.bind('<Escape>', lambda event: exit_fullscreen(event, connect_window))

    form_frame = Frame(connect_window, bg="#15F30D", bd=2, relief=RIDGE)
    form_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

    canvas = Canvas(form_frame, bg="#0BED8B")
    scrollbar = Scrollbar(form_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#0BED8B")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    hostnameLabel = Label(scrollable_frame, text='Host Name', font=('Helvetica', 20, 'bold'), fg='black')
    hostnameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    hostEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    hostEntry.grid(row=0, column=1, pady=15, padx=20, sticky=EW)
    hostEntry.insert(0, "localhost")

    usernameLabel = Label(scrollable_frame, text='User Name', font=('Helvetica', 20, 'bold'), fg='black')
    usernameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    usernameEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    usernameEntry.grid(row=1, column=1, pady=15, padx=20, sticky=EW)
    usernameEntry.insert(0, "root")

    passwordLabel = Label(scrollable_frame, text='Password', font=('Helvetica', 20, 'bold'), fg='black')
    passwordLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    passwordEntry = Entry(scrollable_frame, font=('Helvetica', 16), width=30, show="*", bg='#FFFF00', fg='black', bd=2, relief=FLAT)
    passwordEntry.grid(row=2, column=1, pady=15, padx=20, sticky=EW)
    passwordEntry.insert(0, 'rvs@9215')  # Enter your MySQL password here

    connectButton = ttk.Button(scrollable_frame, text='Connect', style='FormYellow.TButton', command=connect)
    connectButton.grid(row=3, columnspan=2, pady=30)

count = 0
text = ''
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)

def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\n   Time: {currenttime}')
    datetimeLabel.after(1000, clock)

# Main window setup
root = Tk()
root.title('Participant Management System')
set_background(root)

root.state('zoomed')

root.is_fullscreen = False
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', exit_fullscreen)

headerFrame = Frame(root, bg='#0288D1', bd=2, relief=RIDGE)
headerFrame.place(relx=0, rely=0, relwidth=1, height=80)

datetimeLabel = Label(headerFrame, font=('Helvetica', 16, 'bold'), fg='white', bg='#0288D1')
datetimeLabel.place(relx=0.01, rely=0.2)
clock()

s = 'Participant Management System'
sliderLabel = Label(headerFrame, text=s, font=('Helvetica', 20, 'bold'), fg='white', bg='#0288D1', width=40)
sliderLabel.place(relx=0.5, rely=0.3, anchor=CENTER)

connectButton = ttk.Button(headerFrame, text='Connect Database', style='Yellow.TButton', command=connect_database)
connectButton.place(relx=0.95, rely=0.3, anchor=E)

leftFrame = Frame(root, bg="#16AAE4", bd=2, relief=RIDGE)
leftFrame.place(relx=0.01, rely=0.15, relwidth=0.25, relheight=0.8)

try:
    logo_image = PhotoImage(file='student.png')
    logo_Label = Label(leftFrame, image=logo_image, bg='#87CEEB')
    logo_Label.image = logo_image
except TclError:
    logo_Label = Label(leftFrame, text="Logo Image Not Found", font=('Helvetica', 12, 'bold'), bg="#E36666", fg='#FF6F61')
logo_Label.grid(row=0, column=0, pady=20)

addparticipantButton = ttk.Button(leftFrame, text='Add Participant', style='Yellow.TButton', width=20, state=DISABLED, command=add_student)
addparticipantButton.grid(row=1, column=0, pady=15)

searchparticipantButton = ttk.Button(leftFrame, text='Search Participant', style='Yellow.TButton', width=20, state=DISABLED, command=search_participant)
searchparticipantButton.grid(row=2, column=0, pady=15)

deleteparticipantButton = ttk.Button(leftFrame, text='Delete Participant', style='Yellow.TButton', width=20, state=DISABLED, command=delete_participant)
deleteparticipantButton.grid(row=3, column=0, pady=15)

updateparticipantButton = ttk.Button(leftFrame, text='Update Participant', style='Yellow.TButton', width=20, state=DISABLED, command=update_participant)
updateparticipantButton.grid(row=4, column=0, pady=15)

showparticipantButton = ttk.Button(leftFrame, text='Show Participant', style='Yellow.TButton', width=20, state=DISABLED, command=show_participant)
showparticipantButton.grid(row=5, column=0, pady=15)

exportdataparticipantButton = ttk.Button(leftFrame, text='Export Data', style='Yellow.TButton', width=20, state=DISABLED, command=export_data)
exportdataparticipantButton.grid(row=6, column=0, pady=15)

downloadpdfButton = ttk.Button(leftFrame, text='Download PDF', style='Yellow.TButton', width=20, state=DISABLED, command=download_pdf)
downloadpdfButton.grid(row=7, column=0, pady=15)

updatedeptButton = ttk.Button(leftFrame, text='Update Department', style='Yellow.TButton', width=20, state=DISABLED, command=update_department)
updatedeptButton.grid(row=8, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text='Exit', style='Yellow.TButton', width=20, command=iexit)
exitButton.grid(row=9, column=0, pady=15)

rightFrame = Frame(root, bg="red", bd=2, relief=RIDGE)
rightFrame.place(relx=0.3, rely=0.15, relwidth=0.67, relheight=0.8)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

participantTable = ttk.Treeview(rightFrame, style='Custom.Treeview', columns=('Register_no', 'Name', 'Department', 'Event_Name', 'From_Date', 'To_Date', 'Event_Location', 'Mobile_no', 'Email', 'Address', 'Gender', 'Added_Date', 'Added_Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set, show='headings')

scrollBarX.config(command=participantTable.xview)
scrollBarY.config(command=participantTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
participantTable.pack(fill=BOTH, expand=1)

participantTable.heading('Register_no', text='Register Number')
participantTable.heading('Name', text='Name')
participantTable.heading('Department', text='Department')
participantTable.heading('Event_Name', text='Event Name')
participantTable.heading('From_Date', text='From Date')
participantTable.heading('To_Date', text='To Date')
participantTable.heading('Event_Location', text='Event Location')
participantTable.heading('Mobile_no', text='Mobile Number')
participantTable.heading('Email', text='Email')
participantTable.heading('Address', text='Address')
participantTable.heading('Gender', text='Gender')
participantTable.heading('Added_Date', text='Added Date')
participantTable.heading('Added_Time', text='Added Time')

participantTable.column('Register_no', width=190, anchor=CENTER, stretch=True)
participantTable.column('Name', width=190, anchor=CENTER, stretch=True)
participantTable.column('Department', width=190, anchor=CENTER, stretch=True)
participantTable.column('Event_Name', width=140, anchor=CENTER, stretch=True)
participantTable.column('From_Date', width=190, anchor=CENTER, stretch=True)
participantTable.column('To_Date', width=190, anchor=CENTER, stretch=True)
participantTable.column('Event_Location', width=190, anchor=CENTER, stretch=True)
participantTable.column('Mobile_no', width=180, anchor=CENTER, stretch=True)
participantTable.column('Email', width=190, anchor=CENTER, stretch=True)
participantTable.column('Address', width=260, anchor=CENTER, stretch=True)
participantTable.column('Gender', width=140, anchor=CENTER, stretch=True)
participantTable.column('Added_Date', width=140, anchor=CENTER, stretch=True)
participantTable.column('Added_Time', width=140, anchor=CENTER, stretch=True)

participantTable.tag_configure('evenrow', background="skyblue")
participantTable.tag_configure('oddrow', background="skyblue")

apply_styles()
slider()
root.mainloop()