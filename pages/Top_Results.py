import streamlit as st
from helper import center_header_type, import_params, DMSansFont
from helper import set_page_width, center_tabs, load_page_header, set_graph_tab_text_size


params = import_params("params.yaml")

st.set_page_config(
    page_title = params["page_config"]["page_title"],
    page_icon = params["page_config"]["page_icon"],
    initial_sidebar_state = params["page_config"]["initial_sidebar_state"]
)

DMSansFont()
set_page_width(params["page_config"]["page_width"])
center_tabs()
set_graph_tab_text_size("18")

page_title = "Fortune 500 Query Tool"
load_page_header(page_title)

with st.container():
    top_result_frame = st.session_state["search_results"]
    num_results = len(top_result_frame)
    if num_results == 0:
        st.markdown("#")
        st.markdown("#")
        center_header_type("No Matches to Graph", 2)
    else:
        max_20_results = min(num_results, 20)
        with st.container(border = True):
            comparison_slider = st.slider("Choose Number of Top Results to Graph", min_value = 1, max_value = max_20_results, value = max_20_results)
            graph_frame = top_result_frame.iloc[:comparison_slider]
        with st.container(border = True):
            revenue_tab, valuation_tab, profit_tab, profit_percent_sales_tab, num_employee_tab = st.tabs(["Revenue", "Valuation", "Profits", "Profits Percentage of Sales", "Number of Employees"])
            with revenue_tab:
                st.markdown("#### Revenue Graphs")
                st.bar_chart(graph_frame, x = "Company", y = "Revenue (millions)")
            with valuation_tab:
                st.markdown("#### Valuation Graphs")
                st.bar_chart(graph_frame, x = "Company", y = "Valuation (millions)")
            with profit_tab:
                st.markdown("#### Profit Graphs")
                st.bar_chart(graph_frame, x = "Company", y = "Profits (millions)")
            with profit_percent_sales_tab:
                st.markdown("#### Profit Percent of Sales Graphs")
                st.bar_chart(graph_frame, x = "Company", y = "Profits (% of Sales)")
            with num_employee_tab:
                st.markdown("#### Number of Employees Graphs")
                st.bar_chart(graph_frame, x = "Company", y = "Number of Employees")
            