import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ૧. એપનું સેટિંગ અને નામ (Browser Tab માં દેખાશે)
st.set_page_config(page_title="જય ભગવાન બ્રાસ એપ", layout="wide")

# ૨. ડેટા સેવ કરવાનું ફંક્શન
def save_brass_data(name, s_type, gross, less, net, rate, total):
    file_name = "brass_records.csv"
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    entry = {
        "તારીખ": [now],
        "પાર્ટીનું નામ": [name],
        "ભંગાર પ્રકાર": [s_type],
        "કુલ વજન (Kg)": [gross],
        "લેસ (Kg)": [less],
        "ચોખ્ખું વજન (Kg)": [net],
        "ભાવ": [rate],
        "કુલ રકમ": [total]
    }
    df = pd.DataFrame(entry)
    
    if not os.path.isfile(file_name):
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df.to_csv(file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

# ૩. એપનું મુખ્ય હેડિંગ
st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")

# ૪. સાઈડબાર - સેટિંગ્સ
st.sidebar.header("⚙️ સેટિંગ્સ")
brass_rate = st.sidebar.number_input("આજનો પિત્તળનો ભાવ (Kg):", value=450, key="sidebar_rate")

# ૫. ઇનપુટ વિભાગ
st.subheader("📝 નવી એન્ટ્રી")
name = st.text_input("પાર્ટીનું નામ / વિગત:", placeholder="નામ લખો...", key="input_name")

col1, col2, col3 = st.columns(3)

with col1:
    scrap_type = st.selectbox("ભંગારનો પ્રકાર:", ["Honey", "Label", "Pale", "Mixed", "Turning"], key="input_type")

with col2:
    gross_w = st.number_input("કુલ વજન (Gross Kg):", min_value=0.0, step=0.1, key="input_gross")

with col3:
    less_w = st.number_input("લેસ / કચરો (Less Kg):", min_value=0.0, step=0.1, key="input_less")

# ૬. ગણતરી અને પરિણામ
if gross_w > 0:
    net_w = gross_w - less_w
    final_total = net_w * brass_rate
    
    st.divider()
    
    # મોટા અક્ષરે રકમ બતાવવા
    m1, m2, m3 = st.columns(3)
    m1.metric("ચોખ્ખું વજન", f"{net_w:.2f} Kg")
    m2.metric("ભાવ (Kg)", f"₹{brass_rate}")
    m3.metric("કુલ રકમ", f"₹{final_total:,.2f}")
    
    # સેવ કરવાનું બટન
    if st.button("હિસાબ સેવ કરો", key="btn_save"):
        save_brass_data(name, scrap_type, gross_w, less_w, net_w, brass_rate, final_total)
        st.balloons()
        st.success(f"જય ભગવાન! {name} નો હિસાબ ડેટાબેઝમાં સેવ થઈ ગયો છે.")

# ૭. ઇતિહાસ અને રીપોર્ટ
st.divider()
st.subheader("📊 હિસાબનો ઇતિહાસ")

if os.path.isfile("brass_records.csv"):
    history_df = pd.read_csv("brass_records.csv")
    st.dataframe(history_df, use_container_width=True)
    
    # ડાઉનલોડ બટન
    with open("brass_records.csv", "rb") as file:
        st.download_button(
            label="📥 આખો રીપોર્ટ Excel (CSV) માં ડાઉનલોડ કરો",
            data=file,
            file_name="Jay_Bhagvan_Brass_Report.csv",
            mime="text/csv",
            key="btn_download"
        )
else:
    st.info("હજી સુધી કોઈ એન્ટ્રી સેવ કરવામાં આવી નથી.")