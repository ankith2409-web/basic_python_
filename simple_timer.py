import time

def countdown_timer(seconds):
    print(f"Starting countdown for {seconds} seconds...")
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    
    print("\nTime's up!")

if __name__ == "__main__":
    try:
        t = int(input("Enter the time in seconds: "))
        countdown_timer(t)
    except ValueError:
        print("Please enter a valid integer.")
