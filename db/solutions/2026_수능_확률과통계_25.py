from itertools import combinations
import fractions

white_balls = [(1, 'W'), (2, 'W'), (3, 'W'), (4, 'W'), (5, 'W')]
black_balls = [(2, 'B'), (3, 'B'), (4, 'B'), (5, 'B'), (6, 'B')]
all_balls = white_balls + black_balls

all_pairs = list(combinations(all_balls, 2))
total = len(all_pairs)

favorable = 0
for pair in all_pairs:
    ball1, ball2 = pair
    num1, color1 = ball1
    num2, color2 = ball2
    
    same_color = (color1 == color2)
    same_number = (num1 == num2)
    
    if same_color or same_number:
        favorable += 1

prob = fractions.Fraction(favorable, total)
if prob == fractions.Fraction(8, 15):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')