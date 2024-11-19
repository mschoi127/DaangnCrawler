# -*- coding: utf-8 -*-

import json
import csv
import sys
import io
from datetime import datetime

def process_results(json_path, output_csv="sorted_results.csv"):
    # JSON 파일 로드
    with io.open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # search_keyword로 그룹화하고 최신순으로 정렬
    sorted_data = sorted(data, key=lambda x: (x['search_keyword'], datetime.strptime(x['end_time'], "%Y-%m-%d %H:%M:%S")), reverse=True)
    
    # CSV 파일로 저장
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["search_keyword", "total_items", "search_page_requests", "detail_page_requests", "start_time", "end_time", "duration", "total_requests"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in sorted_data:
            # Python 3에서는 모든 문자열이 기본적으로 유니코드이기 때문에 별도로 인코딩할 필요 없음
            writer.writerow(row)
    
    print("[INFO] CSV 파일 '{}'로 저장 완료.".format(output_csv))

if __name__ == "__main__":
    # 사용자가 JSON 파일 경로를 지정하지 않은 경우 기본값으로 사용
    if len(sys.argv) < 2:
        json_path = "result.json"  # 기본 파일명
    else:
        json_path = sys.argv[1]
    
    # CSV 파일 생성
    process_results(json_path)
