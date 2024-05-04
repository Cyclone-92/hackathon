import optimization as opt

def main():
    while True:
        opt.adjust_energy_allocations()
        print("/n")
        print(f"Total kwH you didnt have to pay for: {opt.total_kwH_covered}")
        print("/n")

if __name__ == '__main__':
    main()
