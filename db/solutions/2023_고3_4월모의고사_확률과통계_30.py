CANDIDATE = 188

def get_runs(s, char):
    """Get all runs (maximal consecutive sequences) of char in string s"""
    runs = []
    current_len = 0
    for c in s:
        if c == char:
            current_len += 1
        else:
            if current_len > 0:
                runs.append(current_len)
            current_len = 0
    if current_len > 0:
        runs.append(current_len)
    return runs

def satisfies_conditions(s):
    """
    Check if string s satisfies both conditions:
    (가) 한 문자가 연달아 3개 이어지고 그 문자는 특정 문자뿐이다.
         => a has exactly one run of length exactly 3, b and c have no runs of length >= 3
    (나) 어느 한 문자도 연달아 4개 이상 이어지지 않는다.
         => All characters have max run length <= 3
    """
    runs_a = get_runs(s, 'a')
    runs_b = get_runs(s, 'b')
    runs_c = get_runs(s, 'c')
    
    # Condition (가): a must have exactly one run of length 3
    if runs_a.count(3) != 1:
        return False
    
    # All runs of a must be <= 3 (from condition 나)
    if any(r > 3 for r in runs_a):
        return False
    
    # b and c must have no runs of length >= 3 (from condition 가)
    if any(r >= 3 for r in runs_b) or any(r >= 3 for r in runs_c):
        return False
    
    return True

def count_valid_strings():
    """Count all valid 7-character strings using a, b, c with each <= 5 occurrences"""
    count = 0
    
    def generate(pos, current, counts):
        nonlocal count
        
        if pos == 7:
            # Check if this string satisfies both conditions
            if satisfies_conditions(current):
                count += 1
            return
        
        # Try adding each character if we haven't exceeded the limit of 5
        for char in ['a', 'b', 'c']:
            if counts[char] < 5:
                new_counts = counts.copy()
                new_counts[char] += 1
                generate(pos + 1, current + char, new_counts)
    
    generate(0, '', {'a': 0, 'b': 0, 'c': 0})
    return count

# Verify the candidate answer
result = count_valid_strings()
if result == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")