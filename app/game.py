import random
from enum import Enum
from collections import Counter


class CardType(Enum):
    SINGLE = 1  # 单张
    PAIR = 2  # 对子
    TRIPLE = 3  # 三张
    TRIPLE_WITH_ONE = 4  # 三带一
    TRIPLE_WITH_TWO = 5  # 三带二
    STRAIGHT = 6  # 顺子
    BOMB = 7  # 炸弹
    ROCKET = 8  # 王炸


order = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
         'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15, 'B': 16, 'R': 17}
suits = ['S', 'H', 'D', 'C']
ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
whole_pokers = [r + s for s in suits for r in ranks] + ['BJ', 'RJ']  # BJ=小王，RJ=大王


def sort_card(cards):
    return sorted(cards, key=lambda x: order[x[0]], reverse=True)


def identify_card_type(cards):
    """识别牌型"""
    count = Counter(cards)
    values = [order[c[0]] for c in cards]
    values.sort()

    # 火箭（王炸）
    if set(cards) == {'BJ', 'RJ'}:
        return (CardType.ROCKET, 0)

    # 炸弹
    if len(cards) == 4 and len(set(values)) == 1:
        return (CardType.BOMB, values[0])

    # 单张
    if len(cards) == 1:
        return (CardType.SINGLE, values[0])

    # 对子
    if len(cards) == 2 and values[0] == values[1]:
        return (CardType.PAIR, values[0])

    # 三张系列
    if 3 in count.values():
        triple_value = [v for v, c in count.items() if c == 3][0]
        # 三带一
        if len(cards) == 4:
            return (CardType.TRIPLE_WITH_ONE, triple_value)
        # 三带二
        if len(cards) == 5 and 2 in count.values():
            return (CardType.TRIPLE_WITH_TWO, triple_value)
        # 纯三张
        if len(cards) == 3:
            return (CardType.TRIPLE, triple_value)

    # 顺子（至少5张连续）
    if len(values) >= 5 and all(values[i + 1] - values[i] == 1 for i in range(len(values) - 1)):
        return (CardType.STRAIGHT, len(values))
    return None  # 无效牌型


def compare(last_type, current_type):
    """比较两次出牌的大小"""
    # 火箭最大
    if current_type[0] == CardType.ROCKET:
        return True
    # 炸弹压制非火箭牌
    if current_type[0] == CardType.BOMB:
        if last_type[0] != CardType.BOMB:
            return True
        return current_type[1] > last_type[1]
    # 同类牌比较
    if current_type[0] == last_type[0]:
        return current_type[1] > last_type[1]
    return False


class Game:
    def __init__(self):
        # 初始化牌组
        self.winner = None
        self.players = {0: [], 1: [], 2: []}
        self.landlord = None  # 地主玩家
        self.current_player = 0  # 当前出牌玩家
        self.last_played = {}  # 上家出的牌
        self.game_phase = "deal"  # 游戏阶段：deal/bid/play/end
        self.deck = []
        self._create_deck()
        self.discards = []  # 已出牌堆

        # 发牌
        self._deal_cards()
        self.game_phase = "bid"

    def _create_deck(self):
        """创建一副牌（包括大小王）"""
        self.deck = whole_pokers
        random.shuffle(self.deck)

    def _deal_cards(self):
        """发牌逻辑"""
        for player in self.players.keys():
            start_index = player * 17
            end_index = start_index + 17
            self.players[player] = self.deck[start_index:end_index]
            self.players[player] = sort_card(self.players[player])
        self.bottom_cards = self.deck[-3:]  # 取最后三张作为底牌

    def bid_landlord(self, player, bid_level):
        """
        叫地主逻辑
        :param player: 玩家ID (0-2)
        :param bid_level: 叫分级别 (0不叫，1/2/3分)
        :return: 是否叫地主成功
        """
        if self.game_phase != "bid":
            return False

        if bid_level > 0:
            self.landlord = player
            # 分配底牌
            self.players[player].extend(self.bottom_cards)
            self.players[player].sort()
            self.current_player = player
            self.game_phase = "play"
            return True
        return False

    def play_cards(self, player, cards):
        """
        出牌逻辑
        :param player: 玩家ID
        :param cards: 出的牌列表
        :return: 是否出牌成功
        """
        if not self._validate_play(player, cards):
            return False

        # 移除手牌
        for card in cards:
            self.players[player].remove(card)

        # 更新游戏状态
        if cards:  # 非过牌
            self.last_played = {
                'player': player,
                'cards': cards,
                'type': identify_card_type(cards)
            }
        self.discards.extend(cards)

        # 检查胜利条件
        if not self.players[player]:
            self.game_phase = "end"
            self.winner = "landlord" if player == self.landlord else "farmers"
            return True

        # 轮转玩家
        self.current_player = (player + 1) % 3
        return True

    def _validate_play(self, player, cards):
        """验证出牌合法性"""
        # 基础验证
        if player != self.current_player:
            return False
        if not all(card in self.players[player] for card in cards):
            return False

        # 过牌验证
        if not cards:
            return bool(self.last_played)  # 必须有人出过牌才能过

        # 牌型验证
        card_type = identify_card_type(cards)
        if not card_type:
            return False

        # 比较牌力
        if self.last_played:
            last_type = self.last_played['type']
            if not compare(last_type, card_type):
                return False
        return True

    def get_game_state(self, player):
        """获取游戏状态（玩家视角）"""
        return {
            'hand': sorted(self.players[player]),
            'current_player': self.current_player,
            'last_played': self.last_played,
            'phase': self.game_phase,
            'landlord': self.landlord,
            'remaining': {p: len(cards) for p, cards in self.players.items()}
        }
