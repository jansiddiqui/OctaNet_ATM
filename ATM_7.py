import tkinter as tk
import textwrap
from tkinter import PhotoImage, messagebox, ttk
from datetime import datetime
import pygame
import threading
from user_data import users

current_user = None  # logged-in user's data

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

pygame.init()

sound_files = {
    "send_money": "Credited.mp3",
    "withdraw_money": "withdrawal.mp3"
}

def play_sound(action):
    sound_file = sound_files.get(action)
    if sound_file:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        threading.Thread(target=wait_for_sound_end).start()
    else:
        print("Sound file not found for action:", action)

def wait_for_sound_end():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                running = False

def create_message_window(title, message, action=None):
    message_window = tk.Toplevel(root)
    message_window.title(title)
    message_window.geometry("450x250")
    message_window.configure(bg='#AED6F1')

    # Disable minimize and maximize buttons
    message_window.resizable(False, False)

    # Center the window on the screen
    window_width = 450
    window_height = 250
    screen_width = message_window.winfo_screenwidth()
    screen_height = message_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    message_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # Center the message text
    formatted_message = "\n".join(textwrap.wrap(message, width=30))
    tk.Label(message_window, text=formatted_message, font=('Helvetica', 12), bg='#AED6F1', fg='#21618C', justify="center").pack(pady=20, anchor="center")
    if action:
        ttk.Button(message_window, text="OK", command=lambda: (message_window.destroy(), action()), style='Water.TButton').pack(pady=5)
    else:
        ttk.Button(message_window, text="OK", command=message_window.destroy, style='Water.TButton').pack(pady=5)

def amount_info():
    current_datetime = get_current_datetime()
    current_date, current_time = current_datetime.split(" ")
    message = f'''
        ------------------------
        - Name : {current_user}
        - Total Balance : {users[current_user]["balance"]}
        - Date: {current_date}       
        - Time: {current_time}
        ------------------------
        '''
    create_message_window("Account Information", message)

def withdraw_money():
    clear_screen()
    current_datetime = get_current_datetime()
    current_date, current_time = current_datetime.split(" ")
    tk.Label(root, text="Enter Desired Amount", font=('Helvetica', 14), bg='#AED6F1').pack(pady=10)
    withdraw_amount_entry = tk.Entry(root, font=('Helvetica', 12), justify="center")
    withdraw_amount_entry.pack(pady=5)
    def process_withdrawal():
        withdraw_amount = int(withdraw_amount_entry.get())
        if withdraw_amount <= users[current_user]["balance"]:
            users[current_user]["balance"] -= withdraw_amount
            message = f'''
                ----------------------------
                - Name : {current_user}
                - Amount : {withdraw_amount} Rs. 
                - Amount Remaining : {users[current_user]["balance"]} Rs.                  
                - Date: {current_date}
                - Time: {current_time}
                ----------------------------
                '''
            create_message_window("Withdrawal", message, lambda: play_sound("withdraw_money"))
        else:
            messagebox.showwarning("Warning", "Insufficient funds!")
    ttk.Button(root, text="Submit", command=process_withdrawal, style='Water.TButton').pack(pady=10)
    ttk.Button(root, text="Back", command=show_main_menu, style='Water.TButton').pack(pady=5)

def send_money():
    clear_screen()
    current_datetime = get_current_datetime()
    tk.Label(root, text="Enter Recipient Name", font=('Helvetica', 14), bg='#AED6F1').pack(pady=10)
    recipient_name_entry = tk.Entry(root, font=('Helvetica', 12), justify="center")
    recipient_name_entry.pack(pady=5)
    tk.Label(root, text="Enter Amount to Send", font=('Helvetica', 14), bg='#AED6F1').pack(pady=10)
    send_amount_entry = tk.Entry(root, font=('Helvetica', 12), justify="center")
    send_amount_entry.pack(pady=5)
    def process_send():
        recipient_name = recipient_name_entry.get()
        if recipient_name and recipient_name in users:
            sent_amount = int(send_amount_entry.get())
            if sent_amount <= users[current_user]["balance"]:
                users[current_user]["balance"] -= sent_amount
                users[recipient_name]["balance"] += sent_amount
                current_datetime = get_current_datetime()
                current_date, current_time = current_datetime.split(" ")
                message = f'''
                ----------------------------
                Name: {current_user}
                Recipient Name: {recipient_name}
                Amount: {sent_amount} Rs.
                Amount Remaining: {users[current_user]["balance"]} Rs.
                Date: {current_date}
                Time: {current_time}
                ----------------------------
                '''
                create_message_window("Send Money", message, lambda: play_sound("send_money"))
            else:
                messagebox.showwarning("Warning", "Insufficient funds!")
        else:
            messagebox.showwarning("Warning", "Recipient not found!")
    ttk.Button(root, text="Submit", command=process_send, style='Water.TButton').pack(pady=10)
    ttk.Button(root, text="Back", command=show_main_menu, style='Water.TButton').pack(pady=5)

def check_pin():
    global current_user
    username = username_entry.get()
    pin = pin_entry.get()
    if username in users:
        if int(pin) == users[username]["pin"]:
            current_user = username
            messagebox.showinfo("Welcome", f"Welcome {current_user}!")
            show_main_menu()
        else:
            messagebox.showwarning("Warning", ''' 
                  *******************
                        Warning ! 
                    Wrong Code Entered 
                    Ejecting your card... 
                  *******************
                    ''')
    else:
        messagebox.showwarning("Warning", "Username not found!")

def show_main_menu():
    clear_screen()
    tk.Label(root, text=" ATM Menu ", font=('Helvetica', 18, 'bold'), bg='#AED6F1', fg='#21618C').pack(pady=20)
    ttk.Button(root, text=" Withdraw Money ", command=withdraw_money, style='Water.TButton').pack(pady=5)
    ttk.Button(root, text=" Send Money ", command=send_money, style='Water.TButton').pack(pady=5)
    ttk.Button(root, text=" Account Information ", command=amount_info, style='Water.TButton').pack(pady=5)
    ttk.Button(root, text=" Quit ", command=root.destroy, style='Water.TButton').pack(pady=5)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("HappyBank ATM")
root.geometry("450x350")
root.configure(bg='#AED6F1')
root.resizable(False, False)
icon = PhotoImage(file="atm2.png")
root.iconphoto(False, icon)

style = ttk.Style()
style.configure('Water.TButton', font=('Helvetica', 12), padding=6, relief='flat', background='#85C1E9', foreground='#154360')

tk.Label(root, text="Welcome to HappyBank ATM", font=('Helvetica', 18, 'bold'), bg='#AED6F1', fg='#21618C').pack(pady=20)
tk.Label(root, text="Please insert your card and enter your username", font=('Helvetica', 14), bg='#AED6F1').pack(pady=10)

tk.Label(root, text="Enter Your Username", font=('Helvetica', 14), bg='#AED6F1').pack(pady=10)
username_entry = tk.Entry(root, font=('Helvetica', 12), justify="center")
username_entry.pack(pady=5)

tk.Label(root, text="Enter Your PIN", font=('Helvetica', 14), bg='#AED6F1').pack(pady=10)
pin_entry = tk.Entry(root, font=('Helvetica', 12), show='*', justify="center")
pin_entry.pack(pady=5)

ttk.Button(root, text="Submit", command=check_pin, style='Water.TButton').pack(pady=10)

root.mainloop()

