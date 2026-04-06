"""Программа для анализа погоды с использованием pandas и matplotlib"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

def generate_weather_data():
    """Генерирует данные о погоде за неделю"""
    # Данные за последнюю неделю
    end_date = datetime.now()
    dates = [end_date - timedelta(days=i) for i in range(6, -1, -1)]
    
    # Случайные температуры для демонстрации (в реальности можно загрузить из API)
    weather_data = {
        'Дата': [d.strftime('%Y-%m-%d') for d in dates],
        'День_недели': [d.strftime('%A') for d in dates],
        'Температура_днем': [random.randint(15, 30) for _ in range(7)],
        'Температура_ночью': [random.randint(5, 18) for _ in range(7)],
        'Осадки_мм': [round(random.uniform(0, 15), 1) for _ in range(7)],
        'Влажность_%': [random.randint(40, 90) for _ in range(7)]
    }
    
    return pd.DataFrame(weather_data)

def create_weather_chart(df):
    """Создает график температуры за неделю"""
    # Настройка стиля
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Создаем фигуру с двумя подграфиками
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # График температуры
    dates = df['Дата']
    ax1.plot(dates, df['Температура_днем'], marker='o', linewidth=2, 
             markersize=8, label='Дневная температура', color='red')
    ax1.plot(dates, df['Температура_ночью'], marker='s', linewidth=2, 
             markersize=8, label='Ночная температура', color='blue')
    
    ax1.set_xlabel('Дата', fontsize=12)
    ax1.set_ylabel('Температура (°C)', fontsize=12)
    ax1.set_title('Температура за неделю', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Поворачиваем подписи дат для лучшей читаемости
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # График осадков и влажности
    x = range(len(df))
    width = 0.35
    
    bars1 = ax2.bar([i - width/2 for i in x], df['Осадки_мм'], width, 
                    label='Осадки (мм)', color='cyan', alpha=0.7)
    ax2.set_ylabel('Осадки (мм)', color='cyan', fontsize=12)
    
    # Создаем вторую ось Y для влажности
    ax2_twin = ax2.twinx()
    bars2 = ax2_twin.bar([i + width/2 for i in x], df['Влажность_%'], width,
                         label='Влажность (%)', color='orange', alpha=0.7)
    ax2_twin.set_ylabel('Влажность (%)', color='orange', fontsize=12)
    
    ax2.set_xlabel('Дата', fontsize=12)
    ax2.set_title('Осадки и влажность за неделю', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df['Дата'], rotation=45, ha='right')
    
    # Добавляем значения на столбцы
    for bar, value in zip(bars1, df['Осадки_мм']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{value}', ha='center', va='bottom', fontsize=9)
    
    for bar, value in zip(bars2, df['Влажность_%']):
        ax2_twin.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                     f'{value}', ha='center', va='bottom', fontsize=9)
    
    # Добавляем легенду
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.suptitle('Анализ погоды за неделю', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Сохраняем график
    plt.savefig('weather_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_statistics(df):
    """Выводит статистику по данным о погоде"""
    print("\n" + "="*60)
    print("СТАТИСТИКА ПОГОДЫ ЗА НЕДЕЛЮ")
    print("="*60)
    print(df.to_string(index=False))
    
    print("\n" + "-"*60)
    print("ОСНОВНЫЕ ПОКАЗАТЕЛИ:")
    print("-"*60)
    print(f"Средняя дневная температура: {df['Температура_днем'].mean():.1f}°C")
    print(f"Максимальная дневная температура: {df['Температура_днем'].max()}°C")
    print(f"Минимальная дневная температура: {df['Температура_днем'].min()}°C")
    print(f"Средняя ночная температура: {df['Температура_ночью'].mean():.1f}°C")
    print(f"Общее количество осадков: {df['Осадки_мм'].sum():.1f} мм")
    print(f"Средняя влажность: {df['Влажность_%'].mean():.1f}%")
    
    # День с самой высокой температурой
    hottest_day = df.loc[df['Температура_днем'].idxmax()]
    print(f"\n☀️ Самый жаркий день: {hottest_day['Дата']} ({hottest_day['День_недели']}) - {hottest_day['Температура_днем']}°C")
    
    # День с наибольшими осадками
    rainiest_day = df.loc[df['Осадки_мм'].idxmax()]
    print(f"🌧️ Самый дождливый день: {rainiest_day['Дата']} ({rainiest_day['День_недели']}) - {rainiest_day['Осадки_мм']} мм")

def main():
    """Основная функция программы"""
    print("Создание DataFrame с данными о погоде...")
    
    # Генерируем данные
    df = generate_weather_data()
    
    # Выводим статистику
    print_statistics(df)
    
    # Создаем график
    print("\nСоздание графика температуры...")
    create_weather_chart(df)
    
    print("\n✅ Анализ завершен! График сохранен как 'weather_analysis.png'")

if __name__ == "__main__":
    main()