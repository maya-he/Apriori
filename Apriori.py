from itertools import combinations


def create_candidates(transactions, k):
    candidates = set()
    for transaction in transactions:
        for candidate in combinations(transaction, k):
            candidates.add(frozenset(candidate))
    return candidates


def count_frequencies(data, candidates, min_support):
    freq_counts = {}
    for candidate in candidates:
        count = 0
        for item in data:
            if candidate.issubset(item):
                count += 1
        if count >= min_support:
            freq_counts[candidate] = count

    return freq_counts


def apriori(data, min_support):
    k = 1
    freq_items = {}

    while True:
        candidates = create_candidates(data, k)

        freq_k = count_frequencies(data, candidates, min_support)
        if not freq_k:
            break

        freq_items.update(freq_k)

        k += 1

    return freq_items


def generate_rules(final_generation, min_confidence, freqs):
    rules = []
    for itemset in final_generation.keys():
        if len(itemset) > 1:
            for k in range(1, len(itemset)):
                for antecedent in combinations(itemset, k):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    if len(consequent) > 0:
                        # Calculate confidence of the rule
                        if antecedent in freqs:
                            confidence = freqs[itemset] / \
                                freqs[frozenset(antecedent)]
                            if confidence >= min_confidence:
                                rules.append(
                                    (antecedent, consequent, confidence))

    return rules


data = [
    {'Rihanna', 'Shawn Mendes'},
    {'Shawn Mendes', 'Alec Benjamin'},
    {'Shawn Mendes', 'Taylor Swift'},
    {'Rihanna', 'Shawn Mendes', 'Alec Benjamin'},
    {'Rihanna', 'Taylor Swift'},
    {'Shawn Mendes', 'Taylor Swift'},
    {'Rihanna', 'Taylor Swift'},
    {'Rihanna', 'Shawn Mendes', 'Taylor Swift', 'James Arthur'},
    {'Rihanna', 'Shawn Mendes', 'Taylor Swift'},
]

min_support = 2
min_confidence = 0.5

freq_items = apriori(data, min_support)

final_freq = {}
# Print frequent itemsets
print("Generation 1")
for itemset, support in freq_items.items():
    if len(sorted(list(itemset))) == 1:
        print("{0} : {1}".format(sorted(list(itemset)), support))

print("Generation 2")

for itemset, support in freq_items.items():
    if len(sorted(list(itemset))) == 2:
        print("{0} : {1}".format(sorted(list(itemset)), support))

print("Generation 3")

for itemset, support in freq_items.items():
    if len(sorted(list(itemset))) == 3:
        print("{0} : {1}".format(sorted(list(itemset)), support))
        final_freq[itemset] = support


rules = generate_rules(final_freq, min_confidence, freq_items)
print("_______________________________")
print("Association Rules")

# association rules
for antecedent, consequent, confidence in rules:
    print("{0} => {1} (confidence: {2:.2f})".format(
        sorted(list(antecedent)), sorted(list(consequent)), confidence))
