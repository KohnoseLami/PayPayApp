import streamlit as st
from PayPayPy import PayPay
from PayPayPy.main import PayPayError
import uuid

st.title("PayPay ログイン")
st.markdown("#### 電話番号とパスワードを入力してください")

col1, col2 = st.columns(2)
with col1:
    device_uuid = st.text_input("DeviceUUID", placeholder=str(uuid.uuid4()).upper(), help="デバイスのUUIDを指定できます。OTPをバイパスするために役立ちます")
with col2:
    client_uuid = st.text_input("ClientUUID", placeholder=str(uuid.uuid4()).upper(), help="アプリのUUIDを指定できます。OTPをバイパスするために役立ちます")

phonenumber = st.text_input("電話番号")
password = st.text_input("パスワード", type='password')
login_event = st.button("ログイン")

if phonenumber and password and login_event:
    st.write(device_uuid)
    st.write(client_uuid)
    paypay = PayPay(device_uuid=device_uuid, client_uuid=client_uuid)
    try:
        login_result = paypay.login(phonenumber, password)
    except PayPayError as e:
        st.error(f"ログインに失敗しました {e}")
    else:
        if login_result.header.resultCode == "S0000":
            st.write("ログイン成功！")
            st.write(paypay.headers)
        elif login_result.header.resultCode == "S1004":
            otp = st.text_input("OTP")
            if otp:
                otp_result = paypay.login_otp(otp, login_result.error.otpReferenceId)
                st.write("ログイン成功！")
                st.write(paypay.headers)
