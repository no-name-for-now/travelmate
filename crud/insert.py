import pandas as pd
from sqlalchemy import create_engine

# Path to your CSV file

CSV_FILE = 'data.csv'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(CSV_FILE)
df = df[['city','city_ascii','country','iso2','iso3','lat','lng','population']]

# Create a SQLAlchemy engine to connect to the PostgreSQL database
engine = create_engine('postgresql://myuser:mypassword@localhost/mydatabase')

try:
    # Use the to_sql method to insert the DataFrame into the database table
    df.to_sql('world_cities', engine, if_exists='append', index=False)

    print(f"Data from CSV file inserted into world_cities successfully.")

except Exception as e:
    print(f"Error: {str(e)}")





