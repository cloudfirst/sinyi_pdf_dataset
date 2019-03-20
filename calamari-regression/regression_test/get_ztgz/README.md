
Usage
-----

``` python
from get_ztgz.get_ztgz import gen_big_table, gen_get_value, focus_words
big_table = gen_big_table() # big dict, see: table.txt
get_ztgz = gen_get_value(big_table)

text = '骨混凝土構造'
text_f = focus_words(text) # 骨混凝土 
text_v = get_ztgz(text_f) # 鋼骨混凝土
```



``` bash
python3 preview.py
```

Result:

```
Warning: Value for [ 鐵筋 ] is [ 鐵筋加強磚 ] >>> [ 鐵筋 ]
Warning: Value for [ 鐵 ] is [ 鐵筋加強磚 ] >>> [ 鐵筋 ]
鋼骨造 >> 鋼骨 =\= 鋼骨鋼筋混凝土
磚造 >> 磚 =\= 加強磚
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼骨造 >> 鋼骨 =\= 鋼骨混凝土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼骨造 >> 鋼骨 =\= 鋼骨混凝土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼骨混凝土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼骨造 >> 鋼骨 =\= 鋼筋混凝土
鋼骨造 >> 鋼骨 =\= 鋼骨混凝土
[鋼骨混] not in table
鋼骨造 >> 鋼骨 =\= 鋼骨混
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼骨混凝土
鋼骨造 >> 鋼骨 =\= 鋼骨混凝土
鋼骨鋼筋混凝土造 >> 鋼骨鋼筋混凝土 =\= 鋼骨
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼骨混凝土
鋼骨造 >> 鋼骨 =\= 鋼骨混凝土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼筋混泥土
鋼筋混凝土造 >> 鋼筋混凝土 =\= 鋼骨鋼筋混凝土
==================================
13.86 % : ret == gt
82.05 % : focus_words(ret) == focus_words(gt)
82.05 % : get_ztgz(focus_words(ret)) == get_ztgz(focus_words(gt))
```