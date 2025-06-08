from multiprocessing import Pool
from collections import Counter

texts = [
    "data lake big data hadoop spark",
    "spark big data mapreduce data lake",
    "hadoop mapreduce hive big data",
    "big data streaming spark hadoop"
]

def count_words(text):
    words = text.split()
    return Counter(words)

# Инициализация пула из 4 параллельных процессов
if __name__ == '__main__':
    with Pool(4) as pool:
        results = pool.map(count_words, texts)

# Reduce-функция: объединение словарей с частотами
final_counts = Counter()
for result in results:
    final_counts.update(result)

print(final_counts)
