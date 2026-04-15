import json
import random
import time

try:
    import msvcrt
except ImportError:
    msvcrt = None


class DummySensor:
    # Q6에서 만든 더미 센서를 그대로 사용해서 임의의 환경값을 생성합니다.
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
        return self.env_values


class MissionComputer:
    # 미션 컴퓨터가 센서 데이터를 직접 가져와 출력하도록 만든 클래스입니다.
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        self.ds = DummySensor()
        self.env_history = []

    def get_sensor_data(self):
        # 센서값을 가져와 env_values에 저장하고 5초마다 JSON으로 출력합니다.
        start_time = time.time()
        print('Press q to stop.')

        try:
            while True:
                if self._is_stop_key_pressed():
                    print('Sytem stoped....')
                    break

                self.ds.set_env()
                self.env_values = self.ds.get_env()
                self.env_history.append(self.env_values.copy())

                # 딕셔너리 형태의 환경값을 보기 쉬운 JSON 형식으로 출력합니다.
                print(json.dumps(self.env_values, indent=4))

                if time.time() - start_time >= 300:
                    self.print_average_values()
                    self.env_history = []
                    start_time = time.time()

                if self._wait_seconds(5):
                    print('Sytem stoped....')
                    break
        except KeyboardInterrupt:
            print('Sytem stoped....')

    def print_average_values(self):
        # 보너스 기능: 5분 동안 저장한 환경값의 평균을 계산합니다.
        if not self.env_history:
            return

        average_values = {}
        data_count = len(self.env_history)

        for key in self.env_values:
            total = sum(env_value[key] for env_value in self.env_history)
            average_values[key] = round(total / data_count, 4)

        print('5 minute average values')
        print(json.dumps(average_values, indent=4))

    def _wait_seconds(self, seconds):
        end_time = time.time() + seconds

        while time.time() < end_time:
            if self._is_stop_key_pressed():
                return True
            time.sleep(0.1)

        return False

    def _is_stop_key_pressed(self):
        # Windows에서는 q 키 입력으로 반복 출력을 멈출 수 있습니다.
        if msvcrt is None:
            return False

        if not msvcrt.kbhit():
            return False

        key = msvcrt.getch().decode(errors='ignore').lower()
        return key == 'q'


if __name__ == '__main__':
    # 문제 요구사항에 맞게 RunComputer 이름으로 인스턴스를 생성합니다.
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data()
