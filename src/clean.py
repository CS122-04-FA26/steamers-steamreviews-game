import duckdb
import pandas as pd
from pathlib import Path

RAW_DATA = Path(__file__).resolve().parent.parent / 'data' / 'raw' / 'steam_reviews.csv'
DATA = Path(__file__).resolve().parent.parent / 'data' / 'clean'
DATA.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

eng_extr = con.execute(f"""
    CREATE TABLE IF NOT EXISTS english_reviews AS
    SELECT review_id, 
        app_name,
        "author.num_reviews",
        "author.num_games_owned",
        recommended,
        votes_helpful, 
        "author.playtime_forever", 
        "author.playtime_last_two_weeks",
        "author.playtime_at_review",
        language, 
        weighted_vote_score,
        review
    FROM read_csv('{RAW_DATA}', max_line_size = 10000000)
    WHERE LOWER(TRIM(language)) = 'english'
        AND review IS NOT NULL
        AND app_name IS NOT NULL
        AND recommended IS NOT NULL
        AND TRIM(review) <> ''
    USING SAMPLE 500000 (reservoir, 42);
""")

trim = con.execute(r"""
    UPDATE english_reviews
    SET review = TRIM(REGEXP_REPLACE(review, '\s+', ' ', 'g')),
        language = TRIM(language);
""")

clean = con.execute(""" 
    SELECT  *
    FROM english_reviews
""").fetch_df()

clean.to_csv(DATA / 'clean_sample.csv', index=False)
con.close()
