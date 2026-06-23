A = {3, 5, 7, 9}
B = {3, 7}
diff = A - B
assert 9 in diff, 'VERIFY_FAIL: 9 not in A-B'
elements_except_9 = diff - {9}
assert len(elements_except_9) == 1, 'VERIFY_FAIL: unexpected structure'
a = elements_except_9.pop()
assert a == 5, f'VERIFY_FAIL: a={a}'
print('VERIFY_PASS')