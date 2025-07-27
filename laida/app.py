import time

import matplotlib.pyplot as plt
import requests
import streamlit as st

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1


def get_system():
    r = requests.get("http://localhost:61208/api/4/system/")
    return r.json()


def get_gpu():
    r = requests.get("http://localhost:61208/api/4/gpu/")
    return r.json()


def get_cpu():
    r = requests.get("http://localhost:61208/api/4/cpu")
    return r.json()


def get_mem():
    r = requests.get("http://localhost:61208/api/4/mem")
    return r.json()


system = get_system()
cpu = get_cpu()
gpu = get_gpu()
mem = get_mem()


c0, c1, c2 = st.columns(3)
with c0:
    st.header("CPU")
    width = 0.3
    vals = [cpu["total"], 60]
    fig, ax = plt.subplots()
    ax.pie(vals, startangle=90, wedgeprops={"width": width})
    st.pyplot(fig)

with c1:
    st.header("GPU")
    width = 0.3
    vals = [gpu[1]["proc"], 60]
    fig, ax = plt.subplots()
    ax.pie(vals, startangle=90, wedgeprops={"width": width})
    st.pyplot(fig)

with c2:
    st.header("Memory")
    width = 0.3
    vals = [mem["percent"], 60]
    fig, ax = plt.subplots()
    ax.pie(vals, startangle=90, wedgeprops={"width": width})
    st.pyplot(fig)

while True:
    time.sleep(5)
    st.header(f"This page has run {st.session_state.counter} times.")
    st.rerun()
