from fractions import Fraction
from sympy import Rational, simplify

# 표 데이터 (단위: 명)
movie_and_musical = 90      # 영화 희망, 뮤지컬 희망
movie_and_not_musical = 120  # 영화 희망, 뮤지컬 안함
not_movie_and_musical = 50   # 영화 안함, 뮤지컬 희망
not_movie_and_not_musical = 40  # 영화 안함, 뮤지컬 안함

# 검증: 합계가 300명인지 확인
total = movie_and_musical + movie_and_not_musical + not_movie_and_musical + not_movie_and_not_musical
assert total == 300, f"합계가 300이 아님: {total}"

# 영화 관람을 희망한 학생의 명수
num_movie_hope = movie_and_musical + movie_and_not_musical
assert num_movie_hope == 210, f"영화 희망자가 210이 아님: {num_movie_hope}"

# 영화 희망하고 뮤지컬도 희망한 학생의 명수
num_movie_and_musical_hope = movie_and_musical
assert num_movie_and_musical_hope == 90, f"영화∩뮤지컬 희망자가 90이 아님"

# 조건부확률 P(뮤지컬 희망 | 영화 희망) = N(뮤지컬∩영화) / N(영화)
# 원래 정의식: P(A|B) = N(A∩B) / N(B)
conditional_prob_numerator = num_movie_and_musical_hope
conditional_prob_denominator = num_movie_hope

# 유리수로 표현
conditional_prob = Rational(conditional_prob_numerator, conditional_prob_denominator)

# 기약분수로 정리
simplified_prob = simplify(conditional_prob)

# 문제의 정답 선택지 확인
option_1 = Rational(3, 14)
option_2 = Rational(2, 7)
option_3 = Rational(5, 14)
option_4 = Rational(3, 7)
option_5 = Rational(1, 2)

# 도출한 답이 정답과 일치하는지 확인
if simplified_prob == option_4:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")