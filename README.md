# TheSignalCraft

<p align="center">
  <b>Превръщане на сурови сигнали в обосновани решения.</b>
</p>

<p align="center">
  Модулен Python проект за оценка на трейдинг сигнали чрез технически анализ, скоринг логика и вероятностно базирана подкрепа при вземане на решения.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/architecture-modular-success">
  <img src="https://img.shields.io/badge/focus-signal%20evaluation-informational">
  <img src="https://img.shields.io/badge/domain-trading-orange">
  <img src="https://img.shields.io/badge/data-yfinance-lightgrey">
  <img src="https://img.shields.io/github/license/KristiyanGeorgiev1996/TheSignalCraft">
  <img src="https://img.shields.io/github/repo-size/KristiyanGeorgiev1996/TheSignalCraft">
  <img src="https://img.shields.io/github/last-commit/KristiyanGeorgiev1996/TheSignalCraft">
</p>

---

## Обща информация

**TheSignalCraft** е модулен проект за оценка на трейдинг сигнали, създаден с цел подпомагане на анализа на ръчно подадени сигнали.

Вместо да изпълнява автоматично сделки, системата обработва сигнал, извлича пазарни данни, прилага технически индикатори, оценява setup-а чрез скоринг модел, изчислява вероятността take-profit да бъде достигнат преди stop-loss и връща структурирано решение.

Целта не е да замени човешката преценка, а да подпомогне по-дисциплиниран и информиран анализ.

---

## Снимки

> Запази изображенията в папката `screenshots/` със същите имена.

### 1. Анализ на сигнал
![Signal analysis output](screenshots/signal-analysis.png)

### 2. Структура на проекта
![Project structure](screenshots/project-structure.png)

### 3. Взаимодействие с бота
![Bot interaction](screenshots/bot-interaction.png)

---

## Основни функционалности

- Ръчно подаване и парсване на сигнали чрез Telegram
- Анализ на пазарни данни в различни времеви рамки
- Изчисляване на технически индикатори:
  - EMA 20 / 50 / 200
  - RSI
  - ATR
  - ADX
  - MACD
  - Bollinger Bands
- Оценка на сигнал чрез скоринг система
- Изчисляване на вероятност TP да бъде достигнат преди SL
- Оценка на очаквана продължителност на сделката
- Запис на резултати (CSV + SQLite)
- Модулна архитектура за лесно разширяване

---

## Как работи

Системата следва следния процес:

1. Подаване на сигнал  
2. Парсване на входа  
3. Извличане на пазарни данни  
4. Добавяне на индикатори  
5. Оценка чрез скоринг логика  
6. Изчисляване на вероятност  
7. Генериране на финално решение  
8. Запис на резултата  

---

## Модел на вземане на решения

Сигналите се класифицират в четири категории:

- REJECT (отхвърляне)
- RISKY (рисков)
- ACCEPT (приемлив)
- STRONG TRADE (силен сетъп)

Решението се базира на комбинация от фактори като тренд, momentum, риск/печалба, структура на пазара и вероятност.

---

## Технологии

- Python  
- pandas  
- numpy  
- yfinance  
- ta (technical analysis)  
- python-telegram-bot  
- SQLite  
- CSV  

---

## Структура на проекта

```text
TheSignalCraft/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── indicators.py
│   ├── instrument_profiles.py
│   ├── logger.py
│   ├── market_data.py
│   ├── probability_model.py
│   ├── scoring.py
│   ├── signal_parser.py
│   └── symbol_mapper.py
├── screenshots/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
