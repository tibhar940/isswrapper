import matplotlib.pyplot as plt


def tradesplot(trades, securityid=None):
    fig, [ax1, ax2] = plt.subplots(2, 1, figsize=[16, 6])
    ax1.plot(trades['systime'], trades['price'], color='red')
    ax2.plot(trades['systime'], trades['quantity'], color='green')
    ax1.set_xlabel('time')
    ax1.set_ylabel('price')
    ax2.set_xlabel('time')
    ax2.set_ylabel('quantity')
    ax1.set_title('Trades plot ({0})'.format(securityid))
    return fig, [ax1, ax2]