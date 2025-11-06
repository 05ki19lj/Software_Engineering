import streamlit as st
from streamlit_option_menu import option_menu
import subprocess
import os
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="AI工具箱", layout="wide")

# === 側邊欄選單 ===
with st.sidebar:
    choose = option_menu(
        "工具栏", ["简介", "AI聊天", "AI绘画"],
        icons=['house', 'chat', 'brush'],
        menu_icon="list", default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                         "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#24A608"},
        }
    )

# === 簡介頁面 ===
if choose == "简介":
    st.markdown("### 🧰 AI百宝箱")
    st.markdown("這是一個整合多種 AI 功能的免費工具箱：")
    st.markdown("- 💬 本地 AI 聊天（使用 Ollama）")
    st.markdown("- 🎨 免費 AI 繪圖（使用 Pollinations API）")
    st.markdown("- ✅ 全部功能皆 **免 API Key**")

import subprocess

def local_chat(user_query):
    try:
        ollama_path = r"C:\Users\Tong\AppData\Local\Programs\Ollama\ollama.exe"

        result = subprocess.run(
            [ollama_path, "run", "llama3", user_query],
            capture_output=True
        )

        # 手動以 UTF-8 解碼，避免 cp950 錯誤
        stdout = result.stdout.decode("utf-8", errors="ignore") if result.stdout else ""
        stderr = result.stderr.decode("utf-8", errors="ignore") if result.stderr else ""

        if result.returncode == 0 and stdout.strip():
            return stdout.strip()
        else:
            return f"⚠️ Ollama 錯誤：{stderr or '沒有輸出結果'}"

    except FileNotFoundError:
        return "⚠️ 找不到 Ollama，可執行檔路徑可能錯誤。"
    except Exception as e:
        return f"⚠️ 聊天發生例外錯誤：{e}"



# === Pollinations 免費 AI 繪圖 ===
def generate_image_pollinations(prompt):
    url = f"https://image.pollinations.ai/prompt/{prompt}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"生成失敗，HTTP 狀態碼：{response.status_code}")
            return None
    except Exception as e:
        st.error(f"請求錯誤：{e}")
        return None

# === 聊天頁面 ===
if choose == "AI聊天":
    st.title("🗣️ AI聊天機器人（本地免費）")
    st.markdown("請確保已安裝 Ollama 並下載 `llama3` 模型。")
    user_query = st.text_input("輸入訊息：", "你好！")
    if st.button("發送"):
        if user_query:
            with st.spinner("思考中..."):
                response = local_chat(user_query)
                st.write(response)

# === AI 繪圖頁面 ===
elif choose == "AI绘画":
    st.title("🎨 免費 AI繪圖（Pollinations）")
    prompt = st.text_input("輸入圖片描述：", "一隻穿著太空衣的貓咪在月球上")
    if st.button("生成圖片"):
        if prompt:
            with st.spinner("生成中..."):
                image = generate_image_pollinations(prompt)
                if image:
                    st.image(image, caption="AI 生成圖片", width='stretch')
