import csv
import pdfplumber
from pathlib import Path
from collections import namedtuple

DATES=['01/', '02/', '03/', '04/', '05/', '06/', '07/', '08/', '09/', '10/', '11/', '12/']

Statement_Result = namedtuple('Statement_Result', ['transaction_data', 'credit_data'])

def parse_statement(pdf_file):
    print(f"Parsing transaction and credit data from AMEX statement located at: '{pdf_file}'.")
    # Setting up lists for transaction and credit data
    transactions = []
    credits = []
    # Used to manage application state. When the header of the credits table in the PDF is discovered, 'tracking_credits' will flip to true
    # and the following lines analyzed will be added to the credits list if they fit the expected format of a transaction entry
    screen_reader_optimized = False
    tracking_credits = False
    tracking_transactions = False
    ## Transaction data CSV headers
    # transaction_data = [['Date', 'Amount', 'Category', 'Description', 'Tags', 'Bank Name', 'Account Holder', 'Account Number', 'Account Nickname']]
    # credit_data = [['Date', 'Description', 'Amount', 'Category', 'Bank Name', 'Account Holder', 'Account Number', 'Account Nickname', 'Transaction Match']]    
    transaction_data = []
    credit_data = []    
    ## Complimentary Data to be Parsed
    bank_name = 'amex'
    account_holder = ''
    account_number = ''
    account_nickname = ''
    
    text = ''
    
    with pdfplumber.open(str(pdf_file)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    lines = text.split('\n')

    screen_reader_optimized = True if 'Screen Reader Optimized' in lines[1] else False 

    if screen_reader_optimized:
        for i in range(len(lines)):
            if "Prepared for" in lines[i]:
                account_holder = lines[i+1]
                account_number = lines[i+2].split('-')[-1]
                break
    
        for i in range(len(lines)):
            # print('screen optimized')
            # print(account_holder, ': ', account_number)
            # breakpoint()
            if lines[i] == "Credits Details":
                tracking_credits = True
            if lines[i] == "New Charges Details":
                tracking_transactions = True
            elif lines[i][0:3] in DATES and (tracking_transactions or tracking_credits):
                entry_split = lines[i].split(" ")
                date = entry_split[0]
                amount = entry_split[-1].replace("-", "").replace("$", "")
                description = entry_split[1:-4]
                description_2 = lines[i+1].split(" ")[0:-2]
                description_3 = lines[i+2].split(" ")[0:-1]
                description_2.extend(description_3)
                description.extend(description_2)
                entry = (" ").join([date]+description+[amount]) 
                if tracking_credits: credits.append(entry)
                if tracking_transactions: transactions.append(entry)
            elif lines[i].startswith('New Charges Summary') or lines[i].startswith('Fees'):
                tracking_credits = False
                tracking_transactions = False
    else:
        for i in range(len(lines)):
            if "Customer Care: " in lines[i]:
                text_split = lines[i].split(' ')
                while text_split[0] != 'Customer':
                    account_holder+=text_split.pop(0)
            elif "Account Ending" in lines[i]:
                account_number = lines[i].split('-')[1][0:5]
                break
        for i in range(len(lines)):
            # print('not screen optimized')
            # print(account_holder, ': ', account_number)
            # breakpoint()
            if lines[i] == "Credits Amount":
                tracking_credits = True
            if lines[i]=="Detail - denotes Pay Over Time and/or Cash Advance activity":
                tracking_transactions = True
            elif lines[i][0:3] in DATES and (tracking_transactions or tracking_credits):
                entry_split = lines[i].split(" ")
                entry_split[-1]= entry_split[-1].replace("-", "").replace("$", "")
                date = entry_split[0]
                # amount = entry_split[-1].replace("-", "").replace("$", "")
                # description = entry_split[1:-1]
                entry = (" ").join(entry_split) 
                if tracking_credits: credits.append(entry)
                if tracking_transactions: transactions.append(entry)
            elif lines[i].startswith('Fees') or lines[i].startswith("New Charges"):
                tracking_credits = False
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
        transaction_data.append([date, amount, category, description, tags, bank_name, account_holder, account_number, account_nickname])

    # Refine credit data and write to CSV
    for credit in credits:
        credit_split = credit.split(' ')
        year  = '20' + credit_split[0].split('/')[-1]
        date = credit_split.pop(0).replace("*","")[:-2] + year
        amount = credit_split.pop().replace("⧫", "")
        description = " ".join(credit_split)
        category = ''
        transaction_match = ''
        credit_data.append([date, description, amount, category, bank_name, account_holder, account_number, account_nickname, transaction_match])

    # pdf_file.rename(f"C:\\Users\\ogord\dev\\pocket-watcher\\processed_statements\\{pdf_file.parts[-2]}\\{pdf_file.parts[-1]}")

    result = Statement_Result(transaction_data=transaction_data, credit_data=credit_data)

    return result

def write_csv(transactions_csv_file_path, credits_csv_file_path, transaction_data, credit_data):
    # Open the file in write mode
    with open(transactions_csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(transaction_data)
    # Open the file in write mode
    with open(credits_csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(credit_data)