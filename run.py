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


def main():
    queue = OperatorQueue('https://live.bilibili.com/4612373')
    gui = GUI(queue.next_attacker, queue.next_defender)
    start_monitor_thread(queue, gui.display_window)
    sys.exit(gui.app.exec_())


if __name__ == '__main__':
    main()
