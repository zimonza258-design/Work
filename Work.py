import joblib
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.datasets import load_iris
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Iris AI Command Center",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Futuristic Dark Purple CSS Theme
st.markdown(
    """
    <style>
    header {visibility: hidden;}
    .stApp {
        background-color: #0D0814;
        color: #E2D9F3;
    }
    [data-testid="stSidebar"] {
        background-color: #160D27;
        border-right: 1px solid #331A54;
    }
    .main-card {
        background: linear-gradient(135deg, #1D1035 0%, #29124A 100%);
        border: 1px solid #7B2CBF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(123, 44, 191, 0.2);
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-box {
        background-color: #150B28;
        border-left: 4px solid #9D4EDD;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #C77DFF !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. Load Model & Dataset
@st.cache_resource
def load_data_and_model():
  model = joblib.load("iris_model.pkl")
  iris = load_iris()
  df = pd.DataFrame(iris.data, columns=iris.feature_names)
  df["species"] = [iris.target_names[i].capitalize() for i in iris.target]
  return model, df, [name.capitalize() for name in iris.target_names]


model, df, species_labels = load_data_and_model()

# 4. Sidebar Controls
with st.sidebar:
  st.markdown("## 🎛️ Control Panel")
  st.caption("ปรับแต่งพารามิเตอร์ของดอกไอริส")

  sl = st.number_input(
      "Sepal Length (cm)",
      min_value=float(df["sepal length (cm)"].min()),
      max_value=float(df["sepal length (cm)"].max()),
      value=5.8,
      step=0.1,
  )
  sw = st.number_input(
      "Sepal Width (cm)",
      min_value=float(df["sepal width (cm)"].min()),
      max_value=float(df["sepal width (cm)"].max()),
      value=3.0,
      step=0.1,
  )
  pl = st.number_input(
      "Petal Length (cm)",
      min_value=float(df["petal length (cm)"].min()),
      max_value=float(df["petal length (cm)"].max()),
      value=4.3,
      step=0.1,
  )
  pw = st.number_input(
      "Petal Width (cm)",
      min_value=float(df["petal width (cm)"].min()),
      max_value=float(df["petal width (cm)"].max()),
      value=1.3,
      step=0.1,
  )

  st.divider()
  st.markdown("### 📌 Summary Inputs")
  st.write(f"• **Sepal:** {sl} x {sw} cm")
  st.write(f"• **Petal:** {pl} x {pw} cm")

# 5. Header Section
st.markdown("<h1>🔮 Iris Neural Classifier</h1>", unsafe_allow_html=True)
st.write("ศูนย์ประมวลผลและวิเคราะห์สายพันธุ์ดอกไอริสผ่านโมเดลปัญญาประดิษฐ์")
st.divider()

# 6. ML Inference
input_array = np.array([[sl, sw, pl, pw]])
pred_index = model.predict(input_array)[0]
probas = model.predict_proba(input_array)[0] * 100
predicted_flower = species_labels[pred_index]
confidence = probas[pred_index]

# 7. Hero Display (Prediction Banner)
st.markdown(
    f"""
    <div class="main-card">
        <p style="color: #E2D9F3; font-size: 1.1rem; margin-bottom: 5px;">ผลลัพธ์การวิเคราะห์จำแนกสายพันธุ์</p>
        <h1 style="color: #E0AFA0; font-size: 2.8rem; margin: 0;">Iris {predicted_flower} 🪻</h1>
        <p style="color: #C77DFF; font-size: 1.2rem; margin-top: 10px;">ระดับความมั่นใจของระบบ: <b>{confidence:.2f}%</b></p>
    </div>
""",
    unsafe_allow_html=True,
)

# 8. Main Body Layout (2 Columns)
c_left, c_right = st.columns([1, 1], gap="medium")

with c_left:
  st.markdown("### 📊 Probability Breakdown")

  prob_df = pd.DataFrame(
      {"Species": species_labels, "Probability (%)": probas}
  )

  # Donut / Pie Chart โทนม่วง นีออน
  fig_pie = px.pie(
      prob_df,
      values="Probability (%)",
      names="Species",
      hole=0.6,
      color_discrete_sequence=["#3C096C", "#7B2CBF", "#E0AAFF"],
  )
  fig_pie.update_layout(
      paper_bgcolor="rgba(0,0,0,0)",
      plot_bgcolor="rgba(0,0,0,0)",
      font=dict(color="#E2D9F3"),
      legend=dict(orientation="h", yanchor="bottom", y=-0.2),
  )
  st.plotly_chart(fig_pie, use_container_width=True)

with c_right:
  st.markdown("### 🌌 Feature Distribution Map")

  # 3D Scatter Plot (เปลี่ยนรูปแบบการนำเสนอข้อมูล)
  fig_3d = px.scatter_3d(
      df,
      x="sepal length (cm)",
      y="petal length (cm)",
      z="petal width (cm)",
      color="species",
      color_discrete_sequence=["#5A189A", "#9D4EDD", "#E0AAFF"],
      opacity=0.8,
  )
  fig_3d.update_layout(
      paper_bgcolor="rgba(0,0,0,0)",
      font=dict(color="#E2D9F3"),
      scene=dict(
          xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#331A54"),
          yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#331A54"),
          zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#331A54"),
      ),
      margin=dict(l=0, r=0, b=0, t=0),
  )
  st.plotly_chart(fig_3d, use_container_width=True)

# 9. Expandable Dataset Table
with st.expander("📂 เปิดดูฐานข้อมูลและค่าทางสถิติ (Raw Data & Statistics)"):
  st.dataframe(df.style.highlight_max(axis=0, color="#3C096C"))