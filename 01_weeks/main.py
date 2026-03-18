def main():
    # 1. Hello Mars 출력 확인
    print('Hello Mars')

    input_file = 'mission_computer_main.log'
    error_file = 'error_log.log'  # 보너스: 문제가 되는 부분 저장용

    try:
        # 파일 열기 (UTF-8 인코딩 준수)
        with open(input_file, 'r', encoding='utf-8') as file:
            # 보너스 처리를 위해 줄 단위로 읽어 리스트에 저장
            lines = file.readlines()

        if not lines:
            print('로그 파일이 비어 있습니다.')
            return

        print('-' * 30)
        print('전체 로그 내용 (시간 역순 정렬):')
        
        # 보너스 1: 시간의 역순으로 정렬해서 출력 (리스트 뒤집기)
        reversed_lines = lines[::-1]
        
        error_lines = []
        for line in reversed_lines:
            clean_line = line.strip()
            print(clean_line)
            
            # 보너스 2: 문제가 되는 부분(ERROR 또는 CRITICAL) 따로 수집
            # 로그 형식에 따라 'ERROR', 'FAIL', 'CRITICAL' 등을 체크합니다.
            if 'unstable' in clean_line or 'explosion' in clean_line:
                error_lines.append(line)

        print('-' * 30)

        # 보너스 2 실행: 문제가 되는 부분만 파일로 저장
        if error_lines:
            with open(error_file, 'w', encoding='utf-8') as ef:
                ef.writelines(error_lines)
            print(f'문제가 발견되어 {error_file}에 저장되었습니다.')
        else:
            print('특이사항이 발견되지 않았습니다.')

    except FileNotFoundError:
        print(f'에러: {input_file} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')

if __name__ == '__main__':
    main()