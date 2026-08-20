import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ==========================================
# 1. СТАТИЧЕСКИЙ АНАЛИЗ КОДА (AST)
# ==========================================
class CodeAnalyzer:
    """Модуль быстрой проверки синтаксиса без вызова сторонних API."""
    @staticmethod
    def check_syntax(code_str: str):
        try:
            parsed_ast = ast.parse(code_str)
            return True, "Синтаксических ошибок не обнаружено.", None, parsed_ast
        except SyntaxError as e:
            error_details = {
                "line": e.lineno,
                "offset": e.offset,
                "text": e.text,
                "msg": e.msg
            }
            return False, f"Синтаксическая ошибка на строке {e.lineno}", error_details, None

    @staticmethod
    def get_complexity(node):
        """Расчет цикломатической сложности кода (количество ветвлений)."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or)):
                complexity += 1
        return complexity

# ==========================================
# 2. ИИ-МОДУЛЬ: СОКРАТОВСКИЕ ПОДСКАЗКИ
# ==========================================
class SocraticMentorAI:
    """Генератор наводящих вопросов по методу Сократа."""
    @classmethod
    def generate_hint(cls, code: str, syntax_valid: bool, error_details: dict = None):
        if not syntax_valid and error_details:
            line_no = error_details["line"]
            error_msg = error_details["msg"]
            err_text = error_details["text"].strip() if error_details["text"] else ""

            # Шаблоны наводящих вопросов на основе типа ошибки
            if "expected ':'" in error_msg or ("invalid syntax" in error_msg and ":" not in err_text):
                return (
                    f"💡 **Наводящий вопрос Code Mentor:**\n\n"
                    f"Взгляни на строку `{line_no}`: `{err_text}`.\n"
                    f"В Python управляющие конструкции (`if`, `for`, `def`) открывают новый блок кода. "
                    f"Какой символ обязателен в самом конце такой строки?"
                )
            elif "=" in err_text and "==" not in err_text and "if" in err_text:
                return (
                    f"💡 **Наводящий вопрос Code Mentor:**\n\n"
                    f"Обрати внимание на строку `{line_no}`.\n"
                    f"Одиночный знак `=` используется для *присваивания* значения. "
                    f"А какой оператор нужен, если ты хочешь *сравнить* две величины между собой?"
                )
            else:
                return (
                    f"💡 **Наводящий вопрос Code Mentor:**\n\n"
                    f"Интерпретатор запутался на строке `{line_no}`: `{err_text}`.\n"
                    f"Проверь правила синтаксиса в этой строке: нет ли опечатки в названии команды или пропущенной скобки?"
                )
        else:
            return "🎉 **Отлично!** Код написан без синтаксических ошибок. Попробуй запустить его на разных входных данных!"

# ==========================================
# 3. МОДУЛЬ АНАЛИТИКИ КЛАССА (EDA)
# ==========================================
def make_eda_dashboard():
    """Создает наглядные графики успеваемости класса для учителя."""
    np.random.seed(42)
    topics = ['Циклы', 'Условия', 'Списки', 'Функции', 'PEP8']
    data = {
        'Topic': np.random.choice(topics, size=150),
        'Attempts': np.random.poisson(lam=2, size=150) + 1,
        'Solved_Self': np.random.choice([True, False], size=150, p=[0.8, 0.2])
    }
    df = pd.DataFrame(data)
    
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    sns.set_theme(style="whitegrid")
    
    sns.barplot(ax=axes[0], data=df, x='Topic', y='Attempts', palette='Blues_r', errorbar=None)
    axes[0].set_title('Среднее число попыток до исправления')
    
    self_solve = df.groupby('Topic')['Solved_Self'].mean().reset_index()
    self_solve['Solved_Self'] *= 100
    sns.barplot(ax=axes[1], data=self_solve, x='Topic', y='Solved_Self', palette='Greens_r')
    axes[1].set_title('% самостоятельных решений учениками')
    
    plt.tight_layout()
    return fig

# ==========================================
# 4. ВЕБ-ИНТЕРФЕЙС (STREAMLIT)
# ==========================================
def main():
    st.set_page_config(page_title="Code Mentor AI", layout="wide")
    st.title("🎓 Code Mentor AI")
    st.caption("Интеллектуальный ревьюер кода с Сократовским диалогом")

    tab1, tab2, tab3 = st.tabs(["📝 Проверка кода", "📊 Аналитика учителя", "🛡️ Этика и правила"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            user_code = st.text_area(
                "Введите код программы (Python):",
                value="def check_number(n)\n    if n % 2 = 0:\n        return True",
                height=220
            )
            btn = st.button("Проверить код", type="primary")

        with col2:
            if btn:
                is_valid, msg, err_details, parsed_ast = CodeAnalyzer.check_syntax(user_code)
                if not is_valid:
                    st.error(msg)
                    st.info(SocraticMentorAI.generate_hint(user_code, is_valid, err_details))
                else:
                    st.success(msg)
                    st.metric("Сложность алгоритма", CodeAnalyzer.get_complexity(parsed_ast))
                    st.info(SocraticMentorAI.generate_hint(user_code, is_valid))

    with tab2:
        st.subheader("Дашборд успеваемости класса (Data-Driven Decisions)")
        st.pyplot(make_eda_dashboard())

    with tab3:
        st.markdown("""
        * **Анти-списывание:** ИИ не выдает готовый исправленный код.
        * **Приватность:** Код обрабатывается анонимно без сохранения имен учеников.
        * **Инклюзивность:** Поддержка экранных дикторов и крупного шрифта.
        """)

if __name__ == "__main__":
    main()