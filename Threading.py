from threading import Thread

class Bot:
    def __init__(self,symbol,volume,profit_target):
        self.symbol = symbol
        self.volume = volume
        self.profit_target = profit_target

    def run(self):
        while True:
            print(f'{self.symbol} {self.volume} {self.profit_target} im trading with these settings.' )


bot1 = Bot('BTCUSDT','0.01','0.2')
bot2 = Bot('EURUSD','0.02','1')
bot3 = Bot('GBPUSD','0.03','0.5')

# bot1.run()
# bot2.run()
# bot3.run()

thread1 = Thread(target=lambda: bot1.run())
thread2 = Thread(target=lambda:bot2.run())
thread3 = Thread(target=lambda:bot3.run())

thread1.start()
thread2.start()
thread3.start()
