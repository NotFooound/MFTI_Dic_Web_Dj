import sqlite3
import random

conn = sqlite3.connect('words.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS words (
term1 TEXT, 
term2 TEXT,
term3 TEXT,
term4 TEXT,
added_by TEXT NOT NULL)
''')
conn.commit()
conn.close()

def randomizer_for_test():
    get_terms = get_terms_for_table()
    random_terms = random.sample(get_terms,len(get_terms))
    terms = {
        "term1": random_terms[0][1],
        "term2": random_terms[0][2],
        "term3": random_terms[0][3],
        "term4": random_terms[0][4],
    }
    return terms

def get_terms_for_table():
    terms = []
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    new_term_line = cursor.execute("SELECT term1, term2, term3, term4, added_by FROM words").fetchall()
    cnt = 1
    for line in new_term_line:
        term1, term2, term3, term4, added_by = line
        terms.append([cnt, term1, term2, term3, term4])
        cnt += 1
    conn.commit()
    conn.close()
    return terms

def write_term(new_term1, new_term2, new_term3, new_term4):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (term1, term2, term3, term4, added_by) '
                   'VALUES (?,?,?,?,?)', (new_term1, new_term2, new_term3, new_term4, 'user'))
    conn.commit()
    conn.close()

def get_terms_stats():
    db_terms = 0
    user_terms = 0
    term1_len, term2_len, term3_len, term4_len= [], [], [], []
    term1, term2, term3, term4, added_by = '', '', '', '', ''
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    new_term_line = cursor.execute("SELECT term1, term2, term3, term4, added_by FROM words").fetchall()
    for line in new_term_line:
        term1, term2, term3, term4, added_by = line
        term1_len.append(len(term1))
        term2_len.append(len(term2))
        term3_len.append(len(term3))
        term4_len.append(len(term4))
        if "user" in added_by:
            user_terms += 1
        elif "db" in added_by:
            db_terms += 1
    conn.commit()
    conn.close()

    max_big_line = max(max(term1_len), max(term2_len), max(term3_len), max(term4_len))
    min_big_line = min(min(filter(lambda x: x > 0, term1_len)), min(filter(lambda x: x > 0, term2_len)), min(filter(lambda x: x > 0, term3_len)), min(filter(lambda x: x > 0, term4_len)))
    terms_sum = sum(term1_len) + sum(term2_len) + sum(term3_len) + sum(term4_len)
    terms_len = len(term1_len) + len(term2_len) + len(term3_len) + len(term4_len)

    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": terms_sum / terms_len,
        "words_max": max_big_line,
        "words_min": min_big_line,
    }
    return stats