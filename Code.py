import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Request Denied !!!', 'Field is Empty!')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        selected_indices = task_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo('Request Denied !!!', 'Please Select the task(s) to delete !')
            return

        for index in reversed(selected_indices):
            selected_task = tasks[index]
            tasks.pop(index)
            the_cursor.execute('delete from tasks where title = ?', (selected_task,))
        
        list_update()

    except IndexError:
        messagebox.showinfo('Request Denied !!!', 'Please Select the task to delete !')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?')
    if message_box:
        tasks.clear()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List Manager - AKHILESH")
    guiWindow.geometry("500x450+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#FAEBD7")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    header_frame = tk.Frame(guiWindow, bg="dark orange")
    functions_frame = tk.Frame(guiWindow, bg="dark orange")
    listbox_frame = tk.Frame(guiWindow, bg="dark orange")

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="To-Do List",
        font=("Alice", "30", "bold"),
        background="dark orange",
        foreground="#FFFFFF"
    )
    header_label.pack(padx=10, pady=10)

    task_label = ttk.Label(
        functions_frame,
        text="Enter the Task:",
        font=("Alice", "11", "bold"),
        background="dark orange",
        foreground="#FFFFFF"
    )
    task_label.place(x=30, y=40)

    task_field = ttk.Entry(
        functions_frame,
        font=("Consolas", "12"),
        width=18,
        background="dark orange",
        foreground="#A52A2A"
    )
    task_field.place(x=30, y=80)

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=24,
        command=add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=24,
        command=delete_task
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete All",
        width=24,
        command=delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=24,
        command=close
    )
    add_button.place(x=30, y=120)
    del_button.place(x=30, y=160)
    del_all_button.place(x=30, y=200)
    exit_button.place(x=30, y=240)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=26,
        height=13,
        selectmode='multiple',  # Use 'multiple' for multiple selections
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#CD853F",
        selectforeground="#FFFFFF"
    )
    task_listbox.place(x=10, y=20)

    retrieve_database()
    list_update()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
