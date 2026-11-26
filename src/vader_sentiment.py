from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path
from tqdm.auto import tqdm
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / 'data' / 'clean'
data = DATA / 'clean_sample.csv'
df = pd.read_csv(data)
df = df.dropna(subset=['review'])

#activate progress bar
tqdm.pandas()

analyser = SentimentIntensityAnalyzer()
df['vader_score'] = df['review'].progress_apply(lambda x: analyser.polarity_scores(x)['compound'])

df.to_csv(DATA / 'sample_with_vade.csv', index=False)