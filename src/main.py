import sys
import csv
from pathlib import Path
from parsers import amex, tdbank, schwab, tdameritrade, ameriprise

def main():
    sys.path.append(str(Path(__file__).parent))
    root_dir=Path(__file__).parent.parent
    statements_path = Path(f"{root_dir}/input/statements")
    transaction_csv_path = Path(f"{root_dir}/input/transaction_csv")
    transactions_path = root_dir.joinpath(f"output/transactions.csv")
    deposits_path = root_dir.joinpath(f"output/deposits.csv")
    amex_credit_path = root_dir.joinpath(f"output/amex-credits.csv")
    brokerage_transactions_path = root_dir.joinpath(f"output/brokerage_transactions.csv")

    # Open the file in write mode
    with open(transactions_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Description', 'Amount', 'Bank Name', 'Account Holder', 'Account Number']])  # Consider adding 'Category', 'Tags', 'Account Nickname', 'Transaction Match' at the DB level    
        print(f"Transaction data CSV file created at: '{transactions_path}'.")
    with open(deposits_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Description', 'Amount', 'Bank Name', 'Account Holder', 'Account Number']])  # Consider adding 'Category', 'Tags', 'Account Nickname', 'Transaction Match' at the DB level
        print(f"Deposit data CSV file created at: '{deposits_path}'.")
    with open(amex_credit_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Description', 'Amount', 'Bank Name', 'Account Holder', 'Account Number']])  # Consider adding 'Category', 'Tags', 'Account Nickname', 'Transaction Match' at the DB level
        print(f"Credits data CSV file created at: '{amex_credit_path}'.")
    with open(brokerage_transactions_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Transaction Type', 'Symbol', 'Description', 'Quantity', 'Price', 'Amount', 'Brokerage Name', 'Account Number']])  # Consider adding 'Category', 'Tags', 'Account Nickname', 'Transaction Match' at the DB level
        print(f"Brokerage Transaction data CSV file created at: '{brokerage_transactions_path}'.")
    
    print('*'*100)
    print("Beginning Transaction CSV Parsing Process")
    print('*'*100)

    for csv_file in transaction_csv_path.glob('./tdbank/*.csv'):
        parsed_data = tdbank.parse_csv(csv_file)
        tdbank.write_csv(transactions_path, deposits_path, parsed_data.transaction_data, parsed_data.deposit_data)

    for csv_file in transaction_csv_path.glob('./amex/*.csv'):
        parsed_data = amex.parse_csv(csv_file)
        amex.write_csv(transactions_path, amex_credit_path, parsed_data.transaction_data, parsed_data.credit_data)

    print('*'*100)
    print("Beginning Bank Statement Parsing Process")
    print('*'*100)

    for pdf_file in statements_path.glob('./tdbank/*.pdf'):
        parsed_data = tdbank.parse_statement(pdf_file)
        tdbank.write_csv(transactions_path, deposits_path, parsed_data.transaction_data, parsed_data.deposit_data)

    for pdf_file in statements_path.glob('./amex/*.pdf'):
        parsed_data = amex.parse_statement(pdf_file)
        amex.write_csv(transactions_path, amex_credit_path, parsed_data.transaction_data, parsed_data.credit_data)

    print('*'*100)
    print("Beginning Brokerage Statement Parsing Process")
    print('*'*100)

    for pdf_file in statements_path.glob('./schwab/*.pdf'):
        parsed_data = schwab.parse_statement(pdf_file)
        schwab.write_csv(brokerage_transactions_path, parsed_data.transaction_data)

    for pdf_file in statements_path.glob('./tdameritrade/*.pdf'):
        parsed_data = tdameritrade.parse_statement(pdf_file)
        tdameritrade.write_csv(brokerage_transactions_path, parsed_data.transaction_data)

    print('*'*100)
    print("Beginning Brokerage CSV Parsing Process")
    print('*'*100)

    for csv_file in transaction_csv_path.glob('./schwab/*.csv'):
        parsed_data = schwab.parse_csv(csv_file)
        ameriprise.write_csv(brokerage_transactions_path, parsed_data.transaction_data)

    for csv_file in transaction_csv_path.glob('./ameriprise/*.csv'):
        parsed_data = ameriprise.parse_csv(csv_file)
        ameriprise.write_csv(brokerage_transactions_path, parsed_data.transaction_data)

if __name__ == "__main__":
    main()