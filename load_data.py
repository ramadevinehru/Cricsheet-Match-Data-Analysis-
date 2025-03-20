import mysql.connector
import pandas as pd

DB_CONFIG = {
    "host": "localhost",  
    "user": "root",
    "password": "123456789",
    "database": "cricket_db",  
}

TABLES = {
    "tests_matches": "E:/cricket/tests_matches.csv",
    "odi_matches": "E:/cricket/odis_matches.csv",
    "t20_matches": "E:/cricket/t20s_matches.csv",
    "ipl_matches": "E:/cricket/ipl_matches.csv"
}

BATCH_SIZE = 1000

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS {table_name} (
    match_type VARCHAR(10),
    season VARCHAR(20),
    city VARCHAR(50),
    venue VARCHAR(100),
    toss_winner VARCHAR(50),
    toss_decision VARCHAR(10),
    winner VARCHAR(50),
    player_of_match VARCHAR(50),
    teams VARCHAR(100),
    team VARCHAR(50),
    `over` INT,
    batter VARCHAR(50),
    bowler VARCHAR(50),
    non_striker VARCHAR(50),
    runs_batter INT,
    runs_extras INT,
    runs_total INT,
    wicket VARCHAR(50)
);
"""

def create_table(cursor, table_name):
    cursor.execute(TABLE_SCHEMA.format(table_name=table_name))
    print(f"Table `{table_name}` ensured.")

def insert_records_in_batches(cursor, table_name, data):
    sql = f"""
    INSERT INTO {table_name} (
        match_type, season, city, venue, toss_winner, toss_decision, winner, 
        player_of_match, teams, team, `over`, batter, bowler, non_striker, 
        runs_batter, runs_extras, runs_total, wicket
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for batch_start in range(0, len(data), BATCH_SIZE):
        batch = data[batch_start : batch_start + BATCH_SIZE]
        cursor.executemany(sql, batch)
        print(f"Inserted {len(batch)} records into `{table_name}`...")

def main():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        conn.rollback()

        for table_name, csv_file in TABLES.items():
            print(f"\n Processing `{table_name}` from `{csv_file}`")
            create_table(cursor, table_name)
            try:
                df = pd.read_csv(csv_file, dtype={"season": str}, low_memory=False)
                print(f"CSV `{csv_file}` loaded successfully!")
            except Exception as e:
                print(f"Error loading `{csv_file}`: {e}")
                continue
            df = df.where(pd.notnull(df), None)
            records = [tuple(row) for row in df.itertuples(index=False, name=None)]

            if records:
                insert_records_in_batches(cursor, table_name, records)
            else:
                print(f"No data found in `{csv_file}`.")
        conn.commit()
        print("All data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
        print("🔌 MySQL connection closed.")

if __name__ == "__main__":
    main()
