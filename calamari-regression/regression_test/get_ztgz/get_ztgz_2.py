import Levenshtein, re

def focus_words(text):
    return re.sub(r'[^鋼骨筋混凝泥土SRC鐵筋加強磚瓦木石預鑄]', '', text)

def compare_words(c1, c2):
    c1_f = focus_words(c1)
    c2_f = focus_words(c2)
    return Levenshtein.ratio(c1_f, c2_f)

def find_most_like(text):
    ll = [
        '鋼骨鋼筋混凝土',
        '鋼骨混凝土',
        '鋼骨RC',
        '鋼骨',
        '鋼筋混凝土',
        '鋼筋混泥土',
        '鐵筋加強磚',
        '鐵筋',
        '加強磚',
        'SRC',
        'RC',
        'SC',
        '預鑄',
        '磚',
        '瓦',
        '木',
        '石',
    ]

    current = ll[0]
    distance = Levenshtein.distance(current, text)
    for word in ll:
        d = Levenshtein.distance(word, text)
        if d < distance:
            current = word
            distance = d
    if distance > 0:
        print(text, current, distance)
    return current