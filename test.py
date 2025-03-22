import random
# import yaml
import json
from pathlib import Path

class WordMemoryTest:
    def __init__(self, word_list, history_file='history.json'):
        self.word_list = word_list
        self.history_file = Path(history_file)
        self.history = self._load_history()
        self.last_word = None

    def _load_history(self):
        """加载历史记录"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f) or {}
        return {}

    def _save_history(self):
        """保存历史记录"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def _update_history(self, word, remembered):
        """更新单词记忆数据"""
        if word not in self.history:
            self.history[word] = [0, 0]
        self.history[word][0] += 1  # 总次数
        if not remembered:
            self.history[word][1] += 1  # 忘记次数

    def _get_weights(self):
        """生成权重列表（排除当前单词）"""
        candidates = [w for w in self.word_list if w != self.last_word]
        return [self.history.get(w, [0,0])[1] + 1 for w in candidates]

    def run(self):
        """运行测试"""
        # 合并新单词到历史记录
        for word in self.word_list:
            if word not in self.history:
                self.history[word] = [0, 0]

        while True:
            # 生成候选列表和权重
            candidates = [w for w in self.word_list if w != self.last_word]
            weights = self._get_weights()
            
            if not candidates:  # 处理只剩一个单词的情况
                candidates = self.word_list
                weights = [self.history[w][1]+1 for w in candidates]

            # 加权随机选择
            chosen = random.choices(candidates, weights=weights, k=1)[0]
            self.last_word = chosen
            
            # 用户交互
            print(f"\n当前单词：{chosen}")
            action = input("记得按y，忘记按n，退出按q：").lower()
            
            if action == 'q':
                self._save_history()
                print("已保存学习记录")
                break
            elif action in ('y', 'n'):
                self._update_history(chosen, action == 'y')
                

def load_words_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f).keys()

# 使用示例
if __name__ == "__main__":
    # 你的单词列表（示例）
    words = load_words_from_json('history.json')
    
    test = WordMemoryTest(words)
    test.run()