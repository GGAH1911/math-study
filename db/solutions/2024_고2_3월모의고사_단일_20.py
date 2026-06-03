from itertools import product

# Verify the 3 valid functions
valid_functions = [
    [1, 2, 4, 1],  # f(1)=1, f(2)=2, f(3)=4, f(4)=1
    [1, 1, 4, 2],  # f(1)=1, f(2)=1, f(3)=4, f(4)=2
    [2, 1, 4, 2],  # f(1)=2, f(2)=1, f(3)=4, f(4)=2
]

for f_list in valid_functions:
    f = lambda x: f_list[x-1]
    
    # Check condition (가): x + f(f(x)) <= 5 for all x
    for x in [1, 2, 3, 4]:
        if x + f(f(x)) > 5:
            print("VERIFY_FAIL")
            exit()
    
    # Check condition (나): range(f) = {1, 2, 4}
    range_f = set(f_list)
    if range_f != {1, 2, 4}:
        print("VERIFY_FAIL")
        exit()
    
    # Check ㄴ: f(3) = 4
    if f(3) != 4:
        print("VERIFY_FAIL")
        exit()
    
    # Check ㄱ: f(f(4)) = 1
    if f(f(4)) != 1:
        print("VERIFY_FAIL")
        exit()

print("VERIFY_PASS")