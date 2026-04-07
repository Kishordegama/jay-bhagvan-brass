import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# ૧. પેજ સેટઅપ
st.set_page_config(page_title="જય ભગવાન બ્રાસ", page_icon="🙏")

# ૨. લોગિન સિસ્ટમ
if 'login_done' not in st.session_state:
    st.session_state['login_done'] = False

if not st.session_state['login_done']:
    st.title("🔒 જય ભગવાન - લોગિન")
    pwd = st.text_input("પાસવર્ડ લખો", type="password")
    if st.button("પ્રવેશ કરો"):
        if pwd == "kishor123":
            st.session_state['login_done'] = True
            st.rerun()
        else:
            st.error("ખોટો પાસવર્ડ! ફરી પ્રયત્ન કરો.")
else:
    # ૩. ગૂગલ શીટ કનેક્શન
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # શીટમાંથી ડેટા વાંચવો (ખાલી લાઈનો અને કૉલમ્સ કાઢી નાખવા)
        df = conn.read().dropna(axis=0, how='all').dropna(axis=1, how='all')
    except Exception as e:
        st.error("ગૂગલ શીટ સાથે જોડાવવામાં તકલીફ છે. મહેરબાની કરીને Secrets ચેક કરો.")
        st.stop()

    st.title("🙏 જય ભગવાન બ્રાસ મેનેજમેન્ટ")

    # ૪. નવી એન્ટ્રી ઉમેરવાનું ફોર્મ
    with st.expander("➕ નવી એન્ટ્રી ઉમેરો"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("પાર્ટીનું નામ:")
            scrap = st.selectbox("ભંગાર પ્રકાર:", ["Honey", "Mixed", "Heavy", "Turning", "Other"])
        with col2:
            gross = st.number_input("કુલ વજન (Kg):", min_value=0.0, step=0.1)
            less = st.number_input("લેસ (Kg):", min_value=0.0, step=0.1)
        
        price = st.number_input("ભાવ (₹):", min_value=0)
        
        if st.button("📝 સેવ કરો"):
            if name:
                net = gross - less
                total = net * price
                date = datetime.now().strftime("%d-%m-%Y %H:%M")
                
                # શીટના હેડિંગ મુજબ ડેટા
                cols = ["તારીખ", "પાર્ટીનું નામ", "ભંગાર પ્રકાર", "કુલ વજન (Kg)", "લેસ (Kg)", "ચોખ્ખું વજન (Kg)", "ભાવ", "કુલ રકમ"]
                new_row = pd.DataFrame([[date, name, scrap, gross, less, net, price, total]], columns=cols)
                
                # શીટ અપડેટ કરવી
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"{name} નો હિસાબ સેવ થઈ ગયો! ✨")
                st.rerun()
            else:
                st.warning("મહેરબાની કરીને પાર્ટીનું નામ લખો.")

    # ૫. ફિલ્ટર અને હિસાબ (ક્લાયન્ટ માટે)
    st.divider()
    if not df.empty:
        st.subheader("🔍 પાર્ટી મુજબ હિસાબ અને બિલ")
        
        # બધી પાર્ટીના નામનું લિસ્ટ
        clean_parties = [x for x in df["પાર્ટીનું નામ"].unique() if str(x) != 'nan']
        party_list = ["બધી પાર્ટી"] + sorted(clean_parties)
        selected_party = st.selectbox("પાર્ટી પસંદ કરો:", party_list)

        if selected_party == "બધી પાર્ટી":
            display_df = df
        else:
            display_df = df[df["પાર્ટીનું નામ"] == selected_party]
            
            # ટોટલની ગણતરી
            total_weight = display_df["ચોખ્ખું વજન (Kg)"].sum()
            total_amount = display_df["કુલ રકમ"].sum()
            
            # સ્ક્રીન પર ટોટલ બતાવવું
            c1, c2 = st.columns(2)
            c1.metric("કુલ વજન (Kg)", f"{total_weight:,.2f}")
            c2.metric("કુલ બાકી રકમ (₹)", f"₹{total_amount:,.2f}")
            
            # WhatsApp શેર બટન
            msg = f"જય ભગવાન બ્રાસ\n---\nપાર્ટી: {selected_party}\nકુલ વજન: {total_weight:,.2f} Kg\nકુલ રકમ: ₹{total_amount:,.2f}\n---"
            wa_link = f"https://wa.me/?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.markdown(f"[📲 {selected_party} ને WhatsApp મોકલો]({wa_link})")

        # મુખ્ય ટેબલ
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("હજી કોઈ ડેટા નથી. નવી એન્ટ્રી કરો.")

    if st.sidebar.button("Logout"):
        st.session_state['login_done'] = False
        st.rerun()
