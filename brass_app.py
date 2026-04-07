import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ૧. પાસવર્ડ સેટિંગ
if 'login_done' not in st.session_state:
    st.session_state['login_done'] = False

if not st.session_state['login_done']:
    st.title("🔒 જય ભગવાન - લોગિન")
    pwd = st.text_input("પાસવર્ડ લખો", type="password")
    if st.button("પ્રવેશ કરો"):
        if pwd == "kishor123":
            st.session_state['login_done'] = True
            st.rerun()
        else: st.error("ખોટો પાસવર્ડ!")
else:
    # ૨. ગૂગલ શીટ સાથે જોડાણ
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")
    
    # શીટમાંથી ડેટા વાંચવો (Headers મુજબ)
    df = conn.read()

    # ૩. નવી એન્ટ્રીનું ફોર્મ
    with st.expander("➕ નવી એન્ટ્રી ઉમેરો"):
        name = st.text_input("પાર્ટીનું નામ:")
        gross = st.number_input("કુલ વજન (Kg):", min_value=0.0)
        less = st.number_input("લેસ / કચરો (Kg):", min_value=0.0)
        price = st.number_input("ભાવ:", min_value=0)
        
        if st.button("📝 હિસાબ સેવ કરો"):
            net = gross - less
            total = net * price
            date = datetime.now().strftime("%d-%m-%Y %H:%M")
            
            # નવો ડેટા (તમારી શીટના ખાના મુજબ સેટ કર્યો છે)
            new_row = pd.DataFrame([[date, name, "Honey", gross, less, net, price, total]], 
                                   columns=df.columns)
            
            # ગૂગલ શીટમાં સેવ કરવું
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("હિસાબ ગૂગલ શીટમાં અમર થઈ ગયો! ✨")
            st.rerun()

    # ૪. હિસાબનું ટેબલ
    st.subheader("📊 લાઈવ હિસાબ (Google Sheets)")
    st.dataframe(df, use_container_width=True)
    
