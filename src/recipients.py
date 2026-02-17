import pandas as pd
from .config import RECIPIENTS_FILE, DATA_DIR

def load_recipients():
    """Load recipients from Excel or CSV file."""
    if not RECIPIENTS_FILE:
        raise FileNotFoundError(
            f"No recipients file found in {DATA_DIR}\n"
            "Please create one of these files with columns: email, company_name, employee_name\n"
            "  - recipients.xlsx\n"
            "  - recipients.csv\n"
            "  - recipients_example.xlsx\n"
            "  - recipients_example.csv"
        )
    
    # Load based on file extension
    if RECIPIENTS_FILE.suffix == '.csv':
        df = pd.read_csv(RECIPIENTS_FILE)
    else:
        df = pd.read_excel(RECIPIENTS_FILE)
    
    required_columns = ['email', 'company_name']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Drop rows with missing emails
    df = df.dropna(subset=['email'])
    
    # Ensure employee_name exists (optional column)
    if 'employee_name' not in df.columns:
        df['employee_name'] = ''
    
    # Convert NaN values to empty strings for proper string handling
    df = df.fillna('')
    
    return df.to_dict('records')
