import json
import os
import platform
from pathlib import Path

try:
    # 시스템 정보와 실시간 부하를 가져오기 위해 psutil을 사용
    import psutil
except ImportError:
    # psutil이 없는 환경에서도 코드가 바로 중단되지 않도록 None으로 처리
    psutil = None


# setting.txt는 Q8 보너스 과제에서 출력 항목을 설정하기 위한 파일
SETTING_FILE_PATH = Path(__file__).with_name('setting.txt')


class MissionComputer:
    def __init__(self):
        # Q7에서 사용하던 환경값 저장 구조는 유지
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        # 보너스 과제: setting.txt를 읽어서 출력할 항목을 설정
        self.settings = self.load_settings()

    def load_settings(self):
        # 설정 파일이 없거나 읽을 수 없을 때 사용할 기본 출력 설정
        settings = {
            'operating_system': True,
            'operating_system_version': True,
            'cpu_type': True,
            'cpu_core_count': True,
            'memory_size': True,
            'cpu_usage': True,
            'memory_usage': True,
        }

        if not SETTING_FILE_PATH.exists():
            # setting.txt가 없으면 기본값으로 새 파일을 생성
            self.create_setting_file(settings)
            return settings

        try:
            with open(SETTING_FILE_PATH, 'r', encoding='utf-8') as file:
                for line in file:
                    # 빈 줄과 주석은 설정값으로 처리하지 않고 건너뜀
                    if not line.strip() or line.strip().startswith('#'):
                        continue

                    # key=value 형태로 읽어서 true/false 설정을 반영
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().lower()

                    if key in settings:
                        settings[key] = value in ('true', '1', 'yes', 'on')
        except OSError as error:
            print(f'setting.txt read error: {error}')
        except ValueError as error:
            print(f'setting.txt format error: {error}')

        return settings

    def create_setting_file(self, settings):
        # setting.txt가 없을 경우 기본 설정 파일을 생성
        try:
            with open(SETTING_FILE_PATH, 'w', encoding='utf-8') as file:
                file.write('# true이면 출력하고 false이면 숨깁니다.\n')

                for key, value in settings.items():
                    file.write(f'{key}={value}\n')
        except OSError as error:
            print(f'setting.txt create error: {error}')

    def get_mission_computer_info(self):
        # 운영체제, CPU, 메모리 크기 같은 기본 시스템 정보를 가져옴
        mission_computer_info = {}

        try:
            if self.settings.get('operating_system', True):
                # platform.system()으로 현재 운영체제 이름을 가져옴
                mission_computer_info['operating_system'] = platform.system()

            if self.settings.get('operating_system_version', True):
                # platform.version()으로 운영체제 버전을 가져옴
                mission_computer_info[
                    'operating_system_version'
                ] = platform.version()

            if self.settings.get('cpu_type', True):
                # platform.processor()로 CPU 타입 정보를 가져옴
                mission_computer_info['cpu_type'] = platform.processor()

            if self.settings.get('cpu_core_count', True):
                # os.cpu_count()로 CPU 코어 수를 가져옴
                mission_computer_info['cpu_core_count'] = os.cpu_count()

            if self.settings.get('memory_size', True):
                # 메모리 크기는 psutil을 사용하는 별도 함수에서 계산
                mission_computer_info['memory_size'] = self.get_memory_size()
        except Exception as error:
            # 시스템 정보 수집 중 오류가 나도 프로그램이 멈추지 않게 처리
            mission_computer_info['error'] = f'info read error: {error}'

        # 수집한 시스템 정보를 JSON 형식으로 출력
        print(json.dumps(mission_computer_info, indent=4))
        return mission_computer_info

    def get_mission_computer_load(self):
        # CPU와 메모리의 현재 사용량을 가져옴
        mission_computer_load = {}

        try:
            if self.settings.get('cpu_usage', True):
                # CPU 사용량은 psutil.cpu_percent()로 측정
                mission_computer_load['cpu_usage'] = self.get_cpu_usage()

            if self.settings.get('memory_usage', True):
                # 메모리 사용량은 psutil.virtual_memory().percent로 가져
                mission_computer_load['memory_usage'] = self.get_memory_usage()
        except Exception as error:
            # 부하 정보 수집 중 오류가 나도 프로그램이 멈추지 않게 처리
            mission_computer_load['error'] = f'load read error: {error}'

        # 수집한 부하 정보를 JSON 형식으로 출력
        print(json.dumps(mission_computer_load, indent=4))
        return mission_computer_load

    def get_memory_size(self):
        # 전체 메모리 크기를 byte에서 GB 단위로 변환
        if psutil is None:
            return 'Unknown'

        memory_size = psutil.virtual_memory().total / 1024 ** 3
        return f'{memory_size:.2f} GB'

    def get_cpu_usage(self):
        # 1초 동안 CPU 사용량을 측정해서 퍼센트 문자열로 반환
        if psutil is None:
            return 'Unknown'

        return f'{psutil.cpu_percent(interval=1)}%'

    def get_memory_usage(self):
        # 현재 메모리 사용률을 퍼센트 문자열로 반환
        if psutil is None:
            return 'Unknown'

        return f'{psutil.virtual_memory().percent}%'


if __name__ == '__main__':
    # 문제 요구사항에 맞게 runComputer 이름으로 인스턴스를 생성
    runComputer = MissionComputer()
    # 시스템 기본 정보와 실시간 부하 정보를 차례대로 출력
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
