import random
import sys
import tty
import termios

def flip():
    return "heads" if random.randint(1, 1000) > 500 else "tails"

def get_keypress():
    """Reads a single keypress (cross-platform for Unix-like systems)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

while True:
    print("\nPress any key to flip coins, or press ESC to exit.")
    key = get_keypress()

    if ord(key) == 27:  # ESC key ASCII
        print("👋 Peace out!")
        break

    print("How many coins do you want to flip?")
    user_input = input().strip()

    try:
        count = int(user_input)
        headcount = 0
        tailcount = 0

        for _ in range(count):
            result = flip()
            if result == "heads":
                headcount += 1
            else:
                tailcount += 1

        # Calculate percentages
        head_percent = (headcount / count) * 100
        tail_percent = (tailcount / count) * 100

        print("\n--- Summary ---")
        print(f"Total flips: {count:,}")
        print(f"Heads: {headcount:,} ({head_percent:.2f}%)")
        print(f"Tails: {tailcount:,} ({tail_percent:.2f}%)")

    except ValueError:
        if user_input.lower() == "one":
            print(f"\nYou got: {flip().capitalize()}")
        else:
            print("bruh, type a number or 'one'.")