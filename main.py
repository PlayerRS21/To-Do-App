import json

from pathlib import Path

import os

import platform

from datetime import datetime

import time

path = "list.json"

to_do_list = {}
tasks_remaining = []
tasks_completed = []

def clear_terminal() -> bool:
    current_os = platform.system().lower()
    time.sleep(1)
    try:
        if current_os == "windows":
            os.system('cls')
        elif current_os in ("linux", "darwin"):  # 'darwin' is macOS
            os.system('clear')
        else:
            # Fallback for unexpected terminal types or environments
            print("\033[H\033[2J", end="")
        return True
    except Exception:
        return False

def greet_user():
    clear_terminal()
    print("Hello User\nWelcome to your to do list app.")

def get_time():
    now = datetime.now()
    a = f"{now.strftime('%H:%M:%S')}"
    return a

def load_variables():
    global to_do_list
    global tasks_completed
    global tasks_remaining
    tasks_completed = []
    tasks_remaining = []
    
    for key, value  in to_do_list.items():
        entry = {key:value}
        if value["status"] == "completed":
            tasks_completed.append(entry)
        else:
            tasks_remaining.append(entry)

    # print(to_do_list,tasks_completed,tasks_remaining,end="\n")
        
def save_list():
    global to_do_list
    with open("list.json","w") as file:
        json.dump(to_do_list,file, indent=4)
    print("data saved")
    load_variables()
    clear_terminal()
    to_do_list_terminal_ui()

def create_new_task():
    task_number = len(to_do_list) + 1
    abc = f"task{task_number}"
    name = input("Enter the name of the task: ")
    time = get_time()
    to_do_list.update(
    {abc:
        {"name" : name,
        "time" : time,
        "status" : "pending", 
        "type" : "one_time", 
        "completion_time" : "Null"},
    })
    save_list()

def selected_task(num):
    num = num -1
    global tasks_remaining
    x = tasks_remaining[num]
    for i in x:
        print("Task",'"'+x[i]["name"]+'"', "selected:")
    a = input("""Enter what you have in mind:
    Mark as Completed (press \"c\")
    Delete Task (press \"d\")
    Back to main menu (press \"b\")
    Exit the app (press \"e\")
    >>> """)
    if a.lower() == "c":
        x = list(tasks_remaining[num].keys())[0]
        to_do_list[x]["status"] = "completed"
        to_do_list[x]["completion_time"] = get_time()
        save_list()
        load_variables()
        print("Done, returning to main menu.")
        clear_terminal()
        to_do_list_terminal_ui()
    elif a.lower() == "d":
        for i in range(len(tasks_remaining)):
            if i == num:
                a = dict(tasks_remaining[i])
                for x in a:
                    z = list(a.keys())[0]
                    to_do_list.pop(z)
                    save_list()
                    load_variables()
        clear_terminal()
        to_do_list_terminal_ui()
    elif a.lower() == "b":
        clear_terminal()
        to_do_list_terminal_ui()
    elif a.lower() == "e":
        print("Program exiting...")
        exit()
    else:
        print("Invalid Input.")
        clear_terminal()
        current_tasks_handler()

def current_tasks_handler():
    global tasks_remaining
    for i in range(len(tasks_remaining)):
        for x in tasks_remaining[i]:
            print(i+1," : ",tasks_remaining[i][x]["name"])

    user_input = input("Select a task or press \"n\" to create new or press \"b\" to go back:\n>> ")
    input("")
    try:
        user_input = int(user_input)
        if user_input > len(tasks_remaining):
            print("Invalid Input")
            clear_terminal()
            current_tasks_handler()
        else:
            selected_task(user_input)
    except ValueError:
        if user_input.lower() == "n":
            create_new_task()
        elif user_input.lower() == "b":
            clear_terminal()
            to_do_list_terminal_ui()
        else:
            print("Invalid Input")
            clear_terminal()
            current_tasks_handler()

def clear_completed_tasks():
    lst = list(to_do_list.items())
    # print(lst)
    for key, value  in lst:
        entry = {key:value}
        if value["status"] == "completed":
            to_do_list.pop(key)
    
    save_list()
    print("Done")
    clear_terminal()
    to_do_list_terminal_ui()

def completed_tasks_handler():
    for i in range(len(tasks_completed)):
        for x in tasks_completed[i]:
            print(i+1," : ",tasks_completed[i][x]["name"]," : ",tasks_completed[i][x]["completion_time"])
    user_input = input("Return to main menu (press b)\nClear History (press c)\n>> ").lower()
    if user_input == "b":
        clear_terminal()
        to_do_list_terminal_ui()
    elif user_input == "c":
        clear_completed_tasks()
        clear_terminal()
        to_do_list_terminal_ui()

def to_do_list_terminal_ui():
    user_input = input("Select What you want to do:\nView Current tasks (Add new task from here) {Press 1}\nShow Completed tasks {Press 2}\nExit {press e}\n>> ")
    try:
        user_input = int(user_input)
        if user_input == 1:
            current_tasks_handler()
        elif user_input == 2:
            completed_tasks_handler()
        else:
            print("Invalid Input")
            clear_terminal()
            to_do_list_terminal_ui()
    except ValueError:
        if user_input.lower() == "e":
            print("Program exiting...")
            exit()
        else:
            print("Bad Input")
            clear_terminal()
            to_do_list_terminal_ui()

def load_to_do_list():
    global to_do_list
    try:
        with open("list.json","r") as file:
            to_do_list = json.load(file)
            print("File Loaded")
    except json.decoder.JSONDecodeError:
        to_do_list = {}
    print("Variable Created Sucessfully")
    load_variables()
    print("variables loaded")
    greet_user()
    to_do_list_terminal_ui()

def file_exist_or_not(a):
    while a < 2:
        if Path(path).exists():
            if a == 0:
                print("File Found...\nProceeding.")
                load_to_do_list()
                break
            else:
                print("Done File Creation")
                load_to_do_list()
                break
        else:
            print("File not Found\nProceeding with File Creation.")
            with open("list.json","w") as f:
                f.write("")
            a = a+1
    else:
        print("Error in File Creation.")
        raise FileNotFoundError("The File Can't be Created Please Contact Support.")

file_exist_or_not(0)
