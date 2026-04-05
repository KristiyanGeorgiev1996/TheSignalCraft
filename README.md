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

Системата не изпълнява автоматично сделки. Вместо това:
- извлича пазарни данни  
- прилага технически индикатори  
- оценява сигнала чрез скоринг модел  
- изчислява вероятност за достигане на TP преди SL  
- връща структурирано решение  

---

## Снимки

> Постави изображенията в папката `screenshots/`

### Анализ на сигнал
![Signal analysis](screenshots/signal-analysis.png)

### Структура на проекта
![Structure](screenshots/project-structure.png)

### Взаимодействие с бота
![Bot](screenshots/bot-interaction.png)

---

## Основни функционалности

- 📊 Анализ на пазарни данни (multi-timeframe)  
- 📈 Технически индикатори (EMA, RSI, MACD, ATR, ADX, Bollinger Bands)  
- 🧠 Скоринг система за оценка на сигнала  
- 🎯 Вероятностен модел (TP vs SL)  
- ⏱️ Оценка на продължителност  
- 🗂️ Запис на резултати (CSV + SQLite)  
- ⚙️ Модулна архитектура  

---

## 🔄 Аналитичен поток

```text
Signal Input
     ↓
Parsing (signal_parser)
     ↓
Market Data (yfinance)
     ↓
Indicators (EMA, RSI, MACD, ATR, ADX)
     ↓
Scoring Engine
     ↓
Probability Model
     ↓
Final Decision
     ↓
Logging
