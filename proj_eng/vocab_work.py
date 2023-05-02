import pandas as pd

def get_words_for_table():
    words = []
    df = pd.read_csv("./data/words.csv")
    for i in range(len(df)):
        words.append([i + 1] + df.iloc[i][["en", "ru"]].to_list())
    return words

def write_word(en_word, ru_word):
    try:
        df = pd.read_csv("./data/words.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns={"en", "ru"})
    df.loc[len(df) + 1, ["en", "ru"]] = en_word.strip(), ru_word.strip()
    df = df.drop_duplicates().sort_values(["en", "ru"])
    df.to_csv("./data/words.csv", index=False)

