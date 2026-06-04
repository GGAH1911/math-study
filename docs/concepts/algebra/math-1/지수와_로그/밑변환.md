---
sources: []
created: 2026-05-17
updated: 2026-05-17
auto_explained: true
concept_type: definition
domain: 수와식
grade: 수학1
prerequisites: [docs/concepts/algebra/math-1/지수와_로그.md]
enables: []
mastery: unknown
---

# 밑변환

## 정확한 진술

밑변환 공식은 어떤 밑의 로그를 다른 밑의 로그로 나타내는 방법입니다. $a > 0, a \neq 1$, $c > 0, c \neq 1$, $b > 0$일 때:

$$\log_a b = \frac{\log_c b}{\log_c a}$$

특히 자주 쓰이는 형태는 밑을 10 또는 자연로그 $e$로 바꾸는 것입니다:
$$\log_a b = \frac{\lg b}{\lg a} = \frac{\ln b}{\ln a}$$
(여기서 $\lg$는 상용로그, $\ln$은 자연로그)

## 직관과 유도

밑변환 공식은 로그의 정의에서 바로 나옵니다. $\log_a b = x$라고 하면 $a^x = b$입니다. 양변에 밑 $c$인 로그를 취하면:
$$\log_c(a^x) = \log_c b$$
$$x \log_c a = \log_c b$$
$$x = \frac{\log_c b}{\log_c a}$$

즉, 원래 밑 $a$로 나타낸 로그값이 새로운 밑 $c$의 로그로 어떻게 표현되는지 보여줍니다. 계산기나 컴퓨터는 보통 상용로그나 자연로그만 지원하므로, 임의의 밑을 계산할 때 이 공식이 필수입니다.

## 한 줄 예

$\log_2 8$을 상용로그로 구하면: $\log_2 8 = \frac{\log 8}{\log 2} \approx \frac{0.903}{0.301} = 3$ (실제로 $2^3 = 8$이므로 맞음)

**검산 코드**: `from sympy import log, simplify; simplify(log(8, 2))` → `3`
