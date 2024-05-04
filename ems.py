import time

import optimization as opt
import setup as set

def main():
    user_input = input("Please enter a value: ")
    time.sleep(2)
    # Pass the user input to the setup function
    id = set.setup(user_input)

    while True:
        opt.adjust_energy_allocations(id)
        print("/n")
        print(f"Total kwH you didnt have to pay for: {opt.total_kwH_covered}")
        print("/n")

if __name__ == '__main__':
    main()
