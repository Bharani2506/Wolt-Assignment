import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Load Data
df = pd.read_csv("dataset_for_datascience_assignment.csv")
df["REGISTRATION_DATE"] = pd.to_datetime(df["REGISTRATION_DATE"])
df["FIRST_PURCHASE_DAY"] = pd.to_datetime(df["FIRST_PURCHASE_DAY"])
df["LAST_PURCHASE_DAY"] = pd.to_datetime(df["LAST_PURCHASE_DAY"])

# Define functions for each visualization
def plot_purchase_distribution():
    st.title("📊 Distribution of Purchase Counts per User")
    plt.figure(figsize=(10, 5))
    sns.histplot(df["PURCHASE_COUNT"], bins=30, kde=True, color="blue")
    plt.title("Distribution of Purchase Counts per User")
    plt.xlabel("Number of Purchases")
    plt.ylabel("Number of Users")
    plt.yscale("log")
    st.pyplot(plt) 

def plot_purchase_hour():
    st.title("⏰ Most Common Purchase Hour of the Day")
    plt.figure(figsize=(12, 5))
    sns.histplot(df["MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE"].dropna(), bins=24, kde=True, color="green")
    plt.title("Most Common Purchase Hour of the Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Users")
    plt.xticks(range(0, 24))
    st.pyplot(plt) 

def plot_customer_segmentation():
    st.title("👥 Customer Segmentation by Purchase Frequency")
    df["Customer_Type"] = pd.cut(df["PURCHASE_COUNT"], bins=[-1, 0, 5, 20, df["PURCHASE_COUNT"].max()],
                                 labels=["No Purchase", "Low", "Medium", "High"])
    customer_segmentation = df["Customer_Type"].value_counts().reset_index()
    customer_segmentation.columns = ["Customer Type", "User Count"]
    fig = px.pie(customer_segmentation, values="User Count", names="Customer Type", 
                 title="Customer Segmentation by Purchase Frequency", hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig)

def plot_revenue_by_country():
    st.title("🌍 Revenue Breakdown by Country")
    revenue_by_country = df.groupby("REGISTRATION_COUNTRY")["TOTAL_PURCHASES_EUR"].sum().reset_index()
    revenue_by_country = revenue_by_country.sort_values(by="TOTAL_PURCHASES_EUR", ascending=False).head(10)
    fig = px.bar(revenue_by_country, x="REGISTRATION_COUNTRY", y="TOTAL_PURCHASES_EUR", 
                 title="Top 10 Countries by Total Revenue", text_auto=True, 
                 color="TOTAL_PURCHASES_EUR", color_continuous_scale="blues")
    st.plotly_chart(fig)

def plot_retention_analysis():
    st.title("🔄 Customer Retention Cohort Analysis")
    df["CohortMonth"] = df["REGISTRATION_DATE"].dt.to_period("M")
    retention_matrix = df.groupby(["CohortMonth", df["FIRST_PURCHASE_DAY"].dt.to_period("M")])["PURCHASE_COUNT"].count().unstack()
    plt.figure(figsize=(12, 6))
    sns.heatmap(retention_matrix, annot=True, fmt=".0f", cmap="Blues")
    plt.title("Customer Retention Cohort Analysis")
    plt.xlabel("Months Since Registration")
    plt.ylabel("Cohort Month")
    st.pyplot(plt) 

def plot_funnel_conversion():
    st.title("🔺 User Funnel Conversion Rates")
    funnel_data = {
        "Stage": ["Registered", "First Order", "Repeat Order"],
        "Users": [df.shape[0], df["FIRST_PURCHASE_DAY"].notna().sum(), df[df["PURCHASE_COUNT"] > 1].shape[0]]
    }
    funnel_df = pd.DataFrame(funnel_data)
    fig = go.Figure(go.Funnel(y=funnel_df["Stage"], x=funnel_df["Users"], textinfo="value+percent initial"))
    fig.update_layout(title="User Funnel Conversion")
    st.plotly_chart(fig)

def plot_device_preference():
    st.title("📱 Device Preference: iOS vs. Android vs. Web")
    device_purchases = df[['IOS_PURCHASES', 'WEB_PURCHASES', 'ANDROID_PURCHASES']].sum().reset_index()
    device_purchases.columns = ["Device", "Purchase Count"]
    fig = px.bar(device_purchases, x="Device", y="Purchase Count", text_auto=True,
                 title="Device Preference: iOS vs. Android vs. Web", color="Device")
    st.plotly_chart(fig)

def plot_order_type():
    st.title("🍽️ Order Type Preference: Delivery vs. Takeaway")
    order_type = df[['PURCHASE_COUNT_DELIVERY', 'PURCHASE_COUNT_TAKEAWAY']].sum().reset_index()
    order_type.columns = ["Order Type", "Count"]
    fig = px.pie(order_type, values="Count", names="Order Type", 
                 title="Order Type Preference: Delivery vs. Takeaway", hole=0.4)
    st.plotly_chart(fig)

def plot_repeat_vs_onetime():
    st.title("🔁 Repeat Customers vs. One-Time Users")
    repeat_customers = df[df["PURCHASE_COUNT"] > 1].shape[0]
    one_time_customers = df[df["PURCHASE_COUNT"] == 1].shape[0]
    fig = px.pie(names=["Repeat Customers", "One-Time Users"], 
                 values=[repeat_customers, one_time_customers], 
                 title="Customer Retention: Repeat vs. One-Time Users")
    st.plotly_chart(fig)

def plot_purchase_trends():
    st.title("📅 Purchase Trends by Time of Day & Day of Week")
    fig = px.density_heatmap(df, 
                             x="MOST_COMMON_HOUR_OF_THE_DAY_TO_PURCHASE", 
                             y="MOST_COMMON_WEEKDAY_TO_PURCHASE", 
                             z="PURCHASE_COUNT", 
                             title="Purchase Trends by Time & Day", 
                             color_continuous_scale="reds")
    st.plotly_chart(fig)

# Streamlit sidebar for navigation
st.sidebar.title("📊 Data Science Dashboard")
app_mode = st.sidebar.radio("Select a Visualization", [
    "Purchase Distribution",
    "Purchase Hour",
    "Customer Segmentation",
    "Revenue by Country",
    "Customer Retention Cohort",
    "User Funnel Conversion",
    "Device Preference",
    "Order Type Preference",
    "Repeat vs. One-Time Users",
    "Purchase Trends"
])

# Navigation logic
if app_mode == "Purchase Distribution":
    plot_purchase_distribution()
elif app_mode == "Purchase Hour":
    plot_purchase_hour()
elif app_mode == "Customer Segmentation":
    plot_customer_segmentation()
elif app_mode == "Revenue by Country":
    plot_revenue_by_country()
elif app_mode == "Customer Retention Cohort":
    plot_retention_analysis()
elif app_mode == "User Funnel Conversion":
    plot_funnel_conversion()
elif app_mode == "Device Preference":
    plot_device_preference()
elif app_mode == "Order Type Preference":
    plot_order_type()
elif app_mode == "Repeat vs. One-Time Users":
    plot_repeat_vs_onetime()
elif app_mode == "Purchase Trends":
    plot_purchase_trends()
