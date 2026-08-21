import ast
import os
import sys
import traceback
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Импорт библиотеки Gemini API
try:
  from google import genai
  from google.genai import types

  GENAI_AVAILABLE = True
except ImportError:
  GENAI_AVAILABLE = False


# ==========================================
# 1. СТАТИЧЕСКИЙ АНАЛИЗ КОДА (AST)
# ==========================================
class CodeAnalyzer:
  """Модуль быстрой проверки синтаксиса без вызова сторонних API."""

  @staticmethod
  def check_syntax(code_str: str):
    try:
      parsed_ast = ast.parse(code_str)
      return (
          True,
          "Синтаксических ошибок не обнаружено.",
          None,
          parsed_ast,
      )
    except SyntaxError as e:
      error_details = {
          "line": e.lineno,
          "offset": e.offset,
          "text": e.text,
          "msg": e.msg,
      }
      return (
          False,
          f"Синтаксическая ошибка на строке {e.lineno}",
          error_details,
          None,
      )

  @staticmethod
  def get_complexity(node):
    """Расчет цикломатической сложности кода (количество ветвлений)."""
    complexity = 1
    for child in ast.walk(node):
      if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or)):
        complexity += 1
    return complexity


# ==========================================
# 2. ИИ-МОДУЛЬ: СОКРАТОВСКИЕ ПОДСКАЗКИ (ГИБРИД)
# ==========================================
SYSTEM_INSTRUCTION = """
Ты — педагогический ИИ-ассистент по информатике «Code Mentor AI». Твоя цель — помогать ученикам находить ошибки в коде с помощью Сократовского диалога.

СТРОГИЕ ПРАВИЛА:
1. НИКОГДА НЕ ДАВАЙ ГОТОВЫЙ ИСПРАВЛЕННЫЙ КОД ИЛИ ПРЯМОЙ ОТВЕТ!
2. Задавай 1–2 наводящих вопроса, которые подтолкнут ученика к самостоятельному анализу проблемы.
3. Общайся поддерживающе, понятным для школьника языком.
4. Если видишь логическую ошибку или runtime-ошибку (TypeError, NameError и т.д.), задай вопрос по смыслу этой ошибки.
"""


class SocraticMentorAI:
  """Генератор наводящих вопросов (Шаблоны + Gemini LLM)."""

  @classmethod
  def generate_hint(
      cls, code: str, syntax_valid: bool, error_details: dict = None
  ) -> str:
    # --- Шаг A: Быстрый статический ответ для синтаксиса (Шаблоны) ---
    if not syntax_valid and error_details:
      line_no = error_details["line"]
      error_msg = error_details["msg"]
      err_text = (
          error_details["text"].strip() if error_details["text"] else ""
      )

      if "expected ':'" in error_msg or (
          "invalid syntax" in error_msg and ":" not in err_text
      ):
        return (
            f"💡 **Наводящий вопрос Code Mentor:**\n\n"
            f"Взгляни на строку `{line_no}`: `{err_text}`.\n"
            f"В Python управляющие конструкции (`if`, `for`, `def`) открывают"
            " новый блок кода. Какой символ обязателен в самом конце такой"
            " строки?"
        )
      elif "=" in err_text and "==" not in err_text and "if" in err_text:
        return (
            f"💡 **Наводящий вопрос Code Mentor:**\n\n"
            f"Обрати внимание на строку `{line_no}`.\n"
            "Одиночный знак `=` используется для *присваивания* значения. "
            "А какой оператор нужен, если ты хочешь *сравнить* две величины"
            " между собой?"
        )

    # --- Шаг B: Запуск кода и перехват Runtime-ошибок через LLM ---
    runtime_error_tb = cls._try_execute_code(code)

    if runtime_error_tb:
      # Произошла логическая/смысловая ошибка во время выполнения (TypeError, IndexError, etc.)
      return cls._analyze_with_llm(code, runtime_error_tb)

    # Если ошибок нет вовсе
    return "🎉 **Отлично!** Код написан без ошибок. Попробуй запустить его на различных входных данных (edge cases)!"

  @staticmethod
  def _try_execute_code(code: str) -> str | None:
    """Пытается выполнить код во временном окружении для перехвата runtime-ошибок."""
    try:
      compiled_code = compile(code, filename="<user_code>", mode="exec")
      exec(compiled_code, {})
      return None
    except Exception:
      return traceback.format_exc()

  @staticmethod
  def _analyze_with_llm(user_code: str, error_traceback: str) -> str:
    """Отправляет смысловую ошибку в Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")

    if not GENAI_AVAILABLE:
      return (
          "⚠️ Ошибка выполнения кода. Установите библиотеку `google-genai` для"
          " получения Сократовских подсказок от ИИ."
      )

    if not api_key:
      return (
          "💡 **Code Mentor AI:** В коде есть ошибка выполнения! (Задайте"
          " `GEMINI_API_KEY` в окружении, чтобы получать умные Сократовские"
          " подсказки от Gemini)."
      )

    try:
      client = genai.Client(api_key=api_key)
      prompt = f"""
Ученик написал следующий код:
```python
{user_code}
"""           
       
      
   
    
   
  
       

    
   
