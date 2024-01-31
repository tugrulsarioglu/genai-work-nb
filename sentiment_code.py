import multiprocessing
import pandas as pd
from transformers import pipeline

MODEL = "Kaludi/Reviews-Sentiment-Analysis"
df = pd.read_excel("ING_appstore_reviews.xlsx")

def analyze_sentiment(args):
    index, text = args
    try:
        result = sentiment_pipe(text)[0]
        print(f"Row {index}: Label - {result['label']}, Score - {result['score']}")
        return result["label"], result["score"]
    except Exception as e:
        print(f"Error processing text in row {index}: {e}")
        return None, None

sentiment_pipe = pipeline("text-classification", model=MODEL)

cpu_count = multiprocessing.cpu_count()
num_processes = max(1, cpu_count - 1)

if __name__ == '__main__':
    with multiprocessing.Pool(processes=num_processes) as pool:
        index_text_pairs = zip(df.index, df["deep_translator"])
        results = pool.map(analyze_sentiment, index_text_pairs)

    df['label'], df['score'] = zip(*results)

df.to_excel("ing_sentiment_4.xlsx",index=False)