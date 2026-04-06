import streamlit as st
import pandas as pd
import os

# ૧. પાસવર્ડ સેટિંગ (Login Logic)
if 'login_done' not in st.session_state:
    st.session_state['login_done'] = False

if not st.session_state['login_done']:
    st.title("🔒 જય ભગવાન - લોગિન")
    user_pwd = st.text_input("પાસવર્ડ લખો (Enter Password)", type="password")
    
    if st.button("પ્રવેશ કરો"):
        if user_pwd == "kishor123": # તમે અહીં તમારો પાસવર્ડ બદલી શકો છો
            st.session_state['login_done'] = True
            st.rerun()
        else:
            st.error("ખોટો પાસવર્ડ! ફરી પ્રયત્ન કરો.")
else:
    # ૨. પાસવર્ડ સાચો હોય તો જ આ નીચેનો ભાગ દેખાશે
    st.title("જય ભગવાન બ્રાસ મેનેજમેન્ટ 🛠️")
    
    # ફાઈલ લોડ કરવી
    file_name = "brass_records.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=["Customer Name", "Weight (kg)", "Price (per kg)", "Total Amount"])

    # નવો રેકોર્ડ ઉમેરવો
    st.subheader("નવી એન્ટ્રી ઉમેરો")
    name = st.text_input("Customer Name")
    weight = st.number_input("Weight (kg)", min_value=0.0)
    price = st.number_input("Price (per kg)", min_value=0.0)

    if st.button("Add Record"):
        total = weight * price
        new_data = pd.DataFrame([[name, weight, price, total]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(file_name, index=False)
        st.success(f"{name} નો હિસાબ સેવ થઈ ગયો!")

    # હિસાબ બતાવવો
    st.subheader("બધો હિસાબ")
    st.dataframe(df)
    
    # લોગઆઉટ બટન
    if st.button("Logout"):
        st.session_state['login_done'] = False
        st.rerun()
    
   
