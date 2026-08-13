# 기출 PNG → 무손실/손실 WebP 압축률 실측(표본). 서빙 계층이 무손실을 고른 근거.
import glob, io, os, random, sys
from PIL import Image
random.seed(3)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
s = random.sample(glob.glob(os.path.join(os.path.dirname(__file__), '../../public/problem-images/*.png')), n)
tp = tw = tl = 0
for f in s:
    im = Image.open(f); tp += os.path.getsize(f)
    b = io.BytesIO(); im.save(b, 'WEBP', lossless=True, quality=100, method=6); tw += b.tell()
    b2 = io.BytesIO(); im.convert('RGB').save(b2, 'WEBP', quality=90, method=6); tl += b2.tell()
print(f'표본 {n}장  PNG {tp/1024/1024:.2f}MB')
print(f'  WebP 무손실 {tw/1024/1024:.2f}MB ({tw/tp*100:.1f}%)')
print(f'  WebP q90    {tl/1024/1024:.2f}MB ({tl/tp*100:.1f}%)')
