import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json
import base64

# GitHub API functions
def fetch_json_from_github():
    """Fetch JSON data from a GitHub repository."""
    url = "https://api.github.com/repos/Dariam-tech/utility_calculator/contents/data/utility_payments.json"
    headers = {"Authorization": f"token {st.secrets['github']['token']}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = base64.b64decode(response.json()["content"]).decode("utf-8")
        return json.loads(content)
    elif response.status_code == 404:
        # File doesn't exist yet
        return []
    else:
        st.error(f"Failed to fetch JSON file: {response.status_code}")
        return None


def update_json_on_github(data):
    """Update JSON data in a GitHub repository."""
    url = "https://api.github.com/repos/Dariam-tech/utility_calculator/contents/data/utility_payments.json"
    headers = {"Authorization": f"token {st.secrets['github']['token']}"}

    # Fetch the current file SHA (needed to update the file)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]
    elif response.status_code == 404:
        sha = None  # File doesn't exist
    else:
        st.error(f"Failed to fetch file metadata: {response.status_code}")
        return

    # Prepare the updated file content
    content = base64.b64encode(json.dumps(data, indent=2).encode("utf-8")).decode("utf-8")
    payload = {
        "message": "Update utility payments data",
        "content": content,
        "sha": sha
    }

    # Push the updated file
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code in [201, 200]:
        st.success("Data updated on GitHub!")
    else:
        st.error(f"Failed to update JSON file: {response.status_code}")


# Main Streamlit app
st.title("Расчет коммунальных платежей")

# Session state initialization
if "data_store" not in st.session_state:
    st.session_state["data_store"] = fetch_json_from_github() or []

# Get current year and month
current_year = datetime.now().year
current_month = datetime.now().month

# User input
year = st.selectbox("Выберите год:", range(2020, 2031), index=(current_year - 2020))
month = st.radio(
    "Выберите месяц:",
    [
        "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
)

# Map months to numbers
month_to_number = {
    "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4, "Май": 5, "Июнь": 6,
    "Июль": 7, "Август": 8, "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
}

# Utility inputs
vodootvedenie = st.number_input("Водоотведение, руб.:", min_value=0.0, step=0.1)
holodnoe_vodosnabzhenie = st.number_input("Холодное водоснабжение, руб.:", min_value=0.0, step=0.1)
hvs_dlya_gvs = st.number_input("ХВС для ГВС, руб.:", min_value=0.0, step=0.1)
gvs_podogrev = st.number_input("ГВС подогрев, руб.:", min_value=0.0, step=0.1)
elektroenergiya = st.number_input("Электроэнергия, руб.:", min_value=0.0, step=0.1)

# Calculate total
if st.button("Рассчитать"):
    total_sum = (
        vodootvedenie +
        holodnoe_vodosnabzhenie +
        hvs_dlya_gvs +
        gvs_podogrev +
        elektroenergiya
    )
    st.success(f"Сумма за коммунальные услуги в {month} {year}: {total_sum:.2f} руб.")

    # Update local data store
    new_entry = {
        "year": year,
        "month": month_to_number[month],
        "total": total_sum
    }
    st.session_state["data_store"].append(new_entry)

    # Push updated data to GitHub
    update_json_on_github(st.session_state["data_store"])

# Display history and chart
if st.session_state["data_store"]:
    # Convert data to DataFrame
    data_df = pd.DataFrame(st.session_state["data_store"])
    data_df["date"] = pd.to_datetime(data_df[["year", "month"]].assign(day=1))  # Create date column
    data_df = data_df.sort_values("date")  # Sort by date
    data_df.set_index("date", inplace=True)  # Set date as index

    # Display history
    st.subheader("История коммунальных платежей")
    st.dataframe(data_df)

    # Display chart
    st.subheader("График коммунальных платежей")
    st.line_chart(data_df["total"])




