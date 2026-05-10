stock = float(input("Enter target price of stock ")) #Use the period low price for Target 
contract = float(input("Enter lenth of contract ")) #Contract should be 3-6 months less than experation 
current_stock_price = float(input("Enter current price of stock ")) #The current price of the stock today

strike_price = (stock / contract) * .9
strike_price = round(strike_price)
contract_price = strike_price + current_stock_price

print(f"Strike price is {contract_price}")