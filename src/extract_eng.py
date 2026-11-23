import duckdb
import pandas as pd
from pathlib import Path

RAW_DATA = Path(__file__).resolve().parent.parent / 'data' / 'raw' / 'steam_reviews.csv'
DATA = Path(__file__).resolve().parent.parent / 'data' / 'main'
DATA.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

fix = con.execute(f"""
    SELECT *
    FROM read_csv('{RAW_DATA}', max_line_size = 10000000)
    WHERE language = 'english'
""").fetchdf()

fix.to_csv(DATA / 'cutdown.csv', index=False)
con.close()
