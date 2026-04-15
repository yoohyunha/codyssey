import random
from datetime import datetime
from pathlib import Path


LOG_FILE_PATH = Path(__file__).with_name('mars_env_log.txt')


class DummySensor:
    # 실제 센서가 없기 때문에 테스트용 환경값을 만드는 더미 센서 클래스입니다.
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
        # 각 환경값을 문제에서 정한 범위 안에서 랜덤으로 생성합니다.
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
        # 보너스 기능: 현재 시간과 환경값을 로그 파일에 기록한 뒤 반환합니다.
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

        with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
            log_file.write(log_message)

        return self.env_values


if __name__ == '__main__':
    # DummySensor 객체를 만들고 센서값 생성과 조회가 되는지 확인합니다.
    ds = DummySensor()
    ds.set_env()
    env_data = ds.get_env()

    print(env_data)
