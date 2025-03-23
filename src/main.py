import sys
import csv
from pathlib import Path
from parsers import amex, tdbank

def main():
    sys.path.append(str(Path(__file__).parent))
    root_dir=Path(__file__).parent.parent
    statements_path = Path(f"{root_dir}/input/statements")
    transactions_path = root_dir.joinpath(f"output/transactions.csv")
    deposits_path = root_dir.joinpath(f"output/deposits.csv")
    amex_credit_path = root_dir.joinpath(f"output/amex-credits.csv")

    print("Beginning Bank Statement Parsing Process")

    # Open the file in write mode
    with open(transactions_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Amount', 'Category', 'Description', 'Tags']])
    with open(deposits_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Description', 'Amount']])
    with open(amex_credit_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([['Date', 'Description', 'Amount']])

    for pdf_file in statements_path.glob('./tdbank/*.pdf'):
        # transactions_csv_file_path = root_dir.joinpath(f"output/tdbank-transactions-{pdf_file.name.split(".")[0]}.csv")
        # deposits_csv_file_path = root_dir.joinpath(f"output/tdbank-deposits-{pdf_file.name.split(".")[0]}.csv")
        parsed_data = tdbank.parse_statement(pdf_file)
        tdbank.write_csv(transactions_path, deposits_path, parsed_data.transaction_data, parsed_data.deposit_data)

    for pdf_file in statements_path.glob('./amex/*.pdf'):
        # transactions_csv_file_path = root_dir.joinpath(f"output/amex-transactions-{pdf_file.name.split(".")[0]}.csv")
        # deposits_csv_file_path = root_dir.joinpath(f"output/amex-credits-{pdf_file.name.split(".")[0]}.csv")
        parsed_data = amex.parse_statement(pdf_file)
        amex.write_csv(transactions_path, amex_credit_path, parsed_data.transaction_data, parsed_data.deposit_data)

    for pdf_file in statements_path.glob('./schwab/*.pdf'):
        transactions_csv_file_path = root_dir.joinpath(f"transactions/schwab-{pdf_file.name.split(".")[0]}.csv")
        deposits_csv_file_path = root_dir.joinpath(f"deposits/schwab-{pdf_file.name.split(".")[0]}.csv")
        parsed_data = tdbank.parse_statement(pdf_file)
        tdbank.write_csv(transactions_csv_file_path, deposits_csv_file_path, parsed_data.transaction_data, parsed_data.deposit_data)


if __name__ == "__main__":
    main()