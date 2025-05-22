# scripts/load_regions.py

import os
import django
import json

# ✅ 너의 settings.py 경로에 맞춰서 수정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "keepit.settings")
django.setup()

from regions.models import RegionCity, RegionDistrict

with open('scripts/data.json', encoding='utf-8') as f:
    data = json.load(f)

for city_info in data['mapInfo']:
    city_name = city_info['name']
    city_obj, _ = RegionCity.objects.get_or_create(name=city_name)

    for district_name in city_info['countries']:
        RegionDistrict.objects.get_or_create(name=district_name, city=city_obj)

print("✅ 지역 정보 등록 완료!")
