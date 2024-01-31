import multiprocessing
import pandas as pd
from transformers import pipeline
import pickle


MODEL = "facebook/bart-large-mnli"

LABELS = ["question", "complaint", "statement", "praise", "user interface", "design", "finance", 
          "credit", "customer relationship", "performance"]

df = pd.read_excel("ING_appstore_reviews.xlsx")

pipe = pipeline("zero-shot-classification", model=MODEL)

cpu_count = multiprocessing.cpu_count()
num_processes = max(1, cpu_count - 1)

def analyze_zero(args):
    index, text = args
    try:
        result = pipe(text, LABELS, multi_label=True)
        print(f"Row {index}: Label - {result['labels']}, Score - {result['scores']}")
        output = {
            index: result
        }
        return output
    except Exception as e:
        print(f"Error processing text in row {index}: {e}")
        output = {
            index: None
        }
    return output
    

if __name__ == '__main__':
    with multiprocessing.Pool(processes=num_processes) as pool:
        index_text_pairs = zip(df.index, df["deep_translator"])
        results = pool.map(analyze_zero, index_text_pairs)
    pickle.dump(results, open("zero_shot_2.pkl", "wb"))
    

