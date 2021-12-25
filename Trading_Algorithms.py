"""
Michele Martino
TRADING ALGORITHMS
"""


# I have included the test data function since the autograder asked me to.
# However, it is not used in this Milestone
# Function assigning right column to choose in file
def col_to_y(col):
    columns = ["date", "open", "high", "low", "close", "adj_close", "volume"]
    for i in range(len(columns)):
        if columns[i] == col:
            return i


# function 1
def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

    Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.

        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.

             The string arguments MUST be LOWERCASE!

        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.

    Returns:
        A value selected for the stock on some particular day, in some
        column col. The returned value *must* be of the appropriate type,
        such as float, int or str.
    """
    # reads file
    data = open(filename, 'r')
    # creates erray of lines
    lines = data.readlines()
    y = col_to_y(col)
    # split deignated row in columns
    rowday = lines[day].split(",")
    if y == 0:
        # return date as a string
        return str(rowday[y])
    elif y == 6:
        # return volume as an int
        return int(rowday[y])
    else:
        # return anything else as a float
        return float(rowday[y])


def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.

       Args:
           funds: An account balance, a float;\
           it is a value of how much money you have,
                  currently.

           stocks: An int, representing the number of stock you currently own.

           qty: An int, representing how many stock you wish to buy or sell.

           price: An float reflecting a price of a single stock.

           buy: This option parameter, if set to true, will initiate a buy.

           sell: This option parameter, if set to true, will initiate a sell.

       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.

           Error condition #1: If the `buy` and `sell` keyword parameters
           are both set to true, or both false. You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.

           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.
    """
    # conditional statement for buying/selling
    if buy is True and sell is False:
        newfunds = (funds - ((price)*qty))
        # raises error for insufficient founds
        if newfunds < 0:
            raise ValueError(f"Insufficient funds to purchase \
{qty} stock at ${price:0.2f} each!")
        newstocks = (stocks + qty)
        return newfunds, newstocks
    elif buy is False and sell is True:
        newfunds = (funds + ((price)*qty))
        newstocks = (stocks - qty)
        # raises error for insufficient stocks owned
        if newstocks < 0:
            raise ValueError(f"Insufficient stock owned to sell {qty} stocks!")
        return newfunds, newstocks
    else:
        # riases error if transaction is ambiguous
        raise ValueError("Ambiguous transaction! \
Can't determine whether to buy or sell!")


# ALGORITHM 1: MOVING AVERAGE
def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to
    make decisions using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower
      than the moving average.
    - You must sell shares if the current day price is 5%, or more, higher,
      than the moving average.
    - You must buy, or sell 10 stocks, or less per transaction.
    - You are free to choose which column of stock data to use (open, close,
      low, high, etc)
    - When your algorithm reaches the last day of data, have it sell all
      remaining stock. Your function will return the number of stocks you
      own (should be zero, at this point), and your cash balance.
    - Choose any stock price column you wish for a particular day you use
      (whether it's the current day's "open", "close", "high", etc)

    Args:
        A filename, as a string.

    Returns:
        Note: You *must* sell all your stock before returning.
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """
    # read file
    data = open(filename, 'r')
    # creates erray of lines
    lines = data.readlines()
    # calculate first avg.
    first_20_days_average = 0
    for i in range(1, 22):
        curr = lines[i].split(',')
        first_20_days_average += float(curr[1])
    first_20_days_average = first_20_days_average / 20
    cash_balance = 1000
    stocks_owned = 0
    twenty_avg = first_20_days_average
    # iterate trade decisision based on avg.
    for i in range(22, len(lines)):
        curr = lines[i].split(',')
        if float(curr[1]) <= 0.95*twenty_avg:
            try:
                cash_balance, stocks_owned = \
                              transact(cash_balance,
                                       stocks_owned, 5,
                                       float(curr[1]),
                                       buy=True, sell=False)
            except ValueError:
                pass
        elif float(curr[1]) >= 1.05*twenty_avg:
            try:
                cash_balance, stocks_owned = \
                              transact(cash_balance,
                                       stocks_owned, 5,
                                       float(curr[1]),
                                       buy=False, sell=True)
            except ValueError:
                pass
        # recalculate avg.
        remove_from_line = lines[i-20].split(',')
        twenty_avg -= (float(remove_from_line[1]))/20
        twenty_avg += (float(curr[1]))/20
    # sell all stocks in the end
    last_line = lines[len(lines)-1].split(',')
    cash_balance, stocks_owned = transact(cash_balance, stocks_owned,
                                          stocks_owned, float(last_line[1]),
                                          buy=False, sell=True)
    # Last thing to do, return two values: one for the number of stocks you end up
    # owning after the simulation, and the amount of money you have after the simulation.
    # Remember, all your stocks should be sold at the end!
    return stocks_owned, cash_balance

#ALGORITHM 2: PERSONALIZED ALGORITHM
def alg_mine(filename):
    """This function implements the student's custom trading algorithm.

    Using the CSV stock data that should be loaded into your program, use
    that data to make decisions using your own custome trading algorithm.

    Also, any bookkeeping setup in Milestone I should be called/used here.

    Args:
        A filename, as a string.

    Algorithm:
    The algorithm does the following:
    - It starts trading on day 21.

    - Calculates the "local" trend of the last 5 days. The trend is calculated
    by obtaining the change in price per day (discrete derivative) on each of
    the 5 days and taking a weighted average of the changes in price with
    respect to the volumes(stocks traded) per day. The weight justification
    is in the fact that changes in price are more important when more stocks
    are traded as this is an indicator of a stronger trend. After this, the
    "local trend" is multiplied by a coefficient that is the ratio of the toal
    volumes of the last 5 days over the total volume of the last 20 days.
    This coefficient is an indicator of how
    impacting are the 5 days (local period) with respect to the broader period
    of the 20 days which are taken into consideration for evaluating the
    decision of selling or buying.
    The local trend times this coeffiecient (strength factor) is what is
    analysed in order to take the decision of buying or selling.

    - If the strenght factor is BIGGER than 0 (corresponding to positive
    derivative), then the price is likely to increase the day after.
    This means that I want to BUY as, the day after, what I bought the
    previous day will have increased in trading value (price).
    Conversely, if the strenght factor is SMALLER than 0, I want to sell,
    since the next day the price is likely to be smaller and then I
    prefer to sell in the current day for an higher income.

    - In the first 15 days of trading, the algorithm always sells\buy 5
    stocks.

    - The algorithm stores the strenght factors day by day after starting
    trading. After 15 days of trading, then, the algorithm uses the previous
    strenght factors, to decide how many stocks to trade based on the
    knowledge of the strenght factors of the last 15 days.

    - The algorithm decides to sell or buy an amount of stocks that is equal
    to rounding to the closest integer to the percentage difference between
    the current day strength factor and the average of the strenght factors
    in the previous 15 days. If this difference is big, this means that the
    price is expected to increase\decrease by a lot in the next day.
    Therefore, the algorithm decides to capitalize the trading by buying\
    selling more.

    - At the end, the algorithm sells everything

    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """

    # read file
    data = open(filename, 'r')
    # creates erray of lines
    lines = data.readlines()

    # Create list storing volumes of first 20 days
    Vols = []
    for i in range(1, 22):
        curr = lines[i].split(',')
        Vols.append(float(curr[6]))
    # Creates list storing change in price between consecutive days
    # Uses data from the last 5 days before day 21
    # Prices are from the "Open" column
    DeltaP = []
    for i in range(17, 22):
        curr = lines[i].split(',')
        currM1 = lines[i-1].split(',')
        DeltaP.append((float(curr[1])-float(currM1[1])))

    cash_balance = 1000
    stocks_owned = 0
    # initialize the variable that later is used
    # to store the average of the strength factors of the
    # first 15 days of trading
    strength_avg = 0
    # empty list for storing strength factors
    strength_list = []
    # First 15 days of trading, starting from day 21
    for i in range(22, 37):
        volDP = 0
        vSum20 = 0
        vSum5 = 0
        # Calculates sum of voulumes of first 20 days
        for v in Vols:
            vSum20 += v
        # Calculates sum of last 5 days before starting trading
        for v in Vols[:-5]:
            vSum5 += v
        # Calculates strenght factor and stores it in the list
        for j in range(0, 5):
            volDP += Vols[j] * DeltaP[j]
        volDP = float(volDP / vSum5)
        k = float(vSum5 / vSum20)
        strength_factor = k * volDP
        strength_list.append(strength_factor)
        # Dcision to sell or buy using transact function
        # Uses always 5 stocks
        if float(strength_factor) >= 0:
            try:
                cash_balance, stocks_owned = \
                              transact(cash_balance,
                                       stocks_owned, 5,
                                       float(curr[1]),
                                       buy=True, sell=False)
            except ValueError:
                pass
        elif float(strength_factor) < 0:
            try:
                cash_balance, stocks_owned = \
                              transact(cash_balance,
                                       stocks_owned, 5,
                                       float(curr[1]),
                                       buy=False, sell=True)
            except ValueError:
                pass
        curr = lines[i].split(',')
        # update the list of volumes and changes in price
        # The resulting lists are always updated to the last
        # 20 days for volumes and to the last 5 days for the
        # changes in price
        del Vols[0]
        Vols.append(float(curr[6]))
        del DeltaP[0]
        DeltaP.append(float(curr[1]))

    # Trading after the first 15 days of trading
    # Now the algorithm can improve its decisions
    # by deciding how much to buy or sell using the
    # knowledge of the strenght factors of the first
    # 15 days of trading
    for i in range(37, len(lines)):
        # same as first 15 days of trading
        volDP = 0
        vSum20 = 0
        vSum5 = 0
        sAvg = 0
        for v in Vols:
            vSum20 += v
        for v in Vols[:-5]:
            vSum5 += v
        for j in range(0, 5):
            volDP += Vols[j] * DeltaP[j]
        volDP = float(volDP / vSum5)
        k = float(vSum5 / vSum20)
        strength_factor = k * volDP
        for s in strength_list:
            sAvg += s
        sAvg = float(sAvg / 15)
        strength_avg = float((strength_avg * (i - 22) + strength_factor) / (i - 21))
        if float(strength_factor) >= 0:
            # Calculates how many stocks to trade
            # This is the improvement in decision after
            # the first 15 days of trading
            nstocks = int(100*abs(strength_factor-sAvg)/sAvg)
            try:
                cash_balance, stocks_owned = \
                              transact(cash_balance,
                                       stocks_owned, nstocks,
                                       float(curr[1]),
                                       buy=True, sell=False)
            except ValueError:
                pass
        elif float(strength_factor) < 0:
            nstocks = int(100*abs(sAvg-strength_factor)/sAvg)
            try:
                cash_balance, stocks_owned = \
                              transact(cash_balance,
                                       stocks_owned, nstocks,
                                       float(curr[1]),
                                       buy=False, sell=True)
            except ValueError:
                pass
        # Updates lists of volumes and changes in price
        # like in the first 15 days of trading
        # Additionally, the list of the strenght factors
        # is updated to the last 15 days
        curr = lines[i].split(',')
        del Vols[0]
        Vols.append(float(curr[6]))
        del DeltaP[0]
        DeltaP.append(float(curr[1]))
        del strength_list[0]
        strength_list.append(strength_factor)
    # In the end, sells everything
    last_line = lines[len(lines)-1].split(',')
    cash_balance, stocks_owned = transact(cash_balance, stocks_owned,
                                          stocks_owned, float(last_line[1]),
                                          buy=False, sell=True)
    # Last thing to do, return two values: one for the number of stocks you end up
    # owning after the simulation, and the amount of money you have after
    # the simulation.
    # Remember, all your stocks should be sold at the end!
    return stocks_owned, cash_balance


# Don't forget the required "__main__" check!
def main():
    # My testing will use AAPL.csv or MSFT.csv
    filename = input("Enter a filename for stock data (CSV format): ")

    # Call your moving average algorithm, with the filename to open.
    alg1_stocks, alg1_balance = alg_moving_average(filename)

    # Print results of the moving average algorithm, returned above:
    print("The results are...", alg1_stocks, alg1_balance)

    # Now, call your custom algorithm!
    alg2_stocks, alg2_balance = alg_mine(filename)

    # Print results of your algorithm, returned above:
    print("The results are...", alg2_stocks, alg2_balance)


if __name__ == '__main__':
    main()
