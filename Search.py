import streamlit as st
import pandas as pd
from helper import DMSansFont, load_page_header, center_tabs
from helper import import_params, set_page_width
from page_logic import query_page

params = import_params("params.yaml")

st.set_page_config(
    page_title = params["page_config"]["page_title"],
    page_icon = params["page_config"]["page_icon"],
    initial_sidebar_state = params["page_config"]["initial_sidebar_state"]
)

DMSansFont()
set_page_width(params["page_config"]["page_width"])
center_tabs()

page_title = "Fortune 500 Query Tool"
load_page_header(page_title)

query_page()
