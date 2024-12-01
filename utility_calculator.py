import streamlit as st
import pandas as pd
from datetime import datetime

# Заголовок приложения
st.title("Расчет коммунальных платежей")

# Хранилище данных
if "data_store" not in st.session_state:
    st.session_state["data_store"] = []  # Инициализация пустого хранилища

# Получение текущего года и месяца
current_year = datetime.now().year
current_month = datetime.now().month

# Выбор года с предустановленным текущим годом
year = st.selectbox("Выберите год:", range(2020, 2031), index=(current_year - 2020))

# Выбор месяца с помощью радиокнопок
month = st.radio(
    "Выберите месяц:",
    [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
)

# Словарь для преобразования месяца в число
month_to_number = {
    "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4, "Май": 5, "Июнь": 6,
    "Июль": 7, "Август": 8, "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
}

# Ввод сумм по коммунальным услугам
vodootvedenie = st.number_input("Водоотведение, руб.:", min_value=0.0, step=0.1)
holodnoe_vodosnabzhenie = st.number_input("Холодное водоснабжение, руб.:", min_value=0.0, step=0.1)
hvs_dlya_gvs = st.number_input("ХВС для ГВС, руб.:", min_value=0.0, step=0.1)
gvs_podogrev = st.number_input("ГВС подогрев, руб.:", min_value=0.0, step=0.1)
elektroenergiya = st.number_input("Электроэнергия, руб.:", min_value=0.0, step=0.1)

# Расчет общей суммы
if st.button("Рассчитать"):
    total_sum = (
        vodootvedenie +
        holodnoe_vodosnabzhenie +
        hvs_dlya_gvs +
        gvs_podogrev +
        elektroenergiya
    )
    st.success(f"Сумма за коммунальные услуги в {month} {year}: {total_sum:.2f} руб.")

    # Сохранение данных
    st.session_state["data_store"].append({
        "year": year,
        "month": month_to_number[month],  # Преобразование месяца в число
        "total": total_sum
    })
    st.info(f"Данные за {month} {year} сохранены.")

# Показ истории и графика
if st.session_state["data_store"]:
    # Преобразование данных в DataFrame
    data_df = pd.DataFrame(st.session_state["data_store"])
    data_df["date"] = pd.to_datetime(data_df[["year", "month"]].assign(day=1))  # Создание даты
    data_df = data_df.sort_values("date")  # Сортировка по дате
    data_df.set_index("date", inplace=True)  # Установка даты как индекса

    # Показ истории
    st.subheader("История коммунальных платежей")
    st.dataframe(data_df)

    # Показ графика
    st.subheader("График коммунальных платежей")
    st.line_chart(data_df["total"])




