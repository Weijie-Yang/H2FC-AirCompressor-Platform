import streamlit as st
import matplotlib.tri as tri
import pandas as pd
import os
import math
from pathlib import Path
# from openai import OpenAI # Keep this if you fix the API key issue
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pydeck as pdk
import plotly.figure_factory as ff
# from vega_datasets import data # Not used in your provided snippet
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from streamlit_echarts import st_echarts
import datetime
import random
import time
import json
from pyecharts.charts import Sunburst
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from bokeh.models import HoverTool
from bokeh.plotting import figure, show # show is for standalone, not needed in streamlit
# from bokeh.plotting import figure # Duplicate import
from bokeh.models import ColumnDataSource
from bokeh.palettes import Viridis3
from bokeh.layouts import gridplot
from bokeh.models import BoxSelectTool, LassoSelectTool
# from bokeh.plotting import curdoc, figure # curdoc not typically used in streamlit
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import matplotlib
import shutil
import tempfile
from sklearn import preprocessing
import matplotlib as mpl
import subprocess
# from pathlib import Path # Duplicate import
# import time # Duplicate import
import sys
import requests
from PIL import Image
from io import BytesIO
from streamlit.components.v1 import html
# from sklearn.preprocessing import StandardScaler # Duplicate import
from matplotlib.patches import Rectangle
from pyecharts.charts import Pie
# from bokeh.plotting import figure, show # Duplicate import
from bokeh.transform import cumsum
from bokeh.palettes import Spectral6
from streamlit.components.v1 import iframe
# import threading # Not used
# import webbrowser # Not used
# import http.server # Not used
# import socketserver # Not used
# import requests # Duplicate import

# Your local file/function import - ensure this file exists and works
# from pythonProject3.compute_normals import load_and_process_mesh, export_interactive_html

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --- Start of Recommended CSS Modifications ---

# 1. Remove the old, problematic html_code injection
# Your original `html_code` string is very aggressive in trying to redefine Streamlit's layout.
# We will replace it with a more targeted and safer approach.

# 2. Apply minimal, targeted CSS
# Goal: Achieve the dark theme and custom title without breaking Streamlit.
st.markdown("""
<style>
    /* Apply a background color to the body */
    body {
        background-color: #000d4a; /* Your desired dark blue background */
        color: white; /* Default text color to white for better contrast */
        font-family: "微软雅黑", sans-serif; /* Your desired global font */
    }

    /* Custom class for your main application title */
    .app-title {
        font-size: 2.2rem; /* Responsive font size */
        text-align: center; /* Center the main title */
        color: white;
        padding: 20px 0; /* Add some vertical spacing */
        font-family: "微软雅黑", sans-serif;
        /* Avoid negative margins that shift Streamlit's layout */
    }

    /* Make Streamlit's main content area transparent to see the body background */
    /* This can sometimes be tricky with Streamlit updates, but often works for backgrounds. */
    .main .block-container {
        background: none; /* Or background-color: transparent; */
    }

    /* Style Streamlit Tabs to be more visible on dark background */
    /* Be cautious: Streamlit's internal class names can change. */
    div[data-baseweb="tab-list"] button {
        color: #cccccc !important; /* Lighter tab text */
        background-color: transparent !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] {
        color: white !important; /* Selected tab text */
        border-bottom-color: #02a6b5 !important; /* Highlight for selected tab */
    }

    /* Style Streamlit Expander header */
    .st-emotion-cache-10trblm  /* This class might be unstable, check with browser dev tools */ {
        color: white !important;
        background-color: rgba(25,186,139,.1) !important; /* A subtle background for expander headers */
    }
    .st-emotion-cache-10trblm p {
        color: white !important;
    }


    /* Style for your custom containers/tiles if you still want borders */
    .custom-tile-styling {
        border: 1px solid rgba(25,186,139,.17);
        padding: 1rem; /* Use rem for responsive padding */
        background: rgba(255,255,255,.04);
        position: relative;
        margin-bottom: 1rem;
        /* The pseudo-elements for corners are more complex and might be omitted for simplicity
           or re-implemented carefully if essential. */
    }
    .custom-tile-header {
        font-size: 1.1rem;
        color: white;
        background: linear-gradient(45deg, #191c83, transparent);
        padding: 0.5rem 1rem;
        margin: -1rem -1rem 1rem -1rem; /* Adjust to fit within the .custom-tile-styling padding */
        font-family: "微软雅黑", sans-serif;
    }

    /* Ensure other Streamlit text elements are visible */
    div[data-testid="stMarkdown"] p,
    div[data-testid="stText"],
    label,
    .stButton>button,
    .stFileUploader label,
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput input,
    .stTextArea textarea,
    .stRadio label span,
    .stSlider label {
        color: white !important;
    }
    /* Specific for plotly chart labels if they turn black */
    .js-plotly-plot .plotly .xaxislayer-above .xtick text,
    .js-plotly-plot .plotly .yaxislayer-above .ytick text,
    .js-plotly-plot .plotly .legendtext {
        fill: white !important; /* For SVG text elements */
        color: white !important; /* For HTML-like elements if any */
    }


</style>
""", unsafe_allow_html=True)

# 3. Use the custom class for your title
st.markdown('<h1 class="app-title">氢燃料电池发动机系统空压机大数据平台</h1>', unsafe_allow_html=True)

# --- End of Recommended CSS Modifications ---


# Initialize session state, if not exists
if 'selected' not in st.session_state:
   st.session_state.selected = None
# st.markdown(""" """, unsafe_allow_html=True) # Removed, covered by above CSS block

# The original html_code block should be completely removed or commented out
# # HTML 代码
# html_code = """
# <!DOCTYPE html>
# ...
# </html>
# """
# st.markdown(html_code, unsafe_allow_html=True) # THIS IS THE LINE TO REMOVE/COMMENT

@st.cache_data
def get_gdp_data():
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    # Ensure this file exists and is in the correct path relative to your script
    # For now, I'll return an empty DataFrame if it's not crucial for the error.
    if not DATA_FILENAME.exists():
        st.warning(f"Warning: {DATA_FILENAME} not found. GDP data will be empty.")
        return pd.DataFrame()
    raw_gdp_df = pd.read_csv(DATA_FILENAME)
    # ... rest of your get_gdp_data function if it was complete
    return raw_gdp_df # Or the processed gdp_df

# gdp_df = get_gdp_data() # Call it if used, otherwise comment out


tabs = st.tabs(["首页", "数据分析", "趋势分析", "AI对话", "操作示例"])

# According to user's choice, display different page content
with tabs[0]:
    left, middle, right = st.columns([2.5, 5, 2.5])

    with left:
        row1_left = st.columns(1) # Renamed to avoid conflict
        row2_left = st.columns(1) # Renamed to avoid conflict

        with row1_left[0]:
            # Apply the custom-tile-styling here if you want that bordered look
            with st.container(): # Removed height, border=True and applied custom class via markdown
                st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
                st.markdown('<h2 class="custom-tile-header">数据库介绍</h2>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <p style="font-size:15px;"><strong>     本数据库包含氢燃料电池发动机系统空压机结构参数、性能指标等信息。平台用于研究在燃料电池电堆空压机设计研发过程中遇到的空压机结构设计匹配问题。利用大数据分析和机器学习，辅助河北金士顿有限公司空压机进行结构设计和大数据性能分析，辅助其完成数据检索，基于机器学习工具，训练空压机结构同性能间的关系，为燃料电池电堆空压机的设计提供理论指导。</strong></span>
                    </p>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

        with row2_left[0]:
            with st.container():
                st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
                st.markdown('<h2 class="custom-tile-header">数据库数据详情</h2>', unsafe_allow_html=True)
                # ... (rest of the content for this tile) ...
                # Example: Plotly figure
                x1 = np.random.randn(200) - 2
                x2 = np.random.randn(200)
                x3 = np.random.randn(200) + 2
                x4 = np.random.randn(200) + 4
                hist_data = [x1, x2, x3, x4]
                group_labels = ['Group 1', 'Group 2', 'Group 3', 'Group 4']
                colors = ['#70C7F3', ' #00F5FF', '#C724F1', '#00FFA3']
                fig1 = ff.create_distplot(hist_data, group_labels, colors=colors, bin_size=.2)
                fig1.update_layout(
                    height=230,
                    margin=dict(l=20, r=20, t=20, b=20), # Added top margin
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                    template="plotly_dark" # Use plotly's dark theme for consistency
                )
                st.plotly_chart(fig1, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)


    with middle:
        row1_middle = st.columns(1)
        with row1_middle[0]:
            with st.container():
                st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
                st.markdown('<h2 class="custom-tile-header">氢燃料电池发动机系统空压机性能总览图</h2>', unsafe_allow_html=True)
                # ... (content for middle tile) ...
                # Dummy data for the 3D scatter plot
                df01 = pd.Series(np.random.rand(50) * 100000) # Example: Speed
                df02 = pd.Series(np.random.rand(50) * 100)    # Example: Flow
                df03 = pd.Series(np.random.rand(50) * 0.8)    # Example: Efficiency

                fig_3d_middle = go.Figure(data=[go.Scatter3d(
                    x=df01, y=df02, z=df03,
                    mode='markers',
                    marker=dict(size=12, color=df03, colorscale='Viridis', opacity=0.8)
                )])
                fig_3d_middle.update_layout(
                    scene=dict(
                        zaxis=dict(showbackground=False, title="等熵效率"),
                        xaxis=dict(title="转速r/min"),
                        yaxis=dict(title="质量流量g/s"),
                        aspectmode="manual", aspectratio=dict(x=2, y=1, z=0.5),
                    ),
                    # width=500, # Let Streamlit handle width with use_container_width
                    height=480, # Adjusted height
                    margin=dict(l=0, r=0, b=0, t=0),
                    template="plotly_dark"
                )
                st.plotly_chart(fig_3d_middle, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    with right:
        row1_right = st.columns(1)
        row2_right = st.columns(1)

        with row1_right[0]:
            with st.container():
                st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
                st.markdown('<h2 class="custom-tile-header">数据库结构设计参数</h2>', unsafe_allow_html=True)
                # ... (content for top-right tile - Bokeh chart) ...
                # Bokeh example (simplified, ensure 'data' is defined if using sampledata)
                # from bokeh.sampledata.penguins import data as bokeh_penguins_data # If you use this
                # For now, creating dummy data for bokeh:
                bokeh_source = ColumnDataSource(data=dict(
                    flipper_length_mm=np.random.rand(50) * 50 + 180,
                    body_mass_g=np.random.rand(50) * 3000 + 3000,
                    species=['Adelie'] * 17 + ['Gentoo'] * 17 + ['Chinstrap'] * 16
                ))
                SPECIES = sorted(list(set(bokeh_source.data['species']))) # Correctly get unique species
                MARKERS = ['hex', 'circle_x', 'triangle']

                p_bokeh = figure(
                    tools="pan,wheel_zoom,box_zoom,reset,save,hover",
                    tooltips=[("种类", "@species"), ("Flipper Length", "@flipper_length_mm{0.0} mm"), ("Body Mass", "@body_mass_g{0} g")],
                    background_fill_alpha=0, # Transparent background
                    border_fill_alpha=0,
                    height=230 # Adjusted height
                )
                p_bokeh.scatter(
                    "flipper_length_mm", "body_mass_g", source=bokeh_source, size=10, # Adjusted size
                    fill_alpha=0.6, line_alpha=0.6,
                    color=factor_cmap('species', 'Category10_3', SPECIES),
                    marker=factor_mark('species', MARKERS, SPECIES),
                    legend_label="Species" # Add legend label
                )
                p_bokeh.xaxis.axis_label = 'Flipper Length (mm)'
                p_bokeh.yaxis.axis_label = 'Body Mass (g)'
                p_bokeh.xaxis.axis_label_text_color = "white"
                p_bokeh.yaxis.axis_label_text_color = "white"
                p_bokeh.title.text_color = "white"
                p_bokeh.xgrid.grid_line_color = "#555555"
                p_bokeh.ygrid.grid_line_color = "#555555"
                p_bokeh.axis.major_tick_line_color = "white"
                p_bokeh.axis.minor_tick_line_color = "white"
                p_bokeh.axis.major_label_text_color = "white"
                p_bokeh.legend.label_text_color = "white"
                p_bokeh.legend.background_fill_alpha = 0.3
                p_bokeh.legend.border_line_alpha = 0


                st.bokeh_chart(p_bokeh, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with row2_right[0]:
            with st.container():
                st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
                st.markdown('<h2 class="custom-tile-header">数据库数据类型</h2>', unsafe_allow_html=True)
                # ... (content for bottom-right tile - iframe or pyecharts) ...
                # For the iframe part:
                # If "http://192.168.43.181:9089/tzgy8hfiu2a1/" is a Pyecharts HTML file you generated,
                # you need to include that HTML file in your repository and serve it using st.components.v1.html
                # Example:
                # try:
                #     with open("path_to_your_chart.html", "r", encoding="utf-8") as f:
                #         chart_html = f.read()
                #     st.components.v1.html(chart_html, height=200, scrolling=False)
                # except FileNotFoundError:
                #     st.warning("Chart HTML file not found.")
                st.caption("Pyecharts/iframe content would go here. Ensure the source is accessible on deployment.")
                # Placeholder for now:
                # Creating a simple Pyecharts Pie chart as an example
                data_pie = [("国外论文", 72.34), ("国内论文", 27.66)]
                pie_chart = (
                    Pie()
                    .add(
                        "",
                        data_pie,
                        radius=["40%", "75%"],
                    )
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title="文献来源", title_textstyle_opts=opts.TextStyleOpts(color="white")),
                        legend_opts=opts.LegendOpts(
                            orient="vertical", pos_top="15%", pos_left="2%", textstyle_opts=opts.TextStyleOpts(color="white")
                        ),
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}%", color="white"))
                )
                st_pyecharts(pie_chart, height="220px")
                st.markdown('</div>', unsafe_allow_html=True)


with tabs[1]:
    left1, middle_spacer, middle1 = st.columns([0.3, 0.05, 0.65]) # Adjusted column ratios

    with left1:
        st.markdown('<div class="custom-tile-styling" style="height: 560px; overflow-y: auto;">', unsafe_allow_html=True) # Added fixed height and scroll
        st.markdown('<h2 class="custom-tile-header">数据录入</h2>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader("上传 CSV 或 XLSX 文件", type=["csv", "xlsx"], key="data_upload")

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, header=2)
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file, header=2, engine='openpyxl')
                st.session_state.df_uploaded = df # Store in session state
                st.success("文件上传成功!")
                st.dataframe(df.head(), height=300) # Show head with fixed height
            except Exception as e:
                st.error(f"读取文件时出错: {e}")
                if 'df_uploaded' in st.session_state:
                    del st.session_state.df_uploaded
        st.markdown('</div>', unsafe_allow_html=True)


    with middle1:
        st.markdown('<div class="custom-tile-styling" style="height: 560px; overflow-y: auto;">', unsafe_allow_html=True) # Added fixed height and scroll
        st.markdown('<h2 class="custom-tile-header">数据分析</h2>', unsafe_allow_html=True)

        if 'df_uploaded' in st.session_state and st.session_state.df_uploaded is not None:
            df = st.session_state.df_uploaded
            # Ensure df is not empty and has columns
            if not df.empty and not df.columns.empty:
                option = st.selectbox(
                    "图表类型选择",
                    ("散点图1 (Bokeh)", "相关性分析 (Matplotlib)", "直方图/KDE (Plotly FF)",
                     "间距不规则数据的等值线图 (Matplotlib)", "重叠密度山脊图 (Seaborn)",
                     "小提琴图 (Plotly GO)", "散点频率图 (Bokeh)", "简单散点图 (Bokeh)",
                     "二维散点图 (Matplotlib)", "三维散点图 (Matplotlib)"),
                    key="chart_type_select"
                )

                # --- Plotting logic (ensure df is passed and used correctly) ---
                # Example for "简单散点图 (Bokeh)"
                if option == "简单散点图 (Bokeh)":
                    all_columns = df.columns.tolist()
                    if not all_columns:
                        st.warning("上传的数据没有列名。")
                    else:
                        col1_sel, col2_sel = st.columns(2)
                        with col1_sel:
                            title1_bokeh = st.selectbox("选择X轴列", all_columns, index=0 if all_columns else 0, key="bokeh_x")
                        with col2_sel:
                            title2_bokeh = st.selectbox("选择Y轴列", all_columns, index=min(1, len(all_columns)-1) if len(all_columns)>1 else 0, key="bokeh_y")

                        # Data cleaning for selected columns
                        df_clean_bokeh = df[[title1_bokeh, title2_bokeh]].copy()
                        df_clean_bokeh[title1_bokeh] = pd.to_numeric(df_clean_bokeh[title1_bokeh], errors='coerce')
                        df_clean_bokeh[title2_bokeh] = pd.to_numeric(df_clean_bokeh[title2_bokeh], errors='coerce')
                        df_clean_bokeh.dropna(subset=[title1_bokeh, title2_bokeh], inplace=True)

                        if df_clean_bokeh.empty:
                            st.warning("选择的列经过清洗后没有有效数据。")
                        else:
                            source_bokeh_simple = ColumnDataSource(df_clean_bokeh)
                            hover_bokeh_simple = HoverTool(tooltips=[
                                (title1_bokeh, f"@{title1_bokeh}"), (title2_bokeh, f"@{title2_bokeh}"), ("索引", "$index")
                            ])
                            p_bokeh_simple = figure(
                                tools=[hover_bokeh_simple, "pan,wheel_zoom,box_zoom,reset"],
                                title=f"{title2_bokeh} vs {title1_bokeh}",
                                x_axis_label=title1_bokeh, y_axis_label=title2_bokeh,
                                background_fill_alpha=0, border_fill_alpha=0, height=350
                            )
                            p_bokeh_simple.scatter(
                                x=title1_bokeh, y=title2_bokeh, source=source_bokeh_simple, size=8,
                                fill_color="steelblue", alpha=0.6, line_color="white"
                            )
                            # Style for dark theme
                            p_bokeh_simple.title.text_color = "white"
                            p_bokeh_simple.xaxis.axis_label_text_color = "white"
                            p_bokeh_simple.yaxis.axis_label_text_color = "white"
                            p_bokeh_simple.xaxis.major_label_text_color = "white"
                            p_bokeh_simple.yaxis.major_label_text_color = "white"
                            p_bokeh_simple.xgrid.grid_line_color = "gray"
                            p_bokeh_simple.ygrid.grid_line_color = "gray"
                            p_bokeh_simple.xgrid.grid_line_alpha = 0.5
                            p_bokeh_simple.ygrid.grid_line_alpha = 0.5

                            st.bokeh_chart(p_bokeh_simple, use_container_width=True)
                # ... Add other plotting options here, ensuring df is available and handled ...
                elif option == "相关性分析 (Matplotlib)":
                    # (Your existing heatmap code, ensure it uses the uploaded 'df'
                    # and handles numeric conversion and NaN values. Also, apply dark theme style for matplotlib)
                    st.write("相关性分析图表将显示在此。确保Matplotlib图表适配暗色背景。")
                    # For Matplotlib on dark background:
                    # plt.style.use('dark_background') # Or set rcParams
                    # fig, ax = plt.subplots()
                    # ... your heatmap code ...
                    # ax.tick_params(colors='white')
                    # cbar.ax.yaxis.set_tick_params(color='white')
                    # cbar.set_label("Correlation", color='white')
                    # fig.patch.set_facecolor('#000d4a') # Match body background
                    # ax.set_facecolor('#000d4a')
                    # st.pyplot(fig)
                    pass # Placeholder for brevity

            else:
                st.info("请先上传有效的数据文件。")
        else:
            st.info("请先在左侧上传数据文件。")
        st.markdown('</div>', unsafe_allow_html=True)


with tabs[2]:
    st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
    st.markdown('<h2 class="custom-tile-header">趋势分析</h2>', unsafe_allow_html=True)
    # Your image display logic
    image_paths = [
        "pic/屏幕截图 2025-06-09 041644.png", "pic/屏幕截图 2025-06-09 041746.png",
        "pic/屏幕截图 2025-06-09 041757.png", "pic/屏幕截图 2025-06-09 041811.png",
        "pic/屏幕截图 2025-06-09 044732.png", "pic/屏幕截图 2025-06-09 044906.png",
        "pic/屏幕截图 2025-06-10 040204.png", "pic/屏幕截图 2025-06-10 040248.png",
        "pic/屏幕截图 2025-06-10 040259.png", "pic/屏幕截图 2025-06-10 040312.png",
        "pic/屏幕截图 2025-06-10 040325.png", "pic/屏幕截图 2025-06-10 040340.png",
        "pic/屏幕截图 2025-06-10 040352.png", "pic/屏幕截图 2025-06-10 040406.png"
    ]
    for img_path_str in image_paths:
        img_path = Path(img_path_str)
        if img_path.exists():
            try:
                image = Image.open(img_path)
                st.image(image, use_column_width=True) # Changed width to use_column_width
            except Exception as e:
                st.error(f"无法加载图片 {img_path}: {e}")
        else:
            st.warning(f"图片未找到: {img_path}")
    st.markdown('</div>', unsafe_allow_html=True)


with tabs[3]:
    st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
    st.markdown('<h2 class="custom-tile-header">AI对话</h2>', unsafe_allow_html=True)
    st.title("💬 Chatgpt")
    st.write(
        "这是一个简单的聊天机器人... (your description)"
    )

    # Use Streamlit Secrets for API key on deployment
    # For local, you can use text_input or environment variables
    openai_api_key_input = st.text_input("OpenAI API Key (可选, 优先使用Secrets)", type="password", key="api_key_input")
    
    # Attempt to get from secrets first
    openai_api_key = st.secrets.get("OPENAI_API_KEY") 
    if not openai_api_key: # Fallback to input if not in secrets
        openai_api_key = openai_api_key_input

    if not openai_api_key:
        st.warning("请输入您的OpenAI API密钥以使用聊天功能。或在部署时将其添加到Streamlit Secrets中。")
    else:
        try:
            from openai import OpenAI # Import here after key check
            client = OpenAI(api_key=openai_api_key)
            # Test query to ensure key is valid (optional, remove if too slow)
            # client.models.list()

            if "openai_model" not in st.session_state:
                st.session_state["openai_model"] = "gpt-3.5-turbo"
            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("您有什么问题?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    try:
                        stream = client.chat.completions.create(
                            model=st.session_state["openai_model"],
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ],
                            stream=True,
                        )
                        response = st.write_stream(stream)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"与OpenAI API通信时出错: {e}")

        except ImportError:
             st.error("OpenAI Python库未安装。请运行 'pip install openai'.")
        except Exception as e:
            st.error(f"初始化OpenAI客户端时出错或API密钥无效: {e}")
    st.markdown('</div>', unsafe_allow_html=True)


with tabs[4]:
    st.markdown('<div class="custom-tile-styling">', unsafe_allow_html=True)
    st.markdown('<h2 class="custom-tile-header">操作示例</h2>', unsafe_allow_html=True)
    st.write("这是操作示例页面")

    with st.expander("EDA (探索性数据分析)"):
        st.write("""
           EDA（Exploratory Data Analysis，探索性数据分析）是一种数据分析方法...
           (Your full EDA description)
        """)
        # Example image, ensure it exists
        eda_img_path = Path("pic/eda_example.png") # Replace with a relevant image
        if eda_img_path.exists():
            st.image(str(eda_img_path))
        else:
            st.image("https://static.streamlit.io/examples/dice.jpg") # Fallback

    with st.expander("分类"):
        st.write("分类任务说明...")
        # Example image, ensure it exists
        classification_img_path = Path("pic/classification_example.png") # Replace
        if classification_img_path.exists():
            st.image(str(classification_img_path))
        else:
            st.image("https://static.streamlit.io/examples/dice.jpg") # Fallback

    with st.expander("回归"):
        st.write("""
           回归分析是确定两种或多种变数间相互依赖的定量关系的一种统计分析方法...
           (Your full regression description)
        """)
        # Example image, ensure it exists
        regression_img_path = Path("pic/regression_example.png") # Replace
        if regression_img_path.exists():
            st.image(str(regression_img_path))
        else:
            st.image("https://static.streamlit.io/examples/dice.jpg") # Fallback
    st.markdown('</div>', unsafe_allow_html=True)
