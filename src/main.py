import sys
import csv
from pathlib import Path
from parsers import amex, tdbank

def main():
    sys.path.append(str(Path(__file__).parent))
    root_dir=Path(__file__).parent.parent
    statements_path = Path(f"{root_dir}/input/statements")
    transaction_csv_path = Path(f"{root_dir}/input/transaction_csv")
    transactions_path = root_dir.joinpath(f"output/transactions.csv")
    deposits_path = root_dir.joinpath(f"output/deposits.csv")
    amex_credit_path = root_dir.joinpath(f"output/amex-credits.csv")

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

    # for pdf_file in statements_path.glob('./schwab/*.pdf'):
    #     transactions_csv_file_path = root_dir.joinpath(f"transactions/schwab-{pdf_file.name.split(".")[0]}.csv")
    #     deposits_csv_file_path = root_dir.joinpath(f"deposits/schwab-{pdf_file.name.split(".")[0]}.csv")
    #     parsed_data = tdbank.parse_statement(pdf_file)
    #     schwab.write_csv(transactions_csv_file_path, deposits_csv_file_path, parsed_data.transaction_data, parsed_data.credit_data)


if __name__ == "__main__":
    main()