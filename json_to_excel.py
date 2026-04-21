import json
import pandas as pd
from datetime import datetime

# Read JSON data
with open('diagram.json', 'r') as f:
    data = json.load(f)

# Check if data is a list (sensor data) or dict (circuit diagram)
if isinstance(data, dict) and 'version' in data:
    print("❌ diagram.json contains circuit diagram, not sensor data.")
    print("   Run collect_data.py first to collect sensor readings.")
elif isinstance(data, list) and len(data) == 0:
    print("❌ No data collected yet. Run collect_data.py to start collecting sensor data.")
elif isinstance(data, list):
    # Fill missing values with None to handle inconsistent keys
    df = pd.DataFrame(data).fillna('')
    
    # Convert timestamp to readable format
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Save to Excel
    excel_file = 'health_data.xlsx'
    df.to_excel(excel_file, index=False, sheet_name='Health Monitoring')
    
    print(f"✓ Data converted to {excel_file}")
    print(f"✓ Total records: {len(df)}")
    print(f"\nPreview:\n{df.head()}")
else:
    print("❌ Unexpected data format in diagram.json")
