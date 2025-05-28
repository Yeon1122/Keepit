from PIL import Image
import os

# 현재 스크립트의 위치를 기준으로 상대 경로 계산
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(os.path.dirname(script_dir), 'assets', 'images', 'logo2.png')
output_dir = os.path.join(script_dir, 'public', 'assets', 'images')
os.makedirs(output_dir, exist_ok=True)

# 이미지 로드
img = Image.open(input_path)

# RGBA 모드로 변환 (투명도 지원)
img = img.convert('RGBA')

# 투명도 처리
datas = img.getdata()
newData = []
for item in datas:
    # 흰색 픽셀을 투명하게 변환 (흰색에 가까운 픽셀도 포함)
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)

# 48x48 크기로 리사이즈 (favicon용)
favicon_size = (48, 48)
resized_img = img.resize(favicon_size, Image.Resampling.LANCZOS)

# 저장
output_path = os.path.join(output_dir, 'logo2.png')
resized_img.save(output_path, 'PNG')

print(f"Processed image saved to: {output_path}") 