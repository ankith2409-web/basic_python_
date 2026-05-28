# Variables & Data Types
product = "Laptop"     # str
price = 75000          # int
discount = 0.10        # float
in_stock = True        # bool
sizes = [13, 14, 15]   # list

# Apply discount
final_price = price - (price * discount)

# if/elif/else
if final_price > 80000:
    tag = "Premium"
elif final_price > 50000:
    tag = "Mid-range"
else:
    tag = "Budget"

print(f"{product} | Price: ₹{final_price} | Category: {tag}")

# for loop with index
print("Available sizes:")
for i, size in enumerate(sizes):
    print(f"  {i+1}. {size} inch")

# while loop
stock = 3
while stock > 0:
    print(f"Units left: {stock}")
    stock -= 1

print("Out of stock!" if not in_stock else "Still available") 
