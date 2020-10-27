import pandas as pd
import psycopg2

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

conn = psycopg2.connect(
    host="localhost",
    database="nlp",
    user="postgres",
    password="mati1234")
cur = conn.cursor()


def loop_main():
    while True:
        sentence = input("Search: ")
        print(f'\n\nSearch sentence: {sentence}\n')
        abstract_all(sentence)
        abstract_one_word(sentence)
        one_word_in_all_column(sentence)


def abstract_all(sentence: str):
    sentence = sentence.strip().replace(r'\s\s+', ' ').replace(" ", " & ")
    print("All words:\n")
    query = f"SELECT " \
            f"paper_title, " \
            f"ts_rank_cd(to_tsvector(\'mycfg\',abstract), query) AS rank " \
            f"from " \
            f"article, " \
            f"to_tsquery(\'mycfg\', \'{sentence}\') query " \
            f"where " \
            f"to_tsvector(\'mycfg\',abstract) @@ query " \
            f"order by rank desc;"
    cur.execute(query)
    response = cur.fetchall()
    df = pd.DataFrame(columns=['title', 'rank'], data=response)
    print(f'Amount: {len(response)}')
    print(df)
    print(f'Amount: {len(response)}')
    print("\n\n")


def abstract_one_word(sentence: str):
    sentence = sentence.strip().replace(r'\s\s+', ' ').replace(" ", " | ")
    print("At least one word:\n")
    query = f"SELECT " \
            f"paper_title, " \
            f"ts_rank_cd(to_tsvector(\'mycfg\',abstract), query) AS rank " \
            f"from " \
            f"article, " \
            f"to_tsquery(\'mycfg\', \'{sentence}\') query " \
            f"where " \
            f"to_tsvector(\'mycfg\',abstract) @@ query " \
            f"order by rank desc;"
    cur.execute(query)
    response = cur.fetchall()
    df = pd.DataFrame(columns=['title', 'rank'], data=response)
    print(f'Amount: {len(response)}')
    print(df)
    print(f'Amount: {len(response)}')
    print("\n\n")


def one_word_in_all_column(sentence: str):
    sentence = sentence.strip().replace(r'\s\s+', ' ').replace(" ", " | ")
    print("At least one word in all columns:\n")
    query = f"SELECT " \
            f"paper_title, " \
            f"ts_rank_cd(to_tsvector(\'mycfg\',paper_title), query) AS rank_paper_title, " \
            f"ts_rank_cd(to_tsvector(\'mycfg\',keywords), query) AS rank_keywords, " \
            f"ts_rank_cd(to_tsvector(\'mycfg\',abstract), query) AS rank, " \
            f"ts_rank_cd(to_tsvector(\'mycfg\',session), query) AS rank_session " \
            f"from " \
            f"article, " \
            f"to_tsquery(\'mycfg\', \'{sentence}\') query " \
            f"where " \
            f"to_tsvector(\'mycfg\',paper_title) @@ query " \
            f"or to_tsvector(\'mycfg\',keywords) @@ query " \
            f"or to_tsvector(\'mycfg\',abstract) @@ query " \
            f"or to_tsvector(\'mycfg\',session) @@ query " \
            f"order by " \
            f"rank desc, " \
            f"rank_paper_title desc, " \
            f"rank_keywords desc, " \
            f"rank_session desc;"
    cur.execute(query)
    response = cur.fetchall()
    df = pd.DataFrame(columns=['title', 'rank_paper_title', 'rank_keywords', 'rank', 'rank_session'], data=response)
    print(f'Amount: {len(response)}')
    print(df)
    print(f'Amount: {len(response)}')
    print("\n\n")


if __name__ == '__main__':
    loop_main()
