import re

def list_times(items):
    # [a, b] * [c] => [ac, bc]
    if len(items) == 1:
        return items[0]
    cur = items[0]
    for i in range(1, len(items)):
        results = []
        for left in cur:
            for right in items[i]:
                result = left + right
                if len(result) > 0:
                    results.append(left + right)
        cur = results
    return cur

def make_list(text):
    data = []
    cur = ''
    prev = ''
    opts = None
    for ch in text:
        if ch is '[':
            if len(cur) > 0:
                data.append([cur])
                cur = ''
            opts = ''
        elif ch is ']':
            if len(opts) > 0:
                opt_list = [u for u in opts]
                opt_list.append('')
                data.append(opt_list)
            opts = None
        elif opts is not None:
            opts += ch
        else:
            cur += ch
        prev = ch
    if len(cur) > 0:
        data.append([cur])
    return list_times(data)

def gen_big_table():
    big_table = {}

    dd = {
        '鋼骨鋼筋混凝土': '[鋼]骨[鋼]筋[混]凝[土]',
        '鋼骨混凝土': '[鋼]骨[混]凝[土]',
        '鋼骨RC': '[鋼]骨R[C]',
        '鋼骨': '[鋼]骨',
        '鋼筋混凝土': '[鋼]筋[混]凝[土]',
        '鋼筋混泥土': '[鋼]筋[混]泥[土]',
        '鐵筋加強磚': '鐵[筋][加強][加強][磚]',
        '鐵筋': '鐵[筋]',
        '加強磚': '[加強][加強][磚]',
        'SRC': 'SR[C]',
        'RC': 'R[C]',
        'SC': 'S[C]',
        '預鑄': '[預鑄][預鑄]',
        '磚': '磚',
        '瓦': '瓦',
        '木': '木',
        '石': '石',
    }

    for key in dd:
        tpl = dd[key]
        items = make_list(tpl)
        for item in items:
            if item in big_table and key != big_table[item]:
                print('Warning: Value for [', item, '] is [', big_table[item], '] >>> [', key, ']')
            big_table[item] = key
    return big_table

def gen_get_value(table):
    def get_value(text):
        text = text.strip()
        if text in table:
            return table[text]
        print('[' + text + '] not in table')
        return text
    return get_value

def focus_words(text):
    return re.sub(r'[^鋼骨筋混凝泥土SRC鐵筋加強磚瓦木石預鑄]', '', text)
