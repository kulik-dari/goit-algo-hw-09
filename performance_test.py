"""
Розширені тести продуктивності для алгоритмів розміну грошей
"""

import time
import random
import matplotlib.pyplot as plt
import numpy as np
from main import find_coins_greedy, find_min_coins, get_total_coins
from typing import List, Tuple

def measure_performance(amounts: List[int], iterations: int = 5) -> Tuple[List[float], List[float]]:
    """
    Вимірює середній час виконання алгоритмів для різних сум.
    
    Args:
        amounts: Список сум для тестування
        iterations: Кількість ітерацій для усереднення
        
    Returns:
        Tuple[List[float], List[float]]: (часи_жадібного, часи_дп)
    """
    greedy_times = []
    dp_times = []
    
    print("🔄 Вимірювання продуктивності...")
    print(f"{'Сума':<8} {'Жадібний (мс)':<15} {'ДП (мс)':<12} {'Прискорення':<12}")
    print("-" * 55)
    
    for amount in amounts:
        # Тестуємо жадібний алгоритм
        greedy_total = 0
        for _ in range(iterations):
            start = time.perf_counter()
            find_coins_greedy(amount)
            greedy_total += time.perf_counter() - start
        avg_greedy = greedy_total / iterations
        greedy_times.append(avg_greedy)
        
        # Тестуємо динамічне програмування
        dp_total = 0
        for _ in range(iterations):
            start = time.perf_counter()
            find_min_coins(amount)
            dp_total += time.perf_counter() - start
        avg_dp = dp_total / iterations
        dp_times.append(avg_dp)
        
        # Розрахунок прискорення
        speedup = avg_dp / avg_greedy if avg_greedy > 0 else float('inf')
        
        print(f"{amount:<8} {avg_greedy*1000:<15.3f} {avg_dp*1000:<12.3f} {speedup:<12.1f}x")
    
    return greedy_times, dp_times

def create_performance_plot(amounts: List[int], greedy_times: List[float], dp_times: List[float]):
    """
    Створює графік порівняння продуктивності алгоритмів.
    """
    try:
        plt.figure(figsize=(15, 10))
        
        # Конвертуємо в мілісекунди для зручності
        greedy_ms = [t * 1000 for t in greedy_times]
        dp_ms = [t * 1000 for t in dp_times]
        
        # Графік 1: Лінійна шкала
        plt.subplot(2, 2, 1)
        plt.plot(amounts, greedy_ms, 'b-o', label='Жадібний алгоритм', linewidth=2)
        plt.plot(amounts, dp_ms, 'r-s', label='Динамічне програмування', linewidth=2)
        plt.xlabel('Сума для розміну')
        plt.ylabel('Час виконання (мс)')
        plt.title('Порівняння часу виконання (лінійна шкала)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Графік 2: Логарифмічна шкала
        plt.subplot(2, 2, 2)
        plt.loglog(amounts, greedy_ms, 'b-o', label='Жадібний алгоритм')
        plt.loglog(amounts, dp_ms, 'r-s', label='Динамічне програмування')
        plt.xlabel('Сума (логарифмічна шкала)')
        plt.ylabel('Час (мс, логарифмічна шкала)')
        plt.title('Порівняння у логарифмічній шкалі')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Графік 3: Прискорення
        plt.subplot(2, 2, 3)
        speedup = [dp / greedy for dp, greedy in zip(dp_times, greedy_times)]
        plt.plot(amounts, speedup, 'g-^', linewidth=2, markersize=8)
        plt.xlabel('Сума для розміну')
        plt.ylabel('Прискорення (разів)')
        plt.title('Прискорення жадібного алгоритму відносно ДП')
        plt.grid(True, alpha=0.3)
        
        # Графік 4: Стовпчаста діаграма
        plt.subplot(2, 2, 4)
        x = np.arange(len(amounts))
        width = 0.35
        
        plt.bar(x - width/2, greedy_ms, width, label='Жадібний', alpha=0.8, color='blue')
        plt.bar(x + width/2, dp_ms, width, label='ДП', alpha=0.8, color='red')
        plt.xlabel('Суми для тестування')
        plt.ylabel('Час виконання (мс)')
        plt.title('Порівняння по тестах')
        plt.xticks(x, [str(a) for a in amounts])
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("📊 Графік збережено як 'performance_comparison.png'")
        
    except ImportError:
        print("⚠️  Matplotlib не встановлено. Графік не створено.")
    except Exception as e:
        print(f"❌ Помилка при створенні графіка: {e}")

def memory_usage_analysis():
    """
    Аналіз використання пам'яті алгоритмами.
    """
    import sys
    
    print("\n📊 АНАЛІЗ ВИКОРИСТАННЯ ПАМ'ЯТІ")
    print("=" * 40)
    
    amounts = [100, 1000, 5000, 10000]
    
    print(f"{'Сума':<8} {'Жадібний (bytes)':<18} {'ДП (bytes)':<15} {'Співвідношення'}")
    print("-" * 60)
    
    for amount in amounts:
        # Жадібний алгоритм
        result_greedy = find_coins_greedy(amount)
        greedy_memory = sys.getsizeof(result_greedy)
        
        # Динамічне програмування (приблизна оцінка)
        # ДП використовує масив розміру amount + 1
        dp_memory_estimate = amount * 8  # 8 bytes per int
        
        ratio = dp_memory_estimate / greedy_memory if greedy_memory > 0 else 0
        
        print(f"{amount:<8} {greedy_memory:<18} {dp_memory_estimate:<15} {ratio:<12.1f}x")

def stress_testing():
    """
    Стрес-тестування алгоритмів на великих сумах.
    """
    print("\n🔥 СТРЕС-ТЕСТУВАННЯ")
    print("=" * 30)
    
    large_amounts = [50000, 100000, 200000, 500000]
    
    print("Тестування на великих сумах...")
    print(f"{'Сума':<10} {'Жадібний (мс)':<15} {'Статус'}")
    print("-" * 40)
    
    for amount in large_amounts:
        try:
            start = time.perf_counter()
            result = find_coins_greedy(amount)
            duration = time.perf_counter() - start
            
            total_coins = get_total_coins(result)
            status = f"✅ {total_coins} монет"
            
            print(f"{amount:<10} {duration*1000:<15.3f} {status}")
            
        except Exception as e:
            print(f"{amount:<10} {'ERROR':<15} ❌ {str(e)}")
    
    print("\nПримітка: ДП не тестується на великих сумах через обмеження пам'яті")

def algorithm_correctness_test():
    """
    Тестування правильності алгоритмів.
    """
    print("\n🧪 ТЕСТУВАННЯ ПРАВИЛЬНОСТІ")
    print("=" * 35)
    
    # Генеруємо випадкові суми для тестування
    test_amounts = [random.randint(1, 1000) for _ in range(20)]
    test_amounts.extend([1, 2, 3, 50, 99, 100, 113, 999])  # Додаємо специфічні випадки
    
    mismatches = 0
    total_tests = len(test_amounts)
    
    print("Перевіряємо, чи дають алгоритми однакові результати...")
    
    for amount in test_amounts:
        greedy_result = find_coins_greedy(amount)
        dp_result = find_min_coins(amount)
        
        greedy_total = get_total_coins(greedy_result)
        dp_total = get_total_coins(dp_result)
        
        if greedy_total != dp_total:
            mismatches += 1
            print(f"❌ Сума {amount}: Жадібний={greedy_total}, ДП={dp_total}")
    
    success_rate = (total_tests - mismatches) / total_tests * 100
    print(f"\n📊 Результати тестування:")
    print(f"   • Всього тестів: {total_tests}")
    print(f"   • Співпадінь: {total_tests - mismatches}")
    print(f"   • Розбіжностей: {mismatches}")
    print(f"   • Відсоток успіху: {success_rate:.1f}%")
    
    if mismatches == 0:
        print("✅ Всі тести пройдені! Алгоритми дають однакові результати.")
    else:
        print("⚠️  Виявлено розбіжності. Потрібна додаткова перевірка.")

def main():
    """
    Головна функція для запуску тестів продуктивності.
    """
    print("⚡ РОЗШИРЕНІ ТЕСТИ ПРОДУКТИВНОСТІ")
    print("Алгоритми розміну грошей")
    print("=" * 50)
    
    # Тестування правильності
    algorithm_correctness_test()
    
    # Основні тести продуктивності
    test_amounts = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    greedy_times, dp_times = measure_performance(test_amounts)
    
    # Створення графіків
    create_performance_plot(test_amounts, greedy_times, dp_times)
    
    # Аналіз пам'яті
    memory_usage_analysis()
    
    # Стрес-тестування
    stress_testing()
    
    print(f"\n🎉 Тестування завершено!")
    print("📋 Результати:")
    print("   • Жадібний алгоритм стабільно швидший")
    print("   • Для нашого набору монет обидва алгоритми оптимальні")
    print("   • ДП має обмеження по пам'яті для великих сум")

if __name__ == "__main__":
    main()
