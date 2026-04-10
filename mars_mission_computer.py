import time
import json
import random
from datetime import datetime


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(
            random.uniform(18, 30), 2
        )
        self.env_values['mars_base_external_temperature'] = round(
            random.uniform(0, 21), 2
        )
        self.env_values['mars_base_internal_humidity'] = round(
            random.uniform(50, 60), 2
        )
        self.env_values['mars_base_external_illuminance'] = round(
            random.uniform(500, 715), 2
        )
        self.env_values['mars_base_internal_co2'] = round(
            random.uniform(0.02, 0.1), 4
        )
        self.env_values['mars_base_internal_oxygen'] = round(
            random.uniform(4, 7), 2
        )

    def get_env(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        log_message = (
            f'{current_time}, '
            f'{self.env_values["mars_base_internal_temperature"]}, '
            f'{self.env_values["mars_base_external_temperature"]}, '
            f'{self.env_values["mars_base_internal_humidity"]}, '
            f'{self.env_values["mars_base_external_illuminance"]}, '
            f'{self.env_values["mars_base_internal_co2"]}, '
            f'{self.env_values["mars_base_internal_oxygen"]}\n'
        )

        with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)

        return self.env_values


class MissionComputer:
    def __init__(self):
        # 화성 기지 환경 값을 저장할 사전(Dict) 객체
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        # DummySensor 인스턴스화
        self.ds = DummySensor()
        # 5분 평균 계산을 위한 데이터 히스토리 저장 리스트
        self.history = []

    def get_sensor_data(self):
        print('데이터 수집을 시작합니다. (종료하려면 Ctrl + C 키를 누르세요)')
        start_time = time.time()

        try:
            while True:
                # 센서의 값을 랜덤하게 갱신
                self.ds.set_env()
                
                # 센서의 값을 가져와서 env_values에 담음
                self.env_values = self.ds.get_env()
                self.history.append(self.env_values.copy())

                # 환경 정보의 값을 json 형태로 화면에 출력
                print(json.dumps(self.env_values, indent=4))

                # 보너스 과제: 5분(300초)에 한 번씩 5분 평균 값 출력
                current_time = time.time()
                if current_time - start_time >= 300:
                    self._print_average_values()
                    self.history.clear()  # 출력 후 히스토리 초기화
                    start_time = current_time

                # 5초에 한 번씩 반복
                time.sleep(5)

        except KeyboardInterrupt:
            # 보너스 과제: 특정 키(Ctrl+C) 입력 시 출력 멈춤 및 메시지 출력
            print('Sytem stoped....')

    def _print_average_values(self):
        average_values = {}
        count = len(self.history)
        for key in self.env_values.keys():
            total = sum(item[key] for item in self.history)
            average_values[key] = round(total / count, 4)
            
        print('\n[5분 평균 환경 데이터]')
        print(json.dumps(average_values, indent=4))
        print('-' * 30 + '\n')


if __name__ == '__main__':
    # MissionComputer 클래스를 RunComputer라는 이름으로 인스턴스화
    RunComputer = MissionComputer()
    
    # 지속적으로 환경에 대한 값을 출력할 수 있도록 메소드 호출
    RunComputer.get_sensor_data()
