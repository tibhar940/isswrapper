import matplotlib.pyplot as plt


def tradesplot(trades, securityid=None):
    fig, [ax1, ax2] = plt.subplots(2, 1, figsize=[16, 6])
    ax1.plot(trades["systime"], trades["price"], color="red")
    ax2.plot(trades["systime"], trades["quantity"], color="green")
    ax1.set_xlabel("time")
    ax1.set_ylabel("price")
    ax2.set_xlabel("time")
    ax2.set_ylabel("quantity")
    ax1.set_title("Trades plot ({0})".format(securityid))
    return fig, [ax1, ax2]


def candlesplot(candles, securityid=None):
    fig, [ax1, ax2] = plt.subplots(2, 1, figsize=[16, 6])
    ax1.plot(candles["begin"], candles["close"], color="red")
    ax2.plot(candles["begin"], candles["volume"], color="green")
    ax1.set_xlabel("time")
    ax1.set_ylabel("close price")
    ax2.set_xlabel("time")
    ax2.set_ylabel("volume")
    ax1.set_title("Candles plot ({0})".format(securityid))
    return fig, [ax1, ax2]
