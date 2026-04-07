import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ૧. પાસવર્ડ
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
    # ૨. કનેક્શન (અહીં આપણે એરર હેન્ડલિંગ ઉમેર્યું છે)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read().dropna(axis=0, how='all').dropna(axis=1, how='all')
    except Exception as e:
        st.error("ગૂગલ શીટ સાથે જોડાવવામાં તકલીફ છે. મહેરબાની કરીને સેટિંગ્સ ચેક કરો.")
        st.stop()

    st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")

    # ૩. નવી એન્ટ્રી
    with st.expander("➕ નવી એન્ટ્રી ઉમેરો"):
        name = st.text_input("પાર્ટીનું નામ:")
        scrap = st.selectbox("પ્રકાર:", ["Honey", "Mixed", "Heavy", "Turning", "Other"])
        gross = st.number_input("કુલ વજન (Kg):", min_value=0.0)
        less = st.number_input("લેસ (Kg):", min_value=0.0)
        price = st.number_input("ભાવ:", min_value=0)
        
        if st.button("📝 સેવ કરો"):
            if name:
                try:
                    net = gross - less
                    total = net * price
                    date = datetime.now().strftime("%d-%m-%Y %H:%M")
                    
                    # હેડિંગ્સ તમારી શીટ મુજબ
                    cols = ["તારીખ", "પાર્ટીનું નામ", "ભંગાર પ્રકાર", "કુલ વજન (Kg)", "લેસ (Kg)", "ચોખ્ખું વજન (Kg)", "ભાવ", "કુલ રકમ"]
                    new_row = pd.DataFrame([[date, name, scrap, gross, less, net, price, total]], columns=cols)
                    
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("હિસાબ સેવ થઈ ગયો! ✨")
                    st.rerun()
                except Exception as err:
                    st.error("સેવ કરવામાં એરર આવી. ગૂગલ 'ડિજિટલ ચાવી' (Service Account) માંગે છે.")
                    st.info("જો તમે ડેટા સેવ ના કરી શકતા હોવ, તો અત્યારે જૂની રીતે CSV ડાઉનલોડ કરીને કામ ચલાવો.")
            else:
                st.warning("પાર્ટીનું નામ લખવું જરૂરી છે.")

    # ૪. ફિલ્ટર અને ડિસ્પ્લે
    st.divider()
    if not df.empty:
        # અહીં ખાલી ખાના કાઢીને લિસ્ટ બનાવવું
        clean_parties = [x for x in df["પાર્ટીનું નામ"].unique() if str(x) != 'nan']
        party_list = ["બધી પાર્ટી"] + sorted(clean_parties)
        selected_party = st.selectbox("પાર્ટી પસંદ કરો:", party_list)

        display_df = df if selected_party == "બધી પાર્ટી" else df[df["પાર્ટીનું નામ"] == selected_party]
        
        if selected_party != "બધી પાર્ટી":
            st.metric("કુલ રકમ", f"₹{display_df['કુલ રકમ'].sum():,.2f}")
            
        st.dataframe(display_df, use_container_width=True)
    
    if st.sidebar.button("Logout"):
        st.session_state['login_done'] = False
        st.rerun()

   
