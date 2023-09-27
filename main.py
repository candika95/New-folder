import streamlit as st
import pandas as pd
import base64
from PIL import Image
# from numerize.numerize import numerize



tuguIcon = Image.open('images/Tugu.png')
st.set_page_config(
  page_title = 'UGMxTugu',
  page_icon = '📊',
  layout= 'wide',
  initial_sidebar_state= 'expanded'
)

with open("./styles/style.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;     
    }}
    </style>
    """,
    unsafe_allow_html=True
    )


hide_st_style = """
            <style>
            div.block-container{padding-top: 1rem;}
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.sidebar.image(tuguIcon)

uploaded_files = st.sidebar.file_uploader("Choose file", type="xlsx")
@st.cache_data(ttl=(60*60*24))
def get_data_from_excel(uploaded_file):
    df = pd.read_excel(
        io=uploaded_file,
        # engine="openpyxl",
        # sheet_name="Sales",
        # skiprows=3,
        # usecols="B:R",
        # nrows=1000,
    )
    df['Month'] = df['Order_Date'].dt.strftime('%B')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    df = df.sort_values('Order_Date')
    return df



def sidebarFilter(uploaded_files):
    st.sidebar.header("Please Filter Here:")
    segment = st.sidebar.multiselect(
                "Select the Segment:",
                options=uploaded_files["Segment"].unique(),
                default=uploaded_files["Segment"].unique()
    )
    region = st.sidebar.multiselect(
                "Select the Region:",
                options=uploaded_files["Region"].unique(),
                default=uploaded_files["Region"].unique(),
    )
    ship_mode = st.sidebar.multiselect(
                "Select the Ship Mode:",
                options=uploaded_files["Ship_Mode"].unique(),
                default=uploaded_files["Ship_Mode"].unique()
    )
    df_selection = uploaded_files.query(
                "Segment == @segment & Region == @region & Ship_Mode == @ship_mode"
    )
    return df_selection


    
if uploaded_files:
        if uploaded_files is not None:
            df_selection = sidebarFilter(uploaded_files)
            TotalSales = float(df_selection['Sales'].sum())
            AverageDiscount = float(df_selection['Discount'].mean())
            TotalQuantity = float(df_selection['Quantity'].sum())
            TotalProfit = float(df_selection['Profit'].sum())
              
            col1, col2, col3, col4 = st.columns(4)      
            with col1:
                st.metric(label='Total', value=f"{(TotalSales)}")
            with col2:
                st.metric(label="Average Discount",value=f"{round(AverageDiscount,1)}")
            with col3:
                st.metric(label='Total Quantity',value=(TotalQuantity))
            with col4:
                st.metric(label='Total Profit',value=(TotalProfit))
                
            graph1, graph2 = st.columns(2)
            df_grouped = df_selection.groupby(by=["Order_Date"], as_index=False)[['Sales', 'Profit']].sum()
            with graph1:
                st.line_chart(df_grouped, x = 'Order_Date', y = "Sales", height=400)
            with graph2:
                df_Month = df_selection.groupby(["Month"], as_index=False)[["Sales", "Profit"]].sum()
                month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                df_Month['Month'] = pd.Categorical(df_Month['Month'], categories=month_order, ordered=True)
                df_Month = df_Month.sort_values('Month')
                st.bar_chart(df_Month, x = 'Month', y = "Sales", height=400)
                

            st.dataframe(df_selection)
            
else:
    add_bg_from_local('images/UGM.png')
            