import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Fraud Detection App", layout="centered")

st.title("🛡️ ระบบตรวจสอบธุรกรรมทุจริต")
st.write("อิงจากโมเดล IEEE-CIS Fraud Detection")

@st.cache_resource
def load_model():
    with open('fraud_detection_model.pkl', 'rb') as f:
        return pickle.load(f)

model = load_model()

with st.form("input_form"):
    amt = st.number_input("จำนวนเงิน (USD)", min_value=0.0, value=150.0)
    product_cd = st.selectbox("ประเภทสินค้า (ProductCD)", ['W', 'C', 'H', 'R', 'S'])
    card4 = st.selectbox("เครือข่ายบัตร", ['visa', 'mastercard', 'american express', 'discover'])
    card6 = st.selectbox("ประเภทบัตร", ['debit', 'credit'])
    p_email = st.selectbox("อีเมลผู้ซื้อ", ['gmail.com', 'yahoo.com', 'anonymous.com', 'hotmail.com'])
    device_type = st.selectbox("อุปกรณ์", ['desktop', 'mobile'])
    
    submit = st.form_submit_button("วิเคราะห์ความเสี่ยง")

if submit:
    # สร้าง DataFrame ให้ตรงกับตอนเทรน
    input_data = pd.DataFrame([{
        'TransactionAmt': amt, 'ProductCD': product_cd,
        'card1': 10000, 'card2': 300, # ค่าจำลอง
        'card4': card4, 'card6': card6,
        'P_emaildomain': p_email, 'DeviceType': device_type
    }])
    
    for col in input_data.columns:
        if input_data[col].dtype == 'object':
            input_data[col] = input_data[col].astype('category')
            
    # พยากรณ์
    prob = model.predict_proba(input_data)[0][1] * 100
    
    st.subheader("ผลการวิเคราะห์")
    st.metric("โอกาสเกิดการทุจริต", f"{prob:.2f}%")
    
    if prob >= 75:
        st.error("🚨 เสี่ยงสูงมาก! ระงับธุรกรรมทันที")
    elif prob >= 40:
        st.warning("⚠️ เสี่ยงปานกลาง ส่งให้เจ้าหน้าที่ตรวจสอบ")
    else:
        st.success("✅ ปลอดภัย")
