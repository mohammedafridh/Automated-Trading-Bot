import MetaTrader5 as mt5
import pandas as pd

class Bot:
    def __init__(self, symbol,volume,tp,cycles,no_of_levels):
        self.symbol = symbol
        self.volume = volume
        self.tp = tp
        self.cycles = cycles
        self.no_of_levels = no_of_levels

    def buy_limit(self,price, volume, symbol):
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY_LIMIT,
            "price": price,
            "magic": 100,
            "deviation": 20,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        result = mt5.order_send(request)
        print(result)

    def sell_limit(self,price, volume, symbol):
        request = {
            "action": mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL_LIMIT,
            "price": price,
            "magic": 100,
            "deviation": 20,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        result = mt5.order_send(request)
        print(result)

    def cal_profit(self,symbol):
        usd_positions = mt5.positions_get(symbol=symbol)
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        profit = float(df['profit'].sum())
        return profit

    def cal_volume(self,symbol):
        usd_positions = mt5.positions_get(symbol=symbol)
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        profit = float(df['volume'].sum())
        return profit

    def cal_buy_profit(self,symbol):
        usd_positions = mt5.positions_get(symbol=symbol)
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        df = df.loc[df.type == 0]
        profit = float(df['profit'].sum())
        return profit

    def cal_sell_profit(self,symbol):
        usd_positions = mt5.positions_get(symbol=symbol)
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        df = df.loc[df.type == 1]
        profit = float(df['profit'].sum())
        return profit

    def cal_buy_margin(self,symbol):
        usd_positions = mt5.positions_get(symbol=symbol)
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        df = df.loc[df.type == 0]

        sum = 0

        for i in df.index:
            volume = df.volume[i]
            open_price = df.price_open[i]
            margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, volume, open_price)
            sum += margin

        return sum

    def cal_sell_margin(self,symbol):
        usd_positions = mt5.positions_get(symbol=symbol)
        df = pd.DataFrame(list(usd_positions), columns=usd_positions[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        df = df.loc[df.type == 1]

        sum = 0

        for i in df.index:
            volume = df.volume[i]
            open_price = df.price_open[i]
            margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, volume, open_price)
            sum += margin

        return sum

    def cal_buy_pct_profit(self,symbol):
        profit = self.cal_buy_profit(symbol)
        margin = self.cal_buy_margin(symbol)
        pct_proft = (profit / margin) * 100
        return pct_proft

    def cal_sell_pct_profit(self,symbol):
        profit = self.cal_sell_profit(symbol)
        margin = self.cal_sell_margin(symbol)
        pct_proft = (profit / margin) * 100
        return pct_proft

    def close_position(self,position):
        tick = mt5.symbol_info_tick(position.symbol)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
            "price": tick.ask if position.type == 1 else tick.bid,
            "deviation": 20,
            "magic": 100,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        return result

    def close_all(self,symbol):
        positions = mt5.positions_get(symbol=symbol)
        for i in positions:
            self.close_position(i)

    def delete_pending(self,ticket):
        close_request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(close_request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            result_dict = result._asdict()
            print(result_dict)
        else:
            print('Delete complete...')

    def close_all_pending(self,symbol):
        orders = mt5.orders_get(symbol=symbol)
        df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
        df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial',
                 'price_stoplimit'], axis=1, inplace=True)
        df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
        for ticket in df.ticket:
            self.delete_pending(ticket)

    def draw_grid(self,symbol, volume, no_of_levels):
        pct_change = 1
        info = mt5.symbol_info_tick(symbol)
        bid = info.bid

        for i in range(no_of_levels):
            price = ((pct_change / (100 * 100)) * bid) + bid
            self.sell_limit(price, volume, symbol)
            pct_change += 1

        pct_change_2 = -1
        info = mt5.symbol_info_tick(symbol)
        bid2 = info.bid

        for i in range(no_of_levels):
            price = ((pct_change_2 / (100 * 100)) * bid2) + bid2
            self.buy_limit(price, volume, symbol)
            pct_change_2 -= 1



    def run(self):
        for i in range(self.cycles):

            self.draw_grid(self.symbol, self.volume, self.no_of_levels)

            while True:
                positions = mt5.positions_get(symbol=self.symbol)
                if len(positions) > 0:
                    try:
                        buy_margin = self.cal_buy_margin(self.symbol)
                        sell_margin = self.cal_sell_margin(self.symbol)

                    except:
                        pass

                    if buy_margin > 0:
                        try:
                            pct_profit = self.cal_buy_pct_profit(self.symbol)
                            print(f"Profit of buy positions: {pct_profit} %")
                            if pct_profit >= self.profit_target:
                                self.close_all(self.symbol)
                        except:
                            pass

                    if sell_margin > 0:
                        try:
                            pct_profit = self.cal_sell_pct_profit(self.symbol)
                            print(f"Profit of sell positions: {pct_profit} %")
                            if pct_profit >= self.profit_target:
                                self.close_all(self.symbol)
                        except:
                            pass

                    positions = mt5.positions_get(symbol=self.symbol)
                    if len(positions) == 0:
                        try:
                            self.close_all_pending(self.symbol)
                            break
                        except:
                            pass

