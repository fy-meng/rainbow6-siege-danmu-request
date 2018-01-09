from danmu import DanMuClient
import heapq
import re
import time


class Operator:
    OP_NAME_DICT = []

    def __init__(self, input_name, user):
        input_name.lower()
        success = False
        for operator in self.OP_NAME_DICT:
            for nickname in self.OP_NAME_DICT[operator]:
                if input_name == nickname:
                    self.name = operator
                    success = True
        if not success:
            raise ValueError('Illegal operator name: ' + input_name)
        self.users = {user}
        self.time = time.time()

    def user_count(self):
        return len(self.users)

    def update(self, username):
        self.users.update({username})

    def match_name(self, input_name):
        return input_name.lower() in self.OP_NAME_DICT[self.name]

    def __eq__(self, other):
        return self.user_count() == other.user_count() and self.time == other.time

    def __lt__(self, other):
        return self.user_count() > other.user_count() \
               or self.user_count() == other.user_count() and self.time < other.time

    def __gt__(self, other):
        return not self == other and not self < other

    def __str__(self):
        return '[{0}: {1}]'.format(self.name, self.user_count())

    def __repr__(self):
        return self.__str__()


class Attacker(Operator):
    OP_NAME_DICT = {
        'sledge': ['sledge', '大锤'],
        'thatcher': ['thatcher', 'emp'],
        'ash': ['ash'],
        'thermite': ['thermite', '热切', '铝热'],
        'montagne': ['montagne', 'monty', '全盾', '大盾'],
        'twitch': ['twitch', '电车', '电车妹'],
        'blitz': ['blitz', '闪盾', '闪光盾'],
        'iq': ['iq'],
        'fuze': ['fuze', '福泽', '咚咚咚', '咚子'],
        'glaz': ['glaz', '狙', '大狙'],
        'buck': ['buck'],
        'blackbeard': ['blackbeard', 'bb', '胡哥', '黑胡子', '枪盾', '步枪盾'],
        'capitao': ['capitao', '开皮条', '队长', '巴西队长', '烧烤哥'],
        'jackal': ['jackal', '足控', '脚气', '豺狼'],
        'ying': ['ying', '莹', '烛光'],
        'zofia': ['zofia', '佐菲亚', '人妻'],
        'dokkaebi': ['dokkaebi', '狗逼', '狗逼小姐姐', '美羊羊']
    }


class Defender(Operator):
    OP_NAME_DICT = {
        'mute': ['mute', 'wifi', 'wi-fi'],
        'smoke': ['smoke', '毒气', '臭屁'],
        'castle': ['castle', '龙鳞板'],
        'pulse': ['pulse', '心跳'],
        'doc': ['doc', '医生', '庸医', '老中医'],
        'rook': ['rook'],
        'jager': ['jager', '杰哥', '耶格', 'ADS'],
        'bandit': ['bandit', '皮卡丘', '班迪', '电兵'],
        'tachanka': ['tachanka', 'lord', '机枪', '机枪哥'],
        'kapkan': ['kapkan', '绊雷', 'edd'],
        'frost': ['frost', '夹子', '夹子妹'],
        'valkrie': ['valkrie', '瓦基', '女武神', '瓦尔基里', '黑眼'],
        'caveira': ['caveira', 'cav', '女鬼', '审问'],
        'echo': ['echo', '死宅'],
        'mira': ['mira', '黑镜'],
        'lesion': ['lesion', '刘醒'],
        'ela': ['ela'],
        'vigil': ['vigil', '伟哥', '白裤裆', '男鬼']
    }


class OperatorQueue:
    REQUEST_PATTERN = '(进攻|防守) +(.+)'

    def __init__(self, url, keyword):
        OperatorQueue.REQUEST_PATTERN = keyword.encode('gbk').decode('utf-8') + '(进攻|防守) +(.+)'
        self.changed = False
        self._dmc = DanMuClient(url)
        if not self._dmc.isValid():
            raise ValueError('Url not valid')

        self._attacker_queue = []
        self._defender_queue = []

        @self._dmc.danmu
        def danmu_fn(msg):
            self.process(msg)

        self._dmc.start(blockThread=False)

    def process(self, msg):
        print('[{0}] \"{1}\"'.format(msg['NickName'], msg['Content']))
        m = re.match(OperatorQueue.REQUEST_PATTERN, msg['Content'])
        if m:
            self.changed = True
            q = self._attacker_queue if m.group(1) == '进攻' else self._defender_queue
            find = False
            for operator in q:
                if operator.match_name(m.group(2)):
                    operator.update(msg['NickName'])
                    find = True
                    break
            if not find:
                try:
                    new_operator = Attacker(m.group(2), msg['NickName']) if m.group(1) == '进攻' \
                        else Defender(m.group(2), msg['NickName'])
                    q.append(new_operator)
                except ValueError as e:
                    print(e)
                    return
            heapq.heapify(q)
            print('    ' + repr(self._attacker_queue))
            print('    ' + repr(self._defender_queue))

    def peek_3(self, side):
        q = self._attacker_queue if side == 'attacker' \
            else self._defender_queue if side == 'defender' else None
        if len(q) < 3:
            return q
        lst = q[0:3]
        if q[1] > q[2]:
            lst[1], lst[2] = q[2], q[1]
        return lst

    def next_attacker(self):
        if len(self._attacker_queue) > 0:
            self._attacker_queue.pop(0)
            self.changed = True
        else:
            print('Attacker queue is empty!')

    def next_defender(self):
        if len(self._defender_queue) > 0:
            self._defender_queue.pop(0)
            self.changed = True
        else:
            print('Defender queue is empty!')

    def get_text(self):
        if not self.changed:
            return None

        self.changed = False
        text_attacker = ''
        for op in self.peek_3('attacker'):
            text_attacker += '    ' + op.name + '\n'
        for _ in range(3 - len(self.peek_3('attacker'))):
            text_attacker += '    --\n'

        text_defender = ''
        for op in self.peek_3('defender'):
            text_defender += '    ' + op.name + '\n'
        for _ in range(3 - len(self.peek_3('defender'))):
            text_defender += '    --\n'

        return [text_attacker.rstrip(), text_defender.rstrip()]


def main():
    q = OperatorQueue('https://live.bilibili.com/4612373')


if __name__ == '__main__':
    main()
