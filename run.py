from gui import GUI
import threading
from operator_queue import OperatorQueue
import sys
import time
import configparser
import re

PATTERN = '[0-9]+$'


def start_monitor_thread(queue, display_window, pause_time=.05):
    def _start():
        while True:
            if queue.changed:
                display_window.update_text(queue.get_text())
            time.sleep(pause_time)

    monitor = threading.Thread(target=_start)
    monitor.setDaemon(True)
    monitor.start()


def parseConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')
    # TODO: error check
    room_id = config['General']['roomId']
    keyword = config['General']['keyword']
    room_id = re.search(PATTERN, room_id).group(0)

    return {'roomId': room_id, 'keyword': keyword}


def main():
    config = parseConfig()
    queue = OperatorQueue('https://live.bilibili.com/' + config['roomId'], config['keyword'])
    # TODO: add config to GUI
    gui = GUI(queue.next_attacker, queue.next_defender)
    start_monitor_thread(queue, gui.combined_window)
    sys.exit(gui.app.exec_())


if __name__ == '__main__':
    main()
