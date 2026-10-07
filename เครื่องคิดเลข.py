import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Terminal Calculator", page_icon="💻", layout="centered")

# ตกแต่ง CSS ให้เป็นธีม Code / Dark Terminal
st.markdown("""
    <style>
    /* พื้นหลังโดยรวมของแอป */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Fira Code', 'Courier New', Courier, monospace;
    }
    
    .block-container {
        max-width: 450px;
        padding-top: 2rem;
        background-color: #161b22;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }
    
    /* สไตล์ปุ่มกดสไตล์ Code / Console */
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-weight: bold;
        border-radius: 6px;
        background-color: #21262d;
        color: #58a6ff;
        border: 1px solid #30363d;
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #30363d;
        border-color: #8b949e;
        color: #79c0ff;
        box-shadow: 0 0 8px rgba(88, 166, 255, 0.3);
    }

    /* ปุ่ม C (Clear) - โทนแดงแบบ Syntax Error / Danger */
    div[data-testid="stButton"] > button[aria-label="C"] {
        background-color: #3c1e1e !important;
        border: 1px solid #f85149 !important;
        color: #ff7b72 !important;
    }
    div[data-testid="stButton"] > button[aria-label="C"]:hover {
        background-color: #5d2424 !important;
        box-shadow: 0 0 8px rgba(248, 81, 73, 0.4);
    }

    /* ปุ่ม = (Equal) - โทนเขียวแบบ Success / Console Output */
    div[data-testid="stButton"] > button[aria-label="="] {
        background-color: #113822 !important;
        border: 1px solid #2ea043 !important;
        color: #56d364 !important;
    }
    div[data-testid="stButton"] > button[aria-label="="]:hover {
        background-color: #175230 !important;
        box-shadow: 0 0 8px rgba(46, 160, 67, 0.4);
    }

    /* ปุ่มเครื่องหมายคำนวณ - โทนสีส้มแบบ Operator ใน IDE */
    div[data-testid="stButton"] > button[aria-label="÷"],
    div[data-testid="stButton"] > button[aria-label="×"],
    div[data-testid="stButton"] > button[aria-label="-"],
    div[data-testid="stButton"] > button[aria-label="+"],
    div[data-testid="stButton"] > button[aria-label="%"] {
        color: #ffa657 !important;
        border-color: #d29922 !important;
    }
    </style>
""", unsafe_allow_html=True)

# จัดการสถานะการคำนวณผ่าน st.session_state
if "display" not in st.session_state:
    st.session_state.display = "0"

def click_btn(val):
    current = st.session_state.display
    if val == "C" or current == "Error":
        st.session_state.display = "0"
    elif val == "=":
        try:
            expr = current.replace("×", "*").replace("÷", "/")
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display = str(result)
        except Exception:
            st.session_state.display = "Error"
    else:
        if current == "0" and val not in ["+", "-", "×", "÷", "(", ")", "%"]:
            st.session_state.display = val
        else:
            st.session_state.display += val

# หัวข้อสไตล์ Terminal
st.markdown("<h2 style='text-align: center; color: #58a6ff; font-family: monospace;'>$&nbsp;calculator.py</h2>", unsafe_allow_html=True)

# หน้าจอแสดงผลลัพธ์สไตล์ Code Console
st.markdown(f"""
    <div style="background-color: #010409; padding: 18px; border-radius: 8px; text-align: right; margin-bottom: 20px; border: 1px solid #2ea043; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); overflow-x: auto;">
        <span style="font-family: 'Fira Code', monospace; font-size: 14px; color: #8b949e; float: left;">out:</span>
        <span style="font-family: 'Fira Code', monospace; font-size: 32px; font-weight: bold; color: #3fb950; text-shadow: 0 0 5px rgba(63, 185, 80, 0.5);">{st.session_state.display}</span>
    </div>
""", unsafe_allow_html=True)

# แผงปุ่มกด
buttons = [
    ["C", "(", ")", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", "%"]
]

for r_idx, row in enumerate(buttons):
    cols = st.columns(4)
    for c_idx, char in enumerate(row):
        if char != "":
            with cols[c_idx]:
                if st.button(char, key=f"btn_{r_idx}_{c_idx}"):
                    click_btn(char)
                    st.rerun()