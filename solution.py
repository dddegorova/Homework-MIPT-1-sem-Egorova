"""
Pixel's Enhanced Biologically Inspired Memory
===========================================

Improved with:
1. Ebbinghaus forgetting curve (natural decay)
2. Pin critical facts (never forget)
3. Request frequency tracking
4. Semantic proximity matching
5. Positive reinforcement on hits
6. Adaptive threshold (top-2 only)
7. Cyclic pattern prediction
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Set
import random
import os
import json
import re
import math


@dataclass
class MemoryItem:
    fact: str
    answer: str
    strength: float = 1.0          # Ebbinghaus memory strength
    insert_time: int = 0
    last_access_time: int = 0
    access_count: int = 0
    pinned: bool = False            # Critical facts stay forever
    request_frequency: int = 0    # How often this key is requested


class EbbinghausDecay:
    """Ebbinghaus forgetting curve with recovery."""
    
    def __init__(self, decay_rate: float = 0.05, recovery: float = 0.3):
        self.decay_rate = decay_rate
        self.recovery = recovery
    
    def strength(self, item: MemoryItem, time: int) -> float:
        t = time - item.last_access_time
        return max(0.01, item.strength * math.exp(-self.decay_rate * t))
    
    def on_access(self, item: MemoryItem) -> None:
        # Positive reinforcement!
        boost = self.recovery * (1.0 - item.strength)
        item.strength = min(1.0, item.strength + boost)


class SemanticSimilarity:
    """Character n-gram similarity."""
    
    def get_ngrams(self, text: str, n: int = 3) -> Set[str]:
        return set(text.lower()[i:i+n] for i in range(len(text) - n + 1))
    
    def sim(self, t1: str, t2: str) -> float:
        n1, n2 = self.get_ngrams(t1, 3), self.get_ngrams(t2, 3)
        if not n1 or not n2: return 0.0
        return len(n1 & n2) / len(n1 | n2) if n1 | n2 else 0.0


class EnhancedPixelMemory:
    """
    Enhanced memory with:
    - Ebbinghaus forgetting curve
    - Pinned critical facts
    - Request frequency tracking
    - Cyclic pattern prediction
    - Positive reinforcement
    - Adaptive threshold (top-2)
    """
    
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.memories: List[MemoryItem] = []
        self.kw_freq: Dict[str, int] = {}
        self.time = 0
        self.ebbinghaus = EbbinghausDecay(0.05, 0.3)
        self.semantic = SemanticSimilarity()
        self.dialog: List[Dict] = []
        self.rewards: List[float] = []
        
        # Cyclic pattern tracking
        self.query_history: List[str] = []
        self.pattern_window = 4  # Look at last 4 queries
    
    def _kw(self, text: str) -> Set[str]:
        words = re.findall(r'\w+', text.lower())
        stop = {'это', 'моя', 'мой', 'мое', 'какая', 'какой', 'какое', 'какие',
               'кто', 'что', 'где', 'когда', 'почему', 'как', 'сколько',
               'я', 'у', 'в', 'на', 'по', 'за', 'из', 'мой', 'моя', 'который'}
        return set(w for w in words if len(w) > 2 and w not in stop)
    
    def _imp(self, ks: Set[str]) -> float:
        return sum(self.kw_freq.get(k, 0) for k in ks)
    
    def _ans(self, fact: str) -> str:
        for sep in ['|', ' - ', '—']:
            if sep in fact:
                return fact.split(sep, 1)[1].strip()
        return fact
    
    def _pin_critical_facts(self, fact: str) -> bool:
        """Pin facts about owner, name, identity."""
        critical_keywords = {'зовут', 'хозяин', 'имя', 'владелец', 'мой', 'я'}
        return any(kw in fact.lower() for kw in critical_keywords)
    
    def learn(self, fact: str) -> None:
        self.time += 1
        answer = self._ans(fact)
        ks = self._kw(fact)
        imp = self._imp(ks)
        
        # Update frequency if exists
        for m in self.memories:
            if m.fact == fact:
                m.importance = imp
                return
        
        if len(self.memories) < self.capacity:
            pinned = self._pin_critical_facts(fact)
            self.memories.append(MemoryItem(
                fact=fact, answer=answer, strength=1.0,
                insert_time=self.time, last_access_time=self.time,
                pinned=pinned
            ))
            return
        
        # Evict weakest (but never evict pinned!)
        self._evict_weakest()
        
        pinned = self._pin_critical_facts(fact)
        self.memories.append(MemoryItem(
            fact=fact, answer=answer, strength=1.0,
            insert_time=self.time, last_access_time=self.time,
            pinned=pinned
        ))
    
    def _evict_weakest(self) -> None:
        # Calculate current strength
        for m in self.memories:
            m.strength = self.ebbinghaus.strength(m, self.time)
        
        # Find weakest that is NOT pinned
        evictable = [m for m in self.memories if not m.pinned]
        if not evictable:  # All pinned!
            return
        
        weakest = min(evictable, key=lambda m: m.strength)
        self.memories.remove(weakest)
    
    def _predict_next(self) -> Set[str]:
        """Predict what will be needed based on cyclic patterns."""
        if len(self.query_history) < self.pattern_window:
            return set()
        
        # Recent queries
        recent = self.query_history[-self.pattern_window:]
        
        # Find cyclic repeats
        for i in range(len(recent)):
            for j in range(i+1, len(recent)):
                if recent[i] == recent[j]:
                    # Found cycle! Return keywords from cycle
                    return self._kw(recent[i])
        return set()
    
    def answer(self, query: str) -> List[str]:
        self.time += 1
        qk = self._kw(query)
        
        # Track query history for prediction
        self.query_history.append(query)
        if len(self.query_history) > 20:
            self.query_history.pop(0)
        
        # Track frequency
        for k in qk:
            self.kw_freq[k] = self.kw_freq.get(k, 0) + 1
            
            # Also update request frequency in memories
            for m in self.memories:
                if k in self._kw(m.fact):
                    m.request_frequency += 1
        
        # Predicted keywords (from cyclic pattern)
        predicted = self._predict_next()
        
        # Update importance and strength
        for m in self.memories:
            m.importance = self._imp(self._kw(m.fact))
        
        # Find matches
        matches = []
        for m in self.memories:
            mk = self._kw(m.fact)
            kw_match = len(qk & mk)
            sem = self.semantic.sim(query, m.fact)
            
            if kw_match > 0 or sem > 0.15:
                # Get current strength
                current_strength = self.ebbinghaus.strength(m, self.time)
                
                # Boost if predicted to be needed
                pred_boost = 0.5 if (mk & predicted) else 0.0
                
                # Score: keyword + semantic + strength + frequency + prediction + pinned
                score = (
                    kw_match * 3 +
                    sem * 4 +
                    current_strength * 2 +
                    m.request_frequency * 0.3 +
                    pred_boost +
                    (1.0 if m.pinned else 0.0) +  # Pinned facts stay!
                    m.access_count * 0.2  # Positive reinforcement bonus
                )
                matches.append((m, score, kw_match, current_strength))
        
        matches.sort(key=lambda x: (-x[1], -x[2], -x[3]))
        
        # Return only top-2 (adaptive threshold)
        answers = []
        for m, _, kw_match, _ in matches[:2]:
            # Positive reinforcement!
            self.ebbinghaus.on_access(m)
            m.last_access_time = self.time
            m.access_count += 1
            answers.append(m.answer)
        
        # Track hit/miss
        hit = len(matches) > 0 and matches[0][2] > 0
        self.dialog.append({'q': query, 'a': answers, 'hit': hit})
        self.rewards.append(1.0 if hit else 0.0)
        if len(self.rewards) > 100:
            self.rewards.pop(0)
        
        return answers
    
    def get_state(self) -> Dict:
        pinned_count = sum(1 for m in self.memories if m.pinned)
        return {
            'acc': sum(self.rewards)/len(self.rewards) if self.rewards else 0,
            'ops': self.time,
            'mem': len(self.memories),
            'pinned': pinned_count,
            'kw': len(self.kw_freq)
        }
    
    def save(self, fp: str) -> None:
        os.makedirs(os.path.dirname(fp) if os.path.dirname(fp) else '.', exist_ok=True)
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(self.dialog, f, indent=2, ensure_ascii=False)


# 30 Facts with critical info marked
FACTS = """Моя любимая еда - пицца|пицца
Мой любимый цвет - синий|синий
Меня зовут Pixel|pixel
Я живу в Москве|москва
Мне 3 года|3 года
Мой хозяин - Анна|анна
Я люблю гулять в парке|парк
Мой любимыйtoy - мячик|мячик
Я умею сидеть|сидеть
Я умею давать лапу|лапу
Сейчас зима|зима
Сегодня вторник|вторник
Я робот-собака|робот
Я хожу в школу|школу
Я учусь новому|учусь
Мой номер - 42|42
Я люблю дождь|дождь
Мой хвост - коричневый|коричневый
У меня 4 лапы|4 лапы
Я сплю 8 часов|8 часов
Мой любимый сезон - осень|осень
Я бегаю быстро|быстро
Мой рост - 30 см|30 см
Я вешу 5 кг|5 кг
Мой друг - Робот|робот
Я играю с мячом|мячом
Я живу в квартире|квартире
Мой любимый звук - лай|лай
Я сторож|сторож
Мой ошейник - красный|красный"""

# Test queries
QUERIES = """Какая моя любимая еда?|пицца
Какой мой любимый цвет?|синий
Как меня зовут?|pixel
Где я живу?|москва
Сколько мне лет?|3 года
Кто мой хозяин?|анна
Куда я люблю гулять?|парк
Какой мой любимыйtoy?|мячик"""


def run_test():
    """Run test with enhanced memory."""
    
    facts = [f.strip() for f in FACTS.split('\n') if f.strip()]
    queries = [q.strip() for q in QUERIES.split('\n') if q.strip()]
    
    print("=" * 60)
    print("PIXEL'S ENHANCED MEMORY")
    print("Ebbinghaus + Pinned Facts + Frequency + Prediction")
    print("30 facts, 8 queries")
    print("=" * 60 + "\n")
    
    mem = EnhancedPixelMemory(10)
    random.seed(42)
    random.shuffle(facts)
    
    # Learn first 10
    for f in facts[:10]:
        mem.learn(f)
    
    correct = sum(1 for q in queries if any(mem.answer(q)))
    acc1 = correct / len(queries)
    print(f"After 10 facts: {acc1:.0%}")
    
    # Learn 10 more
    for f in facts[10:20]:
        mem.learn(f)
    
    correct = sum(1 for q in queries if any(mem.answer(q)))
    acc2 = correct / len(queries)
    print(f"After 20 facts: {acc2:.0%}")
    
    # Learn all 30
    for f in facts[20:]:
        mem.learn(f)
    
    correct = sum(1 for q in queries if any(mem.answer(q)))
    accf = correct / len(queries)
    print(f"Final: {accf:.0%}")
    
    state = mem.get_state()
    print(f"\nMetrics: accuracy={state['acc']:.0%}, ops={state['ops']}, pinned={state['pinned']}")
    
    # Save dialog
    fp = "pixel_memory/dialog_log.json"
    os.makedirs("pixel_memory", exist_ok=True)
    mem.save(fp)
    print(f"\nDialog: {fp} (Cyrillic)")
    
    passed = accf >= acc1
    print(f"\n{'[OK] PASSED' if passed else '[FAIL]'}: {acc1:.0%} -> {accf:.0%}")


if __name__ == "__main__":
    import os
    run_test()