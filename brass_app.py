import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ૧. પાસવર્ડ લોજિક
if 'login_done' not in st.session_state:
    st.session_state['login_done'] = False

if not st.session_state['login_done']:
    st.title("🔒 જય ભગવાન - લોગિન")
    user_pwd = st.text_input("પાસવર્ડ લખો", type="password")
    if st.button("પ્રવેશ કરો"):
        if user_pwd == "kishor123":
            st.session_state['login_done'] = True
            st.rerun()
        else:
            st.error("ખોટો પાસવર્ડ!")
else:
    # ૨. મેઈન એપ શરૂ (પાસવર્ડ પછી)
    st.set_page_config(page_title="જય ભગવાન બ્રાસ", layout="wide")
    
    # સાઈડબાર - સેટિંગ્સ
    st.sidebar.title("⚙️ સેટિંગ્સ")
    today_price = st.sidebar.number_input("આજનો પિત્તળનો ભાવ (Kg):", min_value=0, value=450)

    st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")
    
    # ફાઈલ લોડ કરવી
    file_name = "brass_records.csv"
    columns = ["તારીખ", "પાર્ટીનું નામ", "ભંગાર પ્રકાર", "કુલ વજન (Kg)", "લેસ (Kg)", "ચોખ્ખું વજન (Kg)", "ભાવ", "કુલ રકમ"]
    
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=columns)

    # ૩. નવી એન્ટ્રીનું ફોર્મ
    st.subheader("📝 નવી એન્ટ્રી")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("પાર્ટીનું નામ / વિગત:")
        scrap_type = st.selectbox("ભંગારનો પ્રકાર:", ["Honey", "Mixed", "Heavy", "Turning", "Other"])
    
    with col2:
        gross_weight = st.number_input("કુલ વજન (Gross Kg):", min_value=0.0, step=0.1)
        less_weight = st.number_input("લેસ / કચરો (Less Kg):", min_value=0.0, step=0.1)
    
    # ગણતરી
    net_weight = gross_weight - less_weight
    final_price = today_price # અથવા તમે મેન્યુઅલ ઇનપુટ પણ રાખી શકો
    total_amt = net_weight * final_price

    if st.button("📝 હિસાબ સેવ કરો"):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_entry = pd.DataFrame([[current_time, name, scrap_type, gross_weight, less_weight, net_weight, final_price, total_amt]], columns=columns)
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file_name, index=False)
        st.success(f"{name} નો હિસાબ સેવ થઈ ગયો!")
        st.rerun()

    # ૪. હિસાબનું ટેબલ
    st.subheader("📊 હિસાબનો ઇતિહાસ")
    st.dataframe(df, use_container_width=True)

    # ૫. એક્સલ ડાઉનલોડ બટન
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 આખી રિપોર્ટ Excel (CSV) માં ડાઉનલોડ કરો",
        data=csv,
        file_name='brass_report.csv',
        mime='text/csv',
    )

    if st.sidebar.button("Log Out"):
        st.session_state['login_done'] = False
        st.rerun()
