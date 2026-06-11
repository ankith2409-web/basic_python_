def main():
    # Pre-defined exchange rates based on USD
    rates = {
        'USD': 1.0,
        'EUR': 0.91,
        'GBP': 0.79,
        'INR': 83.2,
        'JPY': 149.5
    }

    print("--- Simple Currency Converter ---")
    print("Available currencies: USD, EUR, GBP, INR, JPY")
    
    base_currency = input("Convert from (e.g., USD): ").upper()
    target_currency = input("Convert to (e.g., EUR): ").upper()

    if base_currency not in rates or target_currency not in rates:
        print("Invalid currency code selected.")
        return

    try:
        amount = float(input(f"Enter amount in {base_currency}: "))
    except ValueError:
        print("Invalid amount entered. Please enter a number.")
        return

    # Convert to USD first (as base), then to target currency
    amount_in_usd = amount / rates[base_currency]
    converted_amount = amount_in_usd * rates[target_currency]

    print(f"\n{amount:.2f} {base_currency} is equal to {converted_amount:.2f} {target_currency}")

if __name__ == "__main__":
    main()
