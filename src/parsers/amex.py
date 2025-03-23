import csv
import pdfplumber
from pathlib import Path
from collections import namedtuple

DATES=['01/', '02/', '03/', '04/', '05/', '06/', '07/', '08/', '09/', '10/', '11/', '12/']

Statement_Result = namedtuple('Statement_Result', ['transaction_data', 'deposit_data'])

def parse_statement(pdf_file):
    # Setting up lists for transaction and deposit data
    transactions = []
    deposits = []
    # Used to manage application state. When the header of the deposits table in the PDF is discovered, 'tracking_depositis' will flip to true
    # and the following lines analyzed will be added to the deposits list if they fit the expected format of a transaction entry
    tracking_deposits = False
    tracking_transactions = False
    ## Transaction data CSV headers
    # transaction_data = [['Date', 'Amount', 'Category', 'Description', 'Tags']]
    # deposit_data = [['Date', 'Description', 'Amount']]    
    transaction_data = []
    deposit_data = []    
    
    text = ''
    
    with pdfplumber.open(str(pdf_file)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    lines = text.split('\n')
   
    for i in range(len(lines)):
        if lines[i] == "Credits Details":
            tracking_deposits = True
        if lines[i] == "New Charges Details":
            tracking_transactions = True
        elif lines[i][0:3] in DATES and (tracking_transactions or tracking_deposits):
            breakpoint()
            entry_split = lines[i].split(" ")
            date = entry_split[0]
            amount = entry_split[-1].replace("-", "").replace("$", "")
            description = entry_split[1:-4]
            description_2 = lines[i+1].split(" ")[0:-2]
            description_3 = lines[i+2].split(" ")[0:-1]
            description_2.extend(description_3)
            description.extend(description_2)
            entry = (" ").join([date]+description+[amount]) 
            if tracking_deposits: deposits.append(entry)
            if tracking_transactions: transactions.append(entry)
        elif lines[i].startswith('New Charges Summary') or lines[i].startswith('Fees'):
            tracking_deposits = False
            tracking_transactions = False

    for i in range(len(lines)):
        if lines[i] == "Credits Amount":
            tracking_deposits = True
        if lines[i]=="Detail - denotes Pay Over Time and/or Cash Advance activity":
            tracking_transactions = True
        elif lines[i][0:3] in DATES and (tracking_transactions or tracking_deposits):
            entry_split = lines[i].split(" ")
            entry_split[-1]= entry_split[-1].replace("-", "").replace("$", "")
            date = entry_split[0]
            # amount = entry_split[-1].replace("-", "").replace("$", "")
            # description = entry_split[1:-1]
            entry = (" ").join(entry_split) 
            if tracking_deposits: deposits.append(entry)
            if tracking_transactions: transactions.append(entry)
        elif lines[i].startswith('Fees') or lines[i].startswith("New Charges"):
            tracking_deposits = False
            tracking_transactions = False

    # Refine transaction data and write to CSV
    for transaction in transactions:
        transaction_split = transaction.split(' ')
        year  = '20' + transaction_split[0].split('/')[-1]
        date = transaction_split.pop(0).replace("*","")[:-2] + year
        amount = transaction_split.pop()
        description = " ".join(transaction_split)
        # description = transaction_split.pop()
        category = ''
        tags = ''
        transaction_data.append([date, amount, category, description, tags])

    # Refine deposit data and write to CSV
    for deposit in deposits:
        deposit_split = deposit.split(' ')
        year  = '20' + deposit_split[0].split('/')[-1]
        date = deposit_split.pop(0).replace("*","")[:-2] + year
        amount = deposit_split.pop()
        description = " ".join(deposit_split)
        deposit_data.append([date, description, amount])

    # pdf_file.rename(f"C:\\Users\\ogord\dev\\pocket-watcher\\processed_statements\\{pdf_file.parts[-2]}\\{pdf_file.parts[-1]}")

    result = Statement_Result(transaction_data=transaction_data, deposit_data=deposit_data)

    return result

def write_csv(transactions_csv_file_path, deposits_csv_file_path, transaction_data, deposit_data):
    # Open the file in write mode
    with open(transactions_csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(transaction_data)

    print(f"Transaction data CSV file created at: '{transactions_csv_file_path}'.")

    # Open the file in write mode
    with open(deposits_csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(deposit_data)

    print(f"Deposit data CSV file created at: '{deposits_csv_file_path}'.")