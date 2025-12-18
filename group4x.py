import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Business Dashboard",
    layout="wide"
)

# =====================
# LANGUAGE DICTIONARY
# =====================
LANG = {
    "id": {
        "title": "Dashboard Bisnis Supermarket",
        "upload": "Unggah File Excel",
        "filter": "Filter Data",
        "city": "Kota",
        "product": "Kategori Produk",
        "payment": "Metode Pembayaran",
        "date": "Rentang Tanggal",
        "sales": "Total Pendapatan",
        "profit": "Total Keuntungan",
        "qty": "Total Produk Terjual",
        "c1": "Pendapatan per Kategori Produk",
        "c2": "Pendapatan per Kota",
        "c3": "Distribusi Metode Pembayaran",
        "c4": "Tren Pendapatan Harian",
        "c5": "Jumlah Produk Terjual per Kategori"
    },
    "en": {
        "title": "Supermarket Business Dashboard",
        "upload": "Upload Excel File",
        "filter": "Data Filter",
        "city": "City",
        "product": "Product Line",
        "payment": "Payment Method",
        "date": "Date Range",
        "sales": "Total Revenue",
        "profit": "Total Profit",
        "qty": "Total Quantity Sold",
        "c1": "Revenue by Product Line",
        "c2": "Revenue by City",
        "c3": "Payment Method Distribution",
        "c4": "Daily Revenue Trend",
        "c5": "Quantity Sold by Product Line"
    }
}

# =====================
# LANGUAGE SELECT
# =====================
lang_choice = st.sidebar.selectbox("Language / Bahasa", ["Bahasa", "English"])
lang = LANG["id"] if lang_choice == "Bahasa" else LANG["en"]

st.title(lang["title"])

# =====================
# FILE UPLOAD
# =====================
file = st.file_uploader(lang["upload"], type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df["Date"] = pd.to_datetime(df["Date"])

    # =====================
    # SIDEBAR FILTER
    # =====================
    st.sidebar.header(lang["filter"])

    city_filter = st.sidebar.multiselect(
        lang["city"],
        df["City"].unique(),
        default=df["City"].unique()
    )

    product_filter = st.sidebar.multiselect(
        lang["product"],
        df["Product line"].unique(),
        default=df["Product line"].unique()
    )

    payment_filter = st.sidebar.multiselect(
        lang["payment"],
        df["Payment"].unique(),
        default=df["Payment"].unique()
    )

    date_filter = st.sidebar.date_input(
        lang["date"],
        [df["Date"].min(), df["Date"].max()]
    )

    # =====================
    # FILTERING DATA
    # =====================
    df_filtered = df[
        (df["City"].isin(city_filter)) &
        (df["Product line"].isin(product_filter)) &
        (df["Payment"].isin(payment_filter)) &
        (df["Date"] >= pd.to_datetime(date_filter[0])) &
        (df["Date"] <= pd.to_datetime(date_filter[1]))
    ]

    # =====================
    # KPI
    # =====================
    c1, c2, c3 = st.columns(3)

    c1.metric(lang["sales"], f"{df_filtered['Total'].sum():,.2f}")
    c2.metric(lang["profit"], f"{df_filtered['gross income'].sum():,.2f}")
    c3.metric(lang["qty"], int(df_filtered["Quantity"].sum()))

    st.divider()

    # =====================
    # CHARTS
    # =====================
    st.subheader(lang["c1"])
    st.bar_chart(df_filtered.groupby("Product line")["Total"].sum())

    st.subheader(lang["c2"])
    st.bar_chart(df_filtered.groupby("City")["Total"].sum())

    st.subheader(lang["c3"])
    payment_count = df_filtered["Payment"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(payment_count, labels=payment_count.index, autopct="%1.1f%%")
    st.pyplot(fig)

    st.subheader(lang["c4"])
    st.line_chart(df_filtered.groupby("Date")["Total"].sum())

    st.subheader(lang["c5"])
    st.bar_chart(df_filtered.groupby("Product line")["Quantity"].sum())

else:
    st.info("Unggah file Excel untuk memulai.")
