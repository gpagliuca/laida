__author__ = "Giuseppe Pagliuca"
__version__ = "0.1.0"

import sys
import time

import matplotlib.pyplot as plt
import requests
import streamlit as st
import yaml

plt.style.use("fivethirtyeight")


# Functions
# ------------------------------------------------------------------------------
def get_system():
    r = requests.get("http://{}:61208/api/4/system/".format(server))
    return r.json()


def get_gpu():
    r = requests.get("http://{}:61208/api/4/gpu/".format(server))
    return r.json()


def get_cpu():
    r = requests.get("http://{}:61208/api/4/cpu".format(server))
    return r.json()


def get_mem():
    r = requests.get("http://{}:61208/api/4/mem".format(server))
    return r.json()


def get_sensors():
    r = requests.get("http://{}:61208/api/4/sensors".format(server))
    return r.json()


def get_ip():
    r = requests.get("http://{}:61208/api/4/ip".format(server))
    return r.json()


# Settings
# ------------------------------------------------------------------------------
with open("./settings.yaml", "r") as fobj:
    settings = yaml.safe_load(fobj)
    if sys.argv[1] == "remote":
        server = settings["ip"]
    else:
        server = "localhost"

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

# Main
# ------------------------------------------------------------------------------
system = get_system()
cpu = get_cpu()
gpu = get_gpu()
mem = get_mem()
ip = get_ip()
sensors = get_sensors()

# UI
# ------------------------------------------------------------------------------

# System info
# st.table(system)

# Metrics
st.header("GPU metrics", divider=True)
c0, c1, c2 = st.columns(3)
with c0:
    st.metric("Temperature", str(gpu[1]["temperature"]) + " °C")
with c1:
    st.metric("Fan speed", gpu[1]["fan_speed"])
with c2:
    st.metric("Memory", gpu[1]["mem"])

# Donut plots
c0, c1, c2 = st.columns(3)
with c0:
    st.header("CPU")
    width = 0.3
    vals = [cpu["total"], 60]
    fig, ax = plt.subplots()
    ax.pie(
        vals,
        startangle=90,
        colors=["r", "silver"],
        wedgeprops={
            "width": width,
        },
    )
    st.pyplot(fig)

with c1:
    st.header("GPU")
    width = 0.3
    vals = [gpu[1]["proc"], 60]
    fig, ax = plt.subplots()
    ax.pie(vals, startangle=90, colors=["r", "silver"], wedgeprops={"width": width})
    st.pyplot(fig)

with c2:
    st.header("Memory")
    width = 0.3
    vals = [mem["percent"], 60]
    fig, ax = plt.subplots()
    ax.pie(vals, startangle=90, colors=["r", "silver"], wedgeprops={"width": width})
    st.pyplot(fig)

while True:
    time.sleep(5)
    st.rerun()
