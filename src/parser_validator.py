import sys
import csv
import pandas as pd
from pathlib import Path

def main():
    sys.path.append(str(Path(__file__).parent))
    root_dir=Path(__file__).parent.parent
    transactions_path = root_dir.joinpath(f"output/transactions.csv")
    transactions_path_legacy = root_dir.joinpath(f"output/transactions_legacy.csv")
    deposits_path = root_dir.joinpath(f"output/deposits.csv")
    credits_path = root_dir.joinpath(f"output/credit-card-credits.csv")
    brokerage_transactions_path = root_dir.joinpath(f"output/brokerage_transactions.csv")
    retirement_balance_path = root_dir.joinpath(f"output/retirement_balance.csv")
    retirement_transactions_path = root_dir.joinpath(f"output/retirement_transactions.csv")

    # List of specific CSV files to concatenate
    csv_files = [transactions_path_legacy, deposits_path]

    # Read and concatenate the files
    legacy_dataframes = [pd.read_csv(file)[["Date", "Amount"]] for file in csv_files]
    legacy_parser_dataframe = pd.concat(legacy_dataframes, ignore_index=True).sort_values(by='Amount', ascending=True).reset_index(drop=True)
    table_parser_dataframe = pd.read_csv(transactions_path)[["Date", "Amount"]].sort_values(by='Amount', ascending=True).reset_index(drop=True)
    print(legacy_parser_dataframe)
    print(table_parser_dataframe)
    print(legacy_parser_dataframe.equals(table_parser_dataframe))
    breakpoint()


if __name__ == "__main__":
    main()