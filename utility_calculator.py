import streamlit as st
import pandas as pd
from datetime import datetime

# Заголовок приложения
st.title("Расчет коммунальных платежей")

# Хранилище данных
if "data_store" not in st.session_state:
    st.session_state["data_store"] = []

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
    st.success(f"Сумма за коммунальные услуги в {month:02d}.{year}: {total_sum:.2f} руб.")

    # Добавление данных в хранилище
    if st.button("Сохранить результат"):
        st.session_state["data_store"].append({"year": year, "month": month, "total": total_sum})
        st.info(f"Данные за {month:02d}.{year} сохранены.")

# Показ графика
if st.session_state["data_store"]:
    data_df = pd.DataFrame(st.session_state["data_store"])
    data_df["date"] = pd.to_datetime(data_df[["year", "month"]].assign(day=1))
    data_df = data_df.sort_values("date")
    data_df.set_index("date", inplace=True)

    # График с использованием Streamlit
    st.line_chart(data_df["total"], use_container_width=True, title="История коммунальных платежей")


