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
    df = conn.read()

    st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")

    # ૩. નવી એન્ટ્રી (આને આપણે નાની કરી દીધી છે)
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
            new_row = pd.DataFrame([[date, name, scrap, gross, less, net, price, total]], columns=df.columns)
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("સેવ થઈ ગયું!")
            st.rerun()

    # ૪. ક્લાયન્ટ વાઈઝ હિસાબ (તમારો મુખ્ય ઉકેલ)
    st.divider()
    st.subheader("🔍 પાર્ટી મુજબ હિસાબ અને બિલ")
    
    # બધી પાર્ટીના નામનું લિસ્ટ
    party_list = ["બધી પાર્ટી"] + sorted(list(df["પાર્ટીનું નામ"].unique()))
    selected_party = st.selectbox("પાર્ટી પસંદ કરો:", party_list)

    if selected_party == "બધી પાર્ટી":
        display_df = df
        st.write("અત્યારે બધી પાર્ટીનો હિસાબ દેખાય છે.")
    else:
        display_df = df[df["પાર્ટીનું નામ"] == selected_party]
        
        # ૫. સરવાળો (Total) બતાવવો
        total_weight = display_df["ચોખ્ખું વજન (Kg)"].sum()
        total_amount = display_df["કુલ રકમ"].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("કુલ ચોખ્ખું વજન (Kg)", f"{total_weight:,.2f}")
        with col2:
            st.metric("કુલ બાકી રકમ (₹)", f"₹{total_amount:,.2f}")

    # ટેબલ બતાવવું
    st.dataframe(display_df, use_container_width=True)

    # ૬. વોટ્સએપ પર મોકલવા માટે
    if selected_party != "બધી પાર્ટી" and not display_df.empty:
        msg = f"જય ભગવાન બ્રાસ\n---\nપાર્ટી: {selected_party}\nકુલ વજન: {total_weight} Kg\nકુલ રકમ: ₹{total_amount}\n---"
        wa_link = f"https://wa.me/?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
        st.markdown(f"[📲 {selected_party} ને વોટ્સએપ પર હિસાબ મોકલો]({wa_link})")
            
           
