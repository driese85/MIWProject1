# import libraries
import sqlite3
import pandas as pd
import logging

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn

# Logging config
FORMAT = '%(asctime)s | %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# make connection to sqlite db
logging.info("Creating connection to sqlite database...")
conn = create_connection('build/data/db.sqlite3')

# if connection has been succesfully established start extraction and transformation steps
if conn is not None:

    logging.info("Retrieving data from database...")

    # with active connection read database into pandas DataFrame using SQL statement
    df = pd.read_sql('SELECT * FROM rest_api_netlify', con=conn)
    
    logging.info("Removing duplicates...")
    # remove duplicates
    df = df[~df.duplicated()]

    logging.info("Dropping rows with missing data...")
    # drop rows with missing data
    df = df.dropna()

    logging.info("Adding bmi as new future...")
    # Adding bmi as new feature [bmi = mass / length^2]
    df['bmi'] = round(df['mass'] / (df['length']/100)**2,1)

    # reorder columns to put lifespan at the end and get rid of "id"-column
    df_cleaned = df.reindex(columns=['genetic', 'length', 'mass', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'lifespan'])

    # Calculating Interquartile Range [1.5] to remove mathematical outliers
    Q1 = df_cleaned.quantile(0.25)
    Q3 = df_cleaned.quantile(0.75)
    IQR = Q3 - Q1
    df_iqr_cleaned = df_cleaned[~((df_cleaned < (Q1 - 1.5 * IQR)) |(df_cleaned > (Q3 + 1.5 * IQR))).any(axis=1)]

    logging.info("Saving cleaned data to sqlite3 and csv files...")
    # save dataframes to sqlite3 table, replace data if table already exists
    df_cleaned.to_sql('data_cleaned', con=conn, index=False, if_exists='replace')
    df_iqr_cleaned.to_sql('data_iqr_cleaned', con=conn, index=False, if_exists='replace')

    # save to csv file
    df_cleaned.to_csv('build/data/data_cleaned.csv', index=False)
    df_iqr_cleaned.to_csv('build/data/data_iqr_cleaned.csv', index=False)

    conn.close()
    
# if connections cannot be established, print message to user
else:
    logging.error("Error! Cannot create the database connection.")

