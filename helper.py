import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader


def import_params(path):
    with open(path) as file:
        config = yaml.load(file, Loader=SafeLoader)
        return config

def set_page_width(page_width):
    width_css = '<style>section.main > div {max-width:' + f'{page_width}' + 'rem}</style>'
    st.html(width_css)

def DMSansFont():
    """Styles app-wide font as DM Sans. Currently known to work for headers, captions, text, and dataframes, metric cards, and some plots.

    """
    font_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap');

        html, body * {
            font-family: 'DM Sans', sans-serif !important;
        }

        [data-testid="stDataFrame"] {
            font-family: 'DM Sans', sans-serif !important;
        }
        
        [data-testid="data-grid-canvas"] {
            --gdg-font-family: 'DM Sans', sans-serif !important;
        }
        </style>
        """
    st.html(font_style)

def center_header_type(header: str, h = 1) -> None:
    """Creates a center aligned header of specified h1 through h6. 
    Similar to st.markdown('##### {header}'), just aligned center within the container

    Args:
        header (str): Text to be displayed in the header
        h (int): 1 through 6. HTML header level to be used
    """
    if h not in [1, 2, 3, 4, 5, 6]:
        raise ValueError("h must be one of [1, 2, 3, 4, 5, 6]")
    st.html(f"<h{h} style='text-align: center; padding-bottom: 0; padding-top: 0; gap: 0rem;'>{header}</h{h}>")

def add_vertical_space(num_lines = 1) -> None:
    """Adds vertical space between two elements. 

    Args:
        num_lines (int, optional): The number of h6 lines of spacing to add. Defaults to 1.
    """
    for i in range(0,num_lines + 1):
        st.markdown(" ###### ")


@st.cache_data
def load_page_header(title_text):
    header_string = "# "
    page_title = header_string + title_text

    logo_path = "assets/pd_logo_light_mode.png"

    title_col, logo_col = st.columns([.75, .25])
    with title_col:
        st.markdown(page_title)
    with logo_col:
        st.markdown("#####")
        st.image(logo_path, width = 280)

    st.markdown("##")


def center_tabs():
    CENTER_TAB_CSS = """
    <style>
       button[data-baseweb="tab"] {
       margin: 0;
       width: 100%;
       }
    </style>"""
    st.html(CENTER_TAB_CSS)

# :has(div#graph_text)

def set_graph_tab_text_size(text_size_string):
    GRAPH_SIZE_CSS = f'''
        <style>
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
            font-size: {text_size_string}px;
            }}
        </style>
        '''
    st.html(GRAPH_SIZE_CSS)


def set_button_color():
    BUTTON_COLOR_CSS = '''
        <style>
            button[kind="primaryFormSubmit"] {
            background-color: #006ec7 !important;
            border: #006ec7 !important;
            }
        </stlye>
    '''
    st.html(BUTTON_COLOR_CSS)

def clean_columns(column_series):
    column_series = column_series.fillna('0')
    int_string_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
    column_series = ["".join([char for char in entry if char in int_string_list]) for entry in column_series]
    column_series = [int(entry) for entry in column_series]
    return column_series


@st.cache_data
def load_data(file_path):
    company_df = pd.read_csv(file_path)
    columns_to_clean = ["Number of Employees", "Revenue (millions)", "Valuation (millions)", "Profits (millions)"]
    company_df[columns_to_clean] = company_df[columns_to_clean].apply(clean_columns)
    unique_industries = company_df["Industry"].unique()
    unique_states = company_df["State"].unique()
    return company_df, unique_industries, unique_states


def fileter_search(df, min_rank, max_rank, industries, states, min_employees, max_employees, max_companies, min_revenue, max_revanue, min_valuation, max_valuation, min_profit, max_profit):
    display_frame = df
    if min_rank is not None:
        display_frame = df[df["Rank"] >= min_rank]
    if max_rank is not None:
        display_frame = df[df["Rank"] <= max_rank]
    if min_employees is not None:
        display_frame = display_frame[display_frame["Number of Employees"] >= min_employees]
    if max_employees is not None:
        display_frame = display_frame[display_frame["Number of Employees"] <= max_employees]
    if min_revenue is not None:
        display_frame = display_frame[display_frame["Revenue (millions)"] >= min_revenue]
    if max_revanue is not None:
        display_frame = display_frame[display_frame["Revenue (millions)"] <= max_revanue]
    if min_valuation is not None:
        display_frame = display_frame[display_frame["Valuation (millions)"] >= min_valuation]
    if max_valuation is not None:
        display_frame = display_frame[display_frame["Valuation (millions)"] <= max_valuation]
    if min_profit is not None:
        display_frame = display_frame[display_frame["Profits (millions)"] >= min_profit]
    if max_profit is not None:
        display_frame = display_frame[display_frame["Profits (millions)"] <= max_profit]
    if len(industries) > 0:
        display_frame = display_frame[display_frame["Industry"].isin(industries)]
    if len(states) > 0:
        display_frame = display_frame[display_frame["State"].isin(states)]
    display_frame = display_frame.iloc[:max_companies]
    return display_frame