"""
Домашнє завдання #9: Жадібні алгоритми та динамічне програмування
Система здачі грошей для касового апарату

Завдання: Реалізувати два алгоритми для розміну грошей:
1. Жадібний алгоритм - вибирає найбільші номінали спочатку
2. Динамічне програмування - знаходить мінімальну кількість монет
"""

import time
from typing import Dict, List, Tuple
import sys

# Доступні номінали монет (від найбільшого до найменшого)
COINS = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount: int) -> Dict[int, int]:
    """
    Жадібний алгоритм для розміну грошей.
    
    Принцип роботи:
    1. Спочатку використовуємо найбільші номінали
    2. Для кожного номіналу беремо максимальну кількість монет
    3. Переходимо до меншого номіналу з залишком
    
    Args:
        amount (int): Сума для розміну
        
    Returns:
        Dict[int, int]: Словник {номінал: кількість_монет}
    """
    if amount <= 0:
        return {}
    
    result = {}
    remaining = amount
    
    for coin in COINS:
        if remaining >= coin:
            count = remaining // coin  # Цілочисельне ділення
            result[coin] = count
            remaining -= coin * count
            
            # Якщо залишок став 0, можна завершити
            if remaining == 0:
                break
    
    return result

def find_min_coins(amount: int) -> Dict[int, int]:
    """
    Динамічне програмування для знаходження мінімальної кількості монет.
    
    Принцип роботи:
    1. Створюємо таблицю dp, де dp[i] = мінімальна кількість монет для суми i
    2. Для кожної суми розглядаємо всі можливі монети
    3. Вибираємо варіант з мінімальною кількістю монет
    4. Відновлюємо рішення за допомогою зворотного проходу
    
    Args:
        amount (int): Сума для розміну
        
    Returns:
        Dict[int, int]: Словник {номінал: кількість_монет}
    """
    if amount <= 0:
        return {}
    
    # dp[i] = мінімальна кількість монет для суми i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Для суми 0 потрібно 0 монет
    
    # parent[i] = номінал монети, яку використали для отримання суми i
    parent = [-1] * (amount + 1)
    
    # Заповнюємо таблицю dp
    for i in range(1, amount + 1):
        for coin in COINS:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin
    
    # Якщо неможливо скласти суму (теоретично неможливо з нашими номіналами)
    if dp[amount] == float('inf'):
        return {}
    
    # Відновлюємо рішення
    result = {}
    current = amount
    
    while current > 0:
        coin = parent[current]
        result[coin] = result.get(coin, 0) + 1
        current -= coin
    
    return result

def compare_algorithms(amount: int) -> Tuple[Dict[int, int], Dict[int, int], Dict[str, float]]:
    """
    Порівнює продуктивність жадібного алгоритму та динамічного програмування.
    
    Args:
        amount (int): Сума для тестування
        
    Returns:
        Tuple: (результат_жадібного, результат_дп, статистика_часу)
    """
    # Тестуємо жадібний алгоритм
    start_time = time.perf_counter()
    greedy_result = find_coins_greedy(amount)
    greedy_time = time.perf_counter() - start_time
    
    # Тестуємо динамічне програмування
    start_time = time.perf_counter()
    dp_result = find_min_coins(amount)
    dp_time = time.perf_counter() - start_time
    
    timing_stats = {
        'greedy_time': greedy_time,
        'dp_time': dp_time,
        'speedup': dp_time / greedy_time if greedy_time > 0 else float('inf')
    }
    
    return greedy_result, dp_result, timing_stats

def get_total_coins(coin_dict: Dict[int, int]) -> int:
    """Підраховує загальну кількість монет"""
    return sum(coin_dict.values())

def verify_solution(coin_dict: Dict[int, int], target_amount: int) -> bool:
    """Перевіряє правильність рішення"""
    total = sum(coin * count for coin, count in coin_dict.items())
    return total == target_amount

def format_coins(coin_dict: Dict[int, int]) -> str:
    """Форматує словник монет для красивого виводу"""
    if not coin_dict:
        return "Неможливо скласти суму"
    
    # Сортуємо за номіналом (від більшого до меншого)
    sorted_coins = sorted(coin_dict.items(), key=lambda x: x[0], reverse=True)
    return "{" + ", ".join(f"{coin}: {count}" for coin, count in sorted_coins) + "}"

def demonstrate_algorithms():
    """Демонструє роботу алгоритмів на прикладах"""
    print("💰 ДЕМОНСТРАЦІЯ АЛГОРИТМІВ РОЗМІНУ ГРОШЕЙ")
    print("=" * 60)
    print(f"Доступні номінали: {COINS}")
    
    # Тестові суми
    test_amounts = [113, 50, 37, 99, 1, 2, 127, 200]
    
    for amount in test_amounts:
        print(f"\n💵 Сума для розміну: {amount}")
        print("-" * 40)
        
        # Жадібний алгоритм
        greedy_result = find_coins_greedy(amount)
        greedy_total = get_total_coins(greedy_result)
        greedy_valid = verify_solution(greedy_result, amount)
        
        print(f"🏃 Жадібний алгоритм:")
        print(f"   Результат: {format_coins(greedy_result)}")
        print(f"   Загальна кількість монет: {greedy_total}")
        print(f"   Перевірка: {'✅' if greedy_valid else '❌'}")
        
        # Динамічне програмування
        dp_result = find_min_coins(amount)
        dp_total = get_total_coins(dp_result)
        dp_valid = verify_solution(dp_result, amount)
        
        print(f"🧠 Динамічне програмування:")
        print(f"   Результат: {format_coins(dp_result)}")
        print(f"   Загальна кількість монет: {dp_total}")
        print(f"   Перевірка: {'✅' if dp_valid else '❌'}")
        
        # Порівняння
        if greedy_total == dp_total:
            print(f"⚖️  Результат: Однакова кількість монет")
        elif dp_total < greedy_total:
            print(f"🏆 Переможець: ДП (економія {greedy_total - dp_total} монет)")
        else:
            print(f"🏆 Переможець: Жадібний (економія {dp_total - greedy_total} монет)")

def performance_analysis():
    """Аналіз продуктивності алгоритмів"""
    print(f"\n⚡ АНАЛІЗ ПРОДУКТИВНОСТІ")
    print("=" * 50)
    
    # Тести для різних розмірів
    test_sizes = [100, 500, 1000, 2000, 5000, 10000]
    
    print(f"{'Сума':<8} {'Жадібний (мс)':<15} {'ДП (мс)':<12} {'Прискорення':<12} {'Переможець'}")
    print("-" * 65)
    
    for amount in test_sizes:
        greedy_result, dp_result, timing = compare_algorithms(amount)
        
        greedy_ms = timing['greedy_time'] * 1000
        dp_ms = timing['dp_time'] * 1000
        speedup = timing['speedup']
        
        winner = "Жадібний" if greedy_ms < dp_ms else "ДП"
        
        print(f"{amount:<8} {greedy_ms:<15.3f} {dp_ms:<12.3f} {speedup:<12.1f}x {winner}")

def complexity_analysis():
    """Аналіз часової складності алгоритмів"""
    print(f"\n📊 АНАЛІЗ ЧАСОВОЇ СКЛАДНОСТІ")
    print("=" * 50)
    
    print("🏃 Жадібний алгоритм:")
    print("   • Часова складність: O(k), де k - кількість номіналів")
    print("   • Просторова складність: O(k)")
    print("   • Переваги: Дуже швидкий, простий у реалізації")
    print("   • Недоліки: Не завжди дає оптимальне рішення")
    print("   • Для нашого набору монет [50, 25, 10, 5, 2, 1] завжди оптимальний")
    
    print(f"\n🧠 Динамічне програмування:")
    print("   • Часова складність: O(n × k), де n - сума, k - кількість номіналів")
    print("   • Просторова складність: O(n)")
    print("   • Переваги: Завжди знаходить оптимальне рішення")
    print("   • Недоліки: Повільніший для великих сум, потребує більше пам'яті")
    
    print(f"\n🎯 Висновки:")
    print("   • Для малих сум (< 1000): різниця в швидкості незначна")
    print("   • Для великих сум (> 5000): жадібний алгоритм значно швидший")
    print("   • Для нашого набору монет обидва алгоритми дають однакові результати")
    print("   • У реальних касах краще використовувати жадібний алгоритм")

def edge_cases_testing():
    """Тестування граничних випадків"""
    print(f"\n🧪 ТЕСТУВАННЯ ГРАНИЧНИХ ВИПАДКІВ")
    print("=" * 50)
    
    edge_cases = [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 47, 48, 49, 51]
    
    for amount in edge_cases:
        greedy_result = find_coins_greedy(amount)
        dp_result = find_min_coins(amount)
        
        greedy_total = get_total_coins(greedy_result)
        dp_total = get_total_coins(dp_result)
        
        status = "✅" if greedy_total == dp_total else "⚠️"
        
        print(f"{status} Сума {amount:2d}: Жадібний={greedy_total:2d}, ДП={dp_total:2d} | "
              f"Жадібний: {format_coins(greedy_result)}")

def main():
    """Головна функція демонстрації"""
    print("💰 ДОМАШНЄ ЗАВДАННЯ #9: ЖАДІБНІ АЛГОРИТМИ ТА ДИНАМІЧНЕ ПРОГРАМУВАННЯ")
    print("Система розміну грошей для касового апарату")
    print("=" * 80)
    
    # Демонстрація основних прикладів
    demonstrate_algorithms()
    
    # Аналіз продуктивності
    performance_analysis()
    
    # Аналіз складності
    complexity_analysis()
    
    # Тестування граничних випадків
    edge_cases_testing()
    
    print(f"\n🎉 Тестування завершено!")
    print("📋 Основні висновки збережено у файлі README.md")

if __name__ == "__main__":
    main()
