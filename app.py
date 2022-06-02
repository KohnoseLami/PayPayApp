import streamlit as st
from PayPayPy import PayPay

from PayPayPy.main import PayPayError

st.title("PayPay ログイン")
st.markdown("#### 電話番号とパスワードを入力してください")

phonenumber = st.text_input("電話番号")
password = st.text_input("パスワード", type='password')
login_event = st.button("ログイン")

if phonenumber and password and login_event:
    paypay = PayPay()
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
