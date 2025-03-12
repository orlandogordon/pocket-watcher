import sys
from pathlib import Path
from td_bank.statement_parser import TdStatementParser

sys.path.append(str(Path(__file__).parent))

td_parser = TdStatementParser()
td_parser.parse_pdf()
td_parser.format_data()
td_parser.write_data()