import asyncio
import sqlite3
import tkinter as tk

import ttkbootstrap as ttb
from db import chats, messages, users
from gui import login_gui,stats_gui
from src import telegram_client
from telethon import TelegramClient, errors
from telethon.tl.types import User
from ttkbootstrap.constants import *

db_name="telegram_stats_db.db"
# from gui import login_gui


# chats_window = tk.Toplevel(telegram_client.root)
lisb = tk.Listbox(telegram_client.root)
label = ttb.Label(telegram_client.root, text="Press to get your chats list")

fetch_chats_button = ttb.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))
info_text = ttb.Text(telegram_client.root, height=5, width=40)

get_info_button = ttb.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb)))
chat_list=[]
users_list=[]
def open_new_window():
    global lisb  
    global fetch_chats_button  
    global get_info_button  
    global label
    telegram_client.root.title("Chat list")
    label = ttb.Label(telegram_client.root, text="Press to get your chats list")

    label.place(relx=0.5, rely=0.3,anchor="center")
    fetch_chats_button = ttb.Button(telegram_client.root, text="Fetch Chats", command=lambda: asyncio.get_event_loop().run_until_complete(fetch_and_populate(lisb)))
    
    fetch_chats_button.place(relx=0.5, rely=0.34,anchor="center")
    
    lisb = tk.Listbox(telegram_client.root, height=20, width=30)

    # info_text = ttb.Text(telegram_client.root, height=5, width=40)


    # telegram_client.root.mainloop()



async def populate_listbox(lb):
    
    await save_chats()
    await get_chats()
    # chat_list=[]
    lb.delete(0, tk.END)  # Clear previous items in the listbox
    for chat in chat_list:
        lb.insert(tk.END, chat[0])
   
    get_info_button = ttb.Button(telegram_client.root, text="Get Info", command=lambda: asyncio.get_event_loop().run_until_complete(display_chat_info(lisb,info_text)))
    get_info_button.place(relx=0.5, rely=0.71,anchor="center")    

# root = tk.Tk()
# root.title("Telegram Login")

async def fetch_and_populate(lb):
    global label
    label.destroy()
    fetch_chats_button.destroy()
    # Create a label with the loading message and place it on the root window
    label = ttb.Label(telegram_client.root, text="Loading...")
    label.place(relx=0.5, rely=0.3, anchor="center")

    # Create the progress bar
    progressbar = ttb.Progressbar(telegram_client.root, bootstyle="danger-striped")
    progressbar.place(relx=0.5, rely=0.4, anchor="center")
    progressbar.start()

    # Run the populate_listbox task in parallel
    task = asyncio.create_task(populate_listbox(lb))


    # Continuously update the label while waiting for populate_listbox to finish
    while not task.done():

        telegram_client.root.update_idletasks()  # Update the window to display the updated label
        await asyncio.sleep(0.1)  # Adjust the sleep duration as needed

   
    # loading()
    # progressbar.start()
    # await populate_listbox(lb)
    progressbar.destroy()
 
    # label.destroy()
    label = ttb.Label(telegram_client.root, text="This is list of your chats, choose one to analyze")

    label.place(relx=0.5, rely=0.3,anchor="center")
    lb.place(relx=0.5, rely=0.5,anchor="center")

# def display_statistics():
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()

#     # Выбираем все записи из таблицы statistics
#     cursor.execute('SELECT * FROM messages')
#     rows = cursor.fetchall()

#     # Выводим данные
#     for row in rows:
#         print(row)

#     conn.close()

async def display_chat_info(lb,info_text):
    # info_text.pack()
    selected_index = lb.curselection()  # Get the index of the selected item
    if selected_index:
        selected_chat_name = lb.get(selected_index) 
         # Get the selected chat name
        for chat in chat_list:
            if chat[0]==selected_chat_name:

                offset_id = 0  # Идентификатор сообщения для смещения
                limit = 100     # Максимальное количество сообщений, возвращаемых за один запрос

                while True:
                    # Получаем порцию сообщений из целевого чата
                    all_messages = await login_gui.client.get_messages(chat[1], limit=limit, offset_id=offset_id)

                    # Если сообщений нет, завершаем цикл
                    if not all_messages:
                        break

                    # Собираем статистику для каждого сообщения
                    for message in all_messages:
                        messages.save_message_statistics(message)

                    # Устанавливаем новое значение offset_id для следующего запроса
                    offset_id = all_messages[-1].id

                # info_text.delete(1.0, tk.END)  # Clear previous info
                # info_text.insert(tk.END, f"Chat Name: {chat[0]}\n")
                await save_users(login_gui.client, chat[1])
                # info_text.insert(tk.END, f"Chat ID: {chat[1]}\n")
    stats_gui.display_stats()
    # await get_users()


async def save_chats():
# Получаем список чатов
    # label.destroy()


    dialogs = await login_gui.client.get_dialogs()

# Создаем таблицу, если ее нет
# chats.create_chats_table()

# Выводим информацию о чатах и сохраняем их в базу данных
    for dialog in dialogs:
        # print(f"Chat ID: {dialog}")

        chats.save_chat_to_db(dialog)



async def get_chats():    
    # Assuming 'client' is your connected TelegramClient instance
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT chat_title, chat_id FROM chats ')
    rows = cursor.fetchall()
    
    global chat_list

    for row in rows:
        chat_list.append((row[0],row[1]))
        # print(row[0])
    connection.commit()
    connection.close()

async def get_users():    
    # Assuming 'client' is your connected TelegramClient instance
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users ')
    rows = cursor.fetchall()
    # print(rows)
    global users_list

    for row in rows:
        users_list.append((row[0],row[1],row[2],row[3]))
        # print("users"+row)
    connection.commit()
    connection.close()
    # return chat_list       

async def save_users(client, chat_id):

        participants = await client.get_participants(chat_id)
        for participant in participants:
            if isinstance(participant, User):
                user_id = participant.id
                phone = participant.phone
                name = participant.first_name + " " + participant.last_name if participant.last_name else participant.first_name
                username = participant.username
                print(user_id,phone,name,username)
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT INTO users (user_id, phone, name,username)
                    VALUES (?, ?, ?,?)
                ''', (user_id, phone,name,username))

                conn.commit()
                conn.close()



def clear_form():
    for widget in telegram_client.root.winfo_children():
        widget.destroy()    

