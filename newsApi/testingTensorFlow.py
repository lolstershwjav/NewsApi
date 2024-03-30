import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import re


df = pd.read_csv("csv_files/newsData.csv")
model = load_model("models/trained_model3.h5")


nasdaq_stocks_df = pd.read_csv("csv_files/NASDAQ-100Index.csv")


texts = pd.read_csv("csv_files/text_sentiment.csv")['text'].values
vocab_size = 2600
max_length = 400
tokenizer = Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(texts)
new_data = pad_sequences(tokenizer.texts_to_sequences(df["Content"]), maxlen=max_length)


predictions = model.predict(new_data)
range_predictions = [int((pred * 20) - 10) for pred in predictions]

def find_stock_names(text):
    stock_names = []
    for index, row in nasdaq_stocks_df.iterrows():
        symbol = row['Symbol']
        description = row['Description']
        regex_pattern = rf"\b{re.escape(symbol)}\b|\b{re.escape(description)}\b"
        if re.search(regex_pattern, text, re.IGNORECASE):
            stock_names.append((symbol, description))
    return stock_names

# Create an empty list to store all the results
results_list = []

for index, prediction in enumerate(range_predictions):
    title = df['Title'][index]
    pub_date = df['Publication Date'][index]
    description = df['Description'][index]
    keywords = df['Keywords'][index].split(',')
    content = df['Content'][index]
    source = df['Source'][index]
    sentiment = prediction
    
    stock_names = find_stock_names(content)
    stocks_found = ', '.join([symbol for symbol, _ in stock_names])
    
    # Append the current result to the list
    results_list.append({
        "Title": title,
        "Publication Date": pub_date,
        "Description": description,
        "Keywords": keywords,
        "Content": content,
        "Source": source,
        "Sentiment": sentiment,
        "StocksFound": stocks_found
    })

    # Print information for each title
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Predicted Sentiment: {sentiment}")
    print(f"Stocks Found: {stocks_found}")
    print()
    print()
    print()
    print(f"Content: {content}")
    print("______________________________________________________")

# Convert the list of results to a DataFrame
results_df = pd.DataFrame(results_list)

results_df.to_csv("csv_files/keyForStocks.csv", index=False, mode='w')
print()
print()
print("Finished")
