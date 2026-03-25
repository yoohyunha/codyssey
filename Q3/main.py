def main():
    input_file = 'Mars_Base_Inventory_List.csv' # 파일 읽음
    danger_file = 'Mars_Base_Inventory_danger.csv' # 위험물 저장용 파일
    binary_file = 'Mars_Base_Inventory_List.bin' # 이진 데이터 저장용 파일

    inventory_list = [] #읽어올 데이터 담을 빈 리스트 생성

    try:
        # 1. CSV 파일 읽기 및 출력 (라이브러리 없이 구현)
        with open(input_file, 'r', encoding='utf-8') as file: # 파일을 읽기모드로 열기
            header = file.readline().strip() # 맨 윗줄만 따로 읽어서 저장
            for line in file:
                row = line.strip().split(',')
                if row:
                    inventory_list.append(row)
        
        print('--- 전체 인벤토리 목록 ---')
        for item in inventory_list:
            print(item)

        # 2. 인화성 지수 순으로 정렬 (인덱스는 CSV 구조에 따라 조정 필요, 예: 마지막 컬럼)
        # 인화성 지수가 숫자로 들어있다고 가정하고 정렬 (내림차순)
        inventory_list.sort(key=lambda x: float(x[-1]), reverse=True)

        # 3. 인화성 0.7 이상 목록 추출 및 출력/저장
        danger_list = []
        print('\n--- 위험 물품 목록 (인화성 0.7 이상) ---')
        
        with open(danger_file, 'w', encoding='utf-8') as df:
            df.write(header + '\n')
            for item in inventory_list:
                if float(item[-1]) >= 0.7:
                    print(item)
                    danger_list.append(item)
                    df.write(','.join(item) + '\n')

        # 4. 보너스 과제: 이진 파일(Binary)로 저장 및 다시 읽기
        # 텍스트 데이터를 바이트로 인코딩하여 저장
        with open(binary_file, 'wb') as bf:
            for item in inventory_list:
                data = '|'.join(item) + '\n'
                bf.write(data.encode('utf-8'))

        print('\n--- 이진 파일에서 읽어온 내용 ---')
        with open(binary_file, 'rb') as bf:
            binary_content = bf.read().decode('utf-8')
            print(binary_content)

    except FileNotFoundError:
        print(f'에러: {input_file} 파일을 찾을 수 없습니다.')
    except ValueError:
        print('에러: 인화성 지수 데이터 형식이 올바르지 않습니다.')
    except Exception as e:
        print(f'알 수 없는 오류 발생: {e}')


if __name__ == '__main__':
    main()