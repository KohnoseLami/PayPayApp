import streamlit as st
from PayPayPy import PayPay
from PayPayPy.main import PayPayError
import uuid

st.title("PayPay ログイン")
st.markdown("#### 電話番号とパスワードを入力してください")

phonenumber = st.text_input("電話番号", max_chars=11)
password = st.text_input("パスワード", type='password')

col1, col2 = st.columns(2)
with col1:
    device_uuid = st.text_input("DeviceUUID (optional)", placeholder="00000000-0000-0000-0000-000000000000", help="デバイスのUUIDを指定できます。OTPをバイパスするために役立ちます")
with col2:
    client_uuid = st.text_input("ClientUUID (optional)", placeholder="00000000-0000-0000-0000-000000000000", help="アプリのUUIDを指定できます。OTPをバイパスするために役立ちます")

login_event = st.button("ログイン")

if phonenumber and password and login_event:
    if not device_uuid:
        device_uuid = str(uuid.uuid4()).upper()
    if not client_uuid:
        client_uuid = str(uuid.uuid4()).upper()
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
            otp = st.text_input("OTP", max_chars=4)
            otp_event = st.button("送信")
            if otp and otp_event:
                try:
                    otp_result = paypay.login_otp(login_result.error.otpReferenceId, otp)
                except PayPayError as e:
                    st.error(f"ログインに失敗しました {e}")
                else:
                    st.write("ログイン成功！")
                    st.write(paypay.headers)
