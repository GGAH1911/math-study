ages = [17, 18, 19, 19, 20, 25, 25, 28, 28, 34, 34, 34, 35, 41, 46]
from collections import Counter
freq = Counter(ages)
mode = freq.most_common(1)[0][0]
print('VERIFY_PASS' if mode == 34 else 'VERIFY_FAIL')