import pandas as pd
import string
import re
import pickle

posting_lists = {}
document_data = {}

def read_stopwords(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        stopwords = file.read().splitlines()
    return stopwords

def load_data(file_path, stopwords):
    df = pd.read_csv(file_path)
    plots = df["Plot"]

    for id, plot in plots.items():
        plot = plot.translate(str.maketrans('', '', string.punctuation))
        plot = re.sub(r'\W+', ' ', plot)

        words = set(plot.lower().split())
        for word in words:
            if word not in stopwords:
                posting_lists.setdefault(word, []).append(id)
                
        document_data[id] = df.loc[id].to_dict()

    with open(save_file_path, "w", encoding='utf-8') as file:
        for word in posting_lists:
            file.write(f"{word}: {posting_lists[word]}\n")
    
    print(f"Inverted index saved to {save_file_path}.")

    
    save_document_data_pickle(document_data, document_pickle_file_path)

def save_document_data_pickle(data, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(data, file)
    print(f"Document data saved to {file_path}")

if __name__ == "__main__":
    file_path = "wiki_movie.csv"
    stopword_file_path = "stopwords.txt"
    save_file_path = "inverted_index.txt"
    document_pickle_file_path = "document_data.pkl"

    stopwords = read_stopwords(stopword_file_path)
    load_data(file_path, stopwords)
    