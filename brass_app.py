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
    # ૨. ગૂગલ શીટ કનેક્શન
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # શીટ વાંચતી વખતે વધારાના ખાલી ખાના કાઢી નાખવા
    df = conn.read().dropna(axis=1, how='all')

    st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")

    # ૩. નવી એન્ટ્રી
    with st.expander("➕ નવી એન્ટ્રી ઉમેરો"):
        name = st.text_input("પાર્ટીનું નામ:")
        scrap = st.selectbox("પ્રકાર:", ["Honey", "Mixed", "Heavy", "Turning", "Other"])
        gross = st.number_input("કુલ વજન (Kg):", min_value=0.0)
        less = st.number_input("લેસ (Kg):", min_value=0.0)
        price = st.number_input("ભાવ:", min_value=0)
        
        if st.button("📝 સેવ કરો"):
            net = gross - less
            total = net * price
            date = datetime.now().strftime("%d-%m-%Y %H:%M")
            
            # ખાનાના નામ ચોક્કસ કરવા (તમારી શીટ મુજબ)
            cols = ["તારીખ", "પાર્ટીનું નામ", "ભંગાર પ્રકાર", "કુલ વજન (Kg)", "લેસ (Kg)", "ચોખ્ખું વજન (Kg)", "ભાવ", "કુલ રકમ"]
            
            new_row = pd.DataFrame([[date, name, scrap, gross, less, net, price, total]], columns=cols)
            
            # ડેટા ભેગો કરીને ગૂગલ શીટમાં મોકલવો
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("હિસાબ ગૂગલ શીટમાં સેવ થઈ ગયો! ✨")
            st.rerun()

    # ૪. પાર્ટી મુજબ ફિલ્ટર
    st.divider()
    if not df.empty:
        party_list = ["બધી પાર્ટી"] + sorted(list(df["પાર્ટીનું નામ"].dropna().unique()))
        selected_party = st.selectbox("પાર્ટી પસંદ કરો:", party_list)

        if selected_party == "બધી પાર્ટી":
            display_df = df
        else:
            display_df = df[df["પાર્ટીનું નામ"] == selected_party]
            
            # ટોટલ બતાવવું
            total_weight = display_df["ચોખ્ખું વજન (Kg)"].sum()
            total_amount = display_df["કુલ રકમ"].sum()
            
            c1, c2 = st.columns(2)
            c1.metric("કુલ વજન (Kg)", f"{total_weight:,.2f}")
            c2.metric("કુલ રકમ (₹)", f"₹{total_amount:,.2f}")
            
            # WhatsApp બટન
            msg = f"જય ભગવાન બ્રાસ\n---\nપાર્ટી: {selected_party}\nકુલ વજન: {total_weight} Kg\nકુલ રકમ: ₹{total_amount}"
            wa_link = f"https://wa.me/?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.markdown(f"[📲 {selected_party} ને વોટ્સએપ મોકલો]({wa_link})")

        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("હજી સુધી કોઈ હિસાબ લખાયો નથી.")
    
