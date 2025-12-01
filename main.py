from classes import Bot
import pandas as pd
import MetaTrader5 as mt5
from threading import Thread
import tkinter as tk
import time
import os
from dotenv import load_dotenv

load_dotenv()

login = os.getenv("login")
server = os.getenv("server")
password = os.getenv("password")

if not mt5.initialize(login=int(login), server=server, password=password):
    print("MT5 initialization failed!")
    print("Error:", mt5.last_error())
    quit()

time.sleep(1)

symbol = "EURUSD"
info = mt5.symbol_info(symbol)

if info is None:
    print(f"Symbol '{symbol}' not found!")
    print("Error:", mt5.last_error())
    quit()

print(f"Trade Allowed: {info.trade_mode}, Market Open: {info.visible}")


bot1 = Bot('EURUSD',0.01,0.2,2,15)
bot2 = Bot('USDJPY',0.01,0.2,2,15)
bot3 = Bot('GBPUSD',0.01,0.2,2,15)
bot4 = Bot('USDCHF',0.01,0.2,2,5)

threads = [
    Thread(target=bot1.run),
    Thread(target=bot2.run),
    Thread(target=bot3.run),
    Thread(target=bot4.run)
]

for t in threads:
    t.start()

root = tk.Tk()
root.title('Forex Grid Master')
root.geometry('500x500')
root.resizable(False, False)
icon = tk.PhotoImage(file='trading_bot.jpg')
root.iconphoto(False, icon)

root.mainloop()
