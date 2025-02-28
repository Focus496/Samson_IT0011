import csv

def load_exchange_rates(filename):
    exchange_rates = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                currency, rate = row
                exchange_rates[currency.strip()] = float(rate)
    except FileNotFoundError:
        print("Error: The file currency.csv was not found.")
        exit()
    except ValueError:
        print("Error: Invalid data in the file.")
        exit()
    return exchange_rates

def convert_currency(usd_amount, target_currency, exchange_rates):
    if target_currency in exchange_rates:
        converted_amount = usd_amount * exchange_rates[target_currency]
        return converted_amount
    else:
        print("Error: Currency not found in exchange rates.")
        exit()

if __name__ == "__main__":
    exchange_rates = load_exchange_rates("currency.csv")
    
    usd_amount = float(input("How much dollar do you have? "))
    target_currency = input("What currency do you want to have? ").strip().upper()
    
    converted_amount = convert_currency(usd_amount, target_currency, exchange_rates)
    
    print(f"\nDollar: {usd_amount:.2f} USD")
    print(f"{target_currency}: {converted_amount:.6f}")
