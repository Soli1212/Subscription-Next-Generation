from telethon import TelegramClient
from telethon.sessions import StringSession
from colorama import Fore, init
from pyperclip import copy
from os import system


init(autoreset=True)

system("cls")

print(Fore.GREEN + "https://github.com/Soli1212")

print("")

api_id = int(input(Fore.RESET+ "enter your api-id -> "))
api_hash = input(Fore.RESET+ "enter your api-hash -> ")
phone_number = input(Fore.RESET+ "Enter phone number (+98919 ...) -> ")

client = TelegramClient(StringSession(), api_hash=api_hash, api_id=api_id)

async def main():
    await client.start(phone_number)
    session_string = client.session.save()
    return session_string


SessionStr = client.loop.run_until_complete(main())

system("cls")

print("")
print(Fore.LIGHTGREEN_EX+ SessionStr)
print("")

print(Fore.LIGHTRED_EX+ "[0] - exit ")
print(Fore.LIGHTCYAN_EX+ "[1] - copy and exit")

work = input()

if work == 1: 
    copy(SessionStr)
    print(Fore.GREEN+ "session copied to clipboard")


