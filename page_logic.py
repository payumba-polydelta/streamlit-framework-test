import streamlit as st
import pandas as pd
from helper import load_data, set_button_color
from helper import fileter_search, center_header_type


def query_page():
    # Get Fortune 500 data
    company_df, unique_industries, unique_states = load_data("fortune-500.csv")

    setting_col, display_col = st.columns([.35, .65], gap = "small")
    
    # Column for configuring search details
    with setting_col:
        # Form contains all setting configurations
        with st.form("setting_form"):
            st.markdown("### Company Selection Settings")
            included_industries_multiselecet = st.multiselect("Industries to Include in Search", unique_industries, placeholder = "Leave Blank to Select All")

            # Revanue, valuation, and profit range tabs
            with st.container(border=True):
                revanue_range_tab, valuation_range_tab, profit_range_tab = st.tabs(["Set Revanue Range", "Set Valuation Range", "Set Profit Range"])
                with revanue_range_tab:
                    min_col, max_col = st.columns([.5, .5])
                    with min_col:
                        min_revenue_input = st.number_input("Minimum Revenue (millions):", value = None, format = '%.0f', placeholder = "No Min")
                    with max_col:
                        max_revenue_input = st.number_input("Maximum Revenue (millions):", value = None, format = '%.0f', placeholder = "No Max")
                with valuation_range_tab:
                    min_col, max_col = st.columns([.5, .5])
                    with min_col:
                        min_valuation_input = st.number_input("Minimum Valuation (millions):", value = None, format = '%.0f', placeholder = "No Min")
                    with max_col:
                        max_valuation_input = st.number_input("Maximum Valuation (millions):", value = None, format = '%.0f', placeholder = "No Max")
                with profit_range_tab:
                    min_col, max_col = st.columns([.5, .5])
                    with min_col:
                        min_profit_input = st.number_input("Minimum Profit (millions):", value = None, format = '%.0f', placeholder = "No Min")
                    with max_col:
                        max_profit_input = st.number_input("Maximum Profit (millions):", value = None, format = '%.0f', placeholder = "No Max")
            
            # Min/Max employees/rank
            with st.container(border=True):
                min_additional_col, max_additional_col = st.columns([.5, .5])
                with min_additional_col:
                    min_employee_input = st.number_input("Minimum Number of Employees:", value = None, format = '%.0f', placeholder = "No Min")
                    min_rank_input = st.number_input("Minimum Company Rank:", min_value = 1, max_value = 500, value = None, format = '%d', placeholder = "No Min")
                with max_additional_col:
                    max_employee_input = st.number_input("Maximum Number of Employees:", value = None, format = '%.0f', placeholder = "No Max")
                    max_rank_input = st.number_input("Maximum Company Rank:", min_value = 1, max_value = 500, value = None, format = '%d', placeholder = "No Min")

            # Additional Selection Parameters
            with st.expander("Additional Parameters"):
                with st.container():
                    companay_states_multiselect = st.multiselect("States to Include in Search", unique_states, placeholder = "Leave Blank to Select All")
                    max_companies_input = st.number_input("Max Number of Companies Returned (1-500)", 1, 500, value = 500)

            set_button_color()
            st.form_submit_button("Run Search", type = 'primary', use_container_width = True)

    
    # Column that displays search results
    with display_col:
        display_frame = fileter_search(company_df, min_rank_input, max_rank_input, included_industries_multiselecet, companay_states_multiselect, min_employee_input, max_employee_input, max_companies_input, min_revenue_input, max_revenue_input, min_valuation_input, max_valuation_input, min_profit_input, max_profit_input)
        display_frame.index = range(1, len(display_frame) + 1)
        st.session_state["search_results"] = display_frame
        num_matches = len(display_frame)
        with st.container(border=True):
            result_string = f"Result: There are {num_matches} Companies that Match Your Criteria"
            center_header_type(result_string, 3)
        
        if (num_matches < 14) & (num_matches >= 1):
            st.write(display_frame)
        elif num_matches > 14:
            st.dataframe(display_frame, height = 540)
            


                    





