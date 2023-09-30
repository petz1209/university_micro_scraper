from scraper import main
FLAT_CHOICE = {"h": "house", "a": "apartment"}
CONTRACT_CHOICE = {"b": "buy", "r": "rent"}

def cli():
    print("-------------------------------------------------------")
    print("SCRAPER CLI")
    print("-------------------------------------------------------")
    print()
    flat_choice = input("do you want to filter for flat type? ([h] house [a] apartment [x] all): ")
    contract_choice = input("do you want to filter for contract type? ([b] buy [r] rent [x] all): ")
    page_count = int(input("How many pages per region do you want (expects number): "))
    f_choice = FLAT_CHOICE.get(flat_choice.lower())
    c_choice = CONTRACT_CHOICE.get(contract_choice.lower())
    main(f_choice, c_choice, page_count)


if __name__ == '__main__':
    cli()
