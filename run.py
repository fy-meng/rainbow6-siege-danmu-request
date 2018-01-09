import configparser
from gui import GUI
import threading
from operator_queue import OperatorQueue
import sys
import time


def start_monitor_thread(queue, display_window, pause_time=.05):
    def _start():
        while True:
            if queue.changed:
                display_window.update_text(queue.get_text())
            time.sleep(pause_time)

    monitor = threading.Thread(target=_start)
    monitor.setDaemon(True)
    monitor.start()


def parse_config():
    config = configparser.ConfigParser()
    with open('config.ini', encoding='utf-8') as f:
        config.read_file(f)
    room_id = config['General']['roomId']
    keyword = config['General']['keyword']
    return {'roomId': room_id,
            'keyword': keyword,
            'font': (config['Display']['font'],
                     int(config['Display']['font_size']),
                     config['Display']['font_color']),
            'bg_color': config['Display']['bg_color']}


def main():
    config = parse_config()
    queue = OperatorQueue('https://live.bilibili.com/' + config['roomId'], config['keyword'])
    # TODO: add config to GUI
    gui = GUI(queue.next_attacker, queue.next_defender, config['font'], config['bg_color'])
    start_monitor_thread(queue, gui.display_window)
    sys.exit(gui.app.exec_())


if __name__ == '__main__':
    main()
