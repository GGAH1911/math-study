a_9 = 16
a_10 = a_9 + 9
assert a_10 == 25
a_12 = a_10 + 5
assert a_12 == 30
a_11 = a_12 - 11
assert a_11 == 19
assert a_12 - a_10 == 5, 'Condition (가) failed'
assert a_10 - a_9 == 9, 'Condition (나) derived formula failed'
assert a_12 - a_11 == 11, 'Condition (나) derived formula failed'
print('VERIFY_PASS')