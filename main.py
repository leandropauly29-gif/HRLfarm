import streamlit as st
import pandas as pd
import google.generativeai as genai

# Isso garante que o app não quebre se a chave estiver vazia
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyDokYZR8A4lmtGEb0xVX4160fY2j0EOyHA")
genai.configure(api_key=API_KEY)
