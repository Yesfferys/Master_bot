from pprint import pprint
from time import sleep
import Clave_personal
import pandas as pd
import pandas
from binance.spot import Spot


from utils.strategy import indicators


class RobotBinance:
    """
    Bot para Binance que permit automatizar las compras y ventas en el mercado spot
    """
    __api_key = Clave_personal.API_KEY
    __api_secret = Clave_personal.API_SECRET_KEY
    binance_client = Spot(key=__api_key, secret=__api_secret)  # inicia la conexion con binance en el mercado spot

    def __init__(self, pair: str, temporality: str):
        self.pair1 = pair.upper()
        self.temporality = temporality
        self.symbol = self.pair1.removesuffix("USDT")

    def _request(self, endpoint: str, parameters: dict = None):
        while True:
            try:
                response = getattr(self.binance_client, endpoint)  # => self.binance_client.endpoint
                return response() if parameters is None else response(**parameters)
            except:
                print(f"El endpoint {endpoint} a fallado. \n Parametros: {parameters}")
                sleep(3)

    def binance_account(self, recvWindow: int = None, timestamp: int = None) -> dict:
        """
        Devuelve las metricas y balances asociados a la cuenta.
        :type: object
        :return:cuenta de binance
        """
        recvWindow = 59000 if recvWindow is None else recvWindow
        timestamp = 50 if timestamp is None else timestamp
        return self._request("account",
                             {"recvWindow": recvWindow, "timestamp": timestamp})  # se visualizan 512 asset(activos)

    def cryptocurrencies(self) -> dict:
        """
        Devuelve una lista con todas las criptomonedas en la cuenta que tengan un saldo positivo
        return:Criptomonedas
        """
        return [crypto for crypto in self.binance_account().get("balances") if float(crypto.get("free")) > 0]

    def symbol_price(self, pair: str = None):
        """
        Devuelve el precio para un determinado par
        :param pair: criptomoneda a determinar el precio ["BTCUSDT","  ETHUSDT   "]
        :return:precio del par
        """
        symbol = self.pair1 if pair is None else pair
        return float(self._request("ticker_price", {"symbol": symbol.upper()}).get("price"))

    def candlesticks(self, limit: int = 200) -> pd.DataFrame:
        """
        Devuelve la informacion de las velas.
        :return:velas japonesas
        """
        params = {"symbol": self.pair1,
                  "interval": self.temporality,
                  "limit": limit}
        candle = pd.DataFrame(self._request("klines", params
                                            ),
                              columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                       "quote asset volume",
                                       "number of trade", "Taker buy base asset volume", "taker buy quote asset volume",
                                       "ignore"
                                       ],
                              dtype=float
                              )
        return candle[["Open Time", "Close Time", "Open", "High", "Low", "Close", "Volume"]]

if __name__ == "__main__":
    bot = RobotBinance("btcusdt", "4h")
    #pprint(type(bot.candlesticks()))  # <class 'pandas.core.frame.DataFrame'>
    #pprint(bot.candlesticks())
    #pprint(indicators(bot.candlesticks()).ema())
    #pprint(indicators(bot.candlesticks()).rsi())
    #pprint(indicators(bot.candlesticks()).macd(12,26,9))
    #pprint(indicators(bot.candlesticks())) #<utils.stragety.indicators object at 0x00000045C862AD00>
    pprint(indicators(bot.candlesticks()). adx())