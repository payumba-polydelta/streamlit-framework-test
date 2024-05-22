import streamlit as st
import pandas as pd

st.set_page_config(page_icon="🧊",
                   layout="wide",
                  )

st.title("Fortune 500 App")

# Get Fortune 500 data
@st.cache_data
def load_data(file_path):
    company_df = pd.read_csv(file_path)
    unique_industries = company_df["Industry"].unique()
    employee_range_options = ["Any", "< 5000", "5000 - 19,999", "20,000 - 49,999", "50,000 - 99,999", "100,000 - 200,000", "\> 200,000" ]
    conversion = [[1, 9999999999], [1, 4999], [5000, 19999], [20000, 49999], [50000, 99999], [100000, 200000], [200000, 9999999999]]
    employee_range_conversion = dict(zip(employee_range_options, conversion))
    int_string_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return company_df, unique_industries, employee_range_options, employee_range_conversion, int_string_list

company_df, unique_industries, employee_range_options, employee_range_conversion, int_string_list = load_data("fortune-500.csv")

with st.sidebar:
    st.markdown("# Pretend This is Multipage")

def fileter_search(df, rank_range, included_industries, num_employee_range, max_companies):
    rank_low, rank_high = rank_range[0], rank_range[1]
    display_frame = df[(df["Rank"] >= rank_low) & (df["Rank"] <= rank_high)]
    if len(included_industries) > 0:
        display_frame = display_frame[display_frame["Industry"].isin(included_industries)]
    employee_range = employee_range_conversion[num_employee_range]
    employee_low, employee_high = employee_range[0], employee_range[1]
    display_frame["Number of Employees"] = ["".join([char for char in entry if char in int_string_list]) for entry in display_frame["Number of Employees"]]
    display_frame["Number of Employees"] = display_frame["Number of Employees"].apply(lambda x: int(x))
    display_frame = display_frame[(display_frame["Number of Employees"] >= employee_low) & (display_frame["Number of Employees"] <= employee_high)]
    display_frame = display_frame.iloc[:max_companies]
    return display_frame

setting_col, display_col = st.columns([.3, .7], gap = "large")

with setting_col:
    with st.form("setting_form"):
        st.header("Company Selection Settings")
        included_industries_multiselecet = st.multiselect("Choose Industries", unique_industries, placeholder = "Leave Blank to Select All")
        max_companies_input = st.number_input("Max Number of Selected Companies (1-500)", 1, 500, value = 500)
        with st.expander("Additional Parameters"):
            rank_range_slider = st.slider("Choose from companies with ranks between:", 1, 500, (1, 500))
            pop_left, pop_mid, pop_right = st.columns([1, 1, 1])
            with pop_mid:
                with st.popover("Number of Employees"):
                    num_employee_radio = st.radio("Selecet:", employee_range_options)
        st.form_submit_button("Submit")
    
    with st.expander("All Results"):
        display_frame = fileter_search(company_df, rank_range_slider, included_industries_multiselecet, num_employee_radio, max_companies_input)
        display_frame.index = range(1, len(display_frame) + 1)
        display_frame


with display_col:
    st.header("Top Results (up to 10)")
    with st.container():
        top_result_frame = display_frame.iloc[:10]
        top_result_table = st.table(top_result_frame)
    with st.container():
        st.header("Comparison")
        modified_int_string_list = int_string_list + ["-"]
        revanue_tab, valuation_tab, profit_tab, profit_percent_sales_tab, num_employee_tab = st.tabs(["Revanue", "Valuation", "Profits", "Profits Percentage of Sales", "Number of Employees"])
        with revanue_tab:
            st.markdown("#### Revanue Graphs")
            top_result_frame["Revenue (millions)"] = ["".join([char for char in entry if char in modified_int_string_list]) for entry in top_result_frame["Revenue (millions)"]]
            top_result_frame["Revenue (millions)"] = top_result_frame["Revenue (millions)"].apply(lambda x: int(x))
            st.bar_chart(top_result_frame, x = "Company", y = "Revenue (millions)")
        with valuation_tab:
            st.markdown("#### Valuation Graphs")
            top_result_frame["Valuation (millions)"] = ["".join([char for char in entry if char in modified_int_string_list]) for entry in top_result_frame["Valuation (millions)"]]
            top_result_frame["Valuation (millions)"] = top_result_frame["Valuation (millions)"].apply(lambda x: int(x))
            st.bar_chart(top_result_frame, x = "Company", y = "Valuation (millions)")
        with profit_tab:
            st.markdown("#### Profit Graphs")
            top_result_frame["Profits (millions)"] = ["".join([char for char in entry if char in modified_int_string_list]) for entry in top_result_frame["Profits (millions)"]]
            top_result_frame["Profits (millions)"] = top_result_frame["Profits (millions)"].apply(lambda x: int(x))
            st.bar_chart(top_result_frame, x = "Company", y = "Profits (millions)")
        with profit_percent_sales_tab:
            st.markdown("#### Profit Percent of Sales Graphs")
            st.bar_chart(top_result_frame, x = "Company", y = "Profits (% of Sales)")
        with num_employee_tab:
            st.markdown("#### Number of Employees Graphs")
            st.bar_chart(top_result_frame, x = "Company", y = "Number of Employees")





