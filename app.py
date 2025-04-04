import streamlit as st

# Inline CSS for Sidebar Navigation and Footer
st.markdown(
    """
    <style>
    /* Sidebar style */
    [data-testid="stSidebar"] {
        background-color: #f0f0f0;
        width: 240px !important;
        padding: 10px;
    }
    /* Navigation styling */
    .custom-nav ul {
        list-style: none;
        margin: 0;
        padding: 0;
    }
    .custom-nav li {
        margin: 0;
        padding: 2px 0;
        text-align: left;
    }
    .custom-nav li a {
        text-decoration: none;
        color: inherit;
        display: block;
        padding: 2px 5px;
    }
    .custom-nav li.active a {
        background-color: #d3d3d3;
        border-radius: 4px;
        padding: 2px 5px;
        width: 100%;
        box-sizing: border-box;
    }
    /* Footer styling */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        background-color: #444444;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 20px;
        font-size: 0.9em;
        z-index: 99999;
    }
    .custom-footer a {
        color: #dddddd;
        margin: 0 10px;
        text-decoration: none;
    }
    .custom-footer a:hover {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation Pane
with st.sidebar:
    st.markdown(
        """
        <div class="custom-nav">
          <ul>
            <li><a href="#">Find Real Patients</a></li>
            <li><a href="https://full-site-demo-rtvuylvub3w6fbvdurdgbx.streamlit.app/">Tactical Plans</a></li>
            <li class="active"><a href="https://costcalculator-5zcyncr2pzv4baam2w54e6.streamlit.app/">Cost Calculator</a></li>
            <li><a href="https://landscapeassessment-dnjxq2mzzamu4ekog5y2ew.streamlit.app/">Landscape Analysis</a></li>
            <li><a href="#">Pipeline Outlook</a></li>
            <li><a href="#">Create Messaging</a></li>
            <li><a href="#">Campaign Concepts</a></li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Constants
BASE_BRANDED_COST_10_PAGES = 178750
BASE_FULL_CONTENT_COST_10_PAGES = 424875
ADDITIONAL_PAGE_COST = 17875
ADDITIONAL_REVIEW_COST = 13406.25
CMS_COST_INCREASE = 0.10
NO_CODING_DISCOUNT = 0.20

# Streamlit UI
st.title('Pharma Website Cost Estimator')

# Inputs
branded = st.radio('Branded or Unbranded?', ['Branded', 'Unbranded'], index=0)
pages = st.number_input('Number of Pages', min_value=2, value=10, step=1)
client_reviews = st.number_input('Number of Client Reviews', min_value=2, value=2, step=1)
prc_reviews = st.number_input('Number of PRC Reviews', min_value=2, value=2, step=1)
existing_content_pct = st.selectbox('Site to Use Existing Content', ['0%', '25%', '50%', '75%', '100%'], index=4)
doing_dev = st.radio('Are we doing Development?', ['Yes', 'No'], index=0)
has_cms = st.radio('Does this have a CMS Backend?', ['No', 'Yes'], index=0)
hourly_rate = 275  # Fixed for now, not editable by user

# Calculate base costs based on pages
page_difference = pages - 10

branded_base = BASE_BRANDED_COST_10_PAGES + (page_difference * ADDITIONAL_PAGE_COST)
full_content_base = BASE_FULL_CONTENT_COST_10_PAGES + (page_difference * ADDITIONAL_PAGE_COST)

# Content reuse calculation
content_multiplier = {
    '0%': full_content_base,
    '25%': branded_base + (full_content_base - branded_base) * 0.75,
    '50%': branded_base + (full_content_base - branded_base) * 0.50,
    '75%': branded_base + (full_content_base - branded_base) * 0.25,
    '100%': branded_base
}

cost = content_multiplier[existing_content_pct]

# Adjust for branded/unbranded
if branded == 'Unbranded':
    cost *= 0.80

# Adjust reviews
additional_reviews = (client_reviews - 2 + prc_reviews - 2)
cost += additional_reviews * ADDITIONAL_REVIEW_COST

# Adjust for coding
if doing_dev == 'No':
    cost *= (1 - NO_CODING_DISCOUNT)

# Adjust for CMS
if has_cms == 'Yes':
    cost *= (1 + CMS_COST_INCREASE)

# Final presentation
st.subheader('Total Estimated Cost')
st.markdown(f"## ${cost:,.2f}")

# Display assumptions dynamically
assumptions = [
    f'Branded: {branded}',
    f'Number of Pages: {pages}',
    f'Number of Client Reviews: {client_reviews}',
    f'Number of PRC Reviews: {prc_reviews}',
    f'Existing Content Usage: {existing_content_pct}',
    f'Development Included: {doing_dev}',
    f'CMS Backend: {has_cms}',
    f'Hourly Rate: ${hourly_rate}/hr (Fixed)',
    'Assumption: Costs include standard project management and account services.',
    'Assumption: Content strategy and UX design are based on industry standards.',
    'Assumption: Two design concepts provided; additional concepts billed separately.',
    'Assumption: All photography and assets provided by client unless otherwise specified.'
]

if doing_dev == 'Yes':
    assumptions.append('Assumption: We are hosting in our environment for production and development.')
else:
    assumptions.append('Assumption: We are not responsible for coding, hosting, testing, or launch.')

st.markdown('### Assumptions:')
for assumption in assumptions:
    st.markdown(f'- {assumption}', unsafe_allow_html=True)

# Footer
footer_html = """
<footer class="custom-footer">
  <div style="text-align: left; flex: 1;">© Philip Storer 2025</div>
  <div>
    <a href="#">Terms of Use</a> |
    <a href="#">Privacy Policy</a> |
    <a href="#">Cookie Settings</a> |
    <a href="#">Contact Us</a>
  </div>
</footer>
"""
st.markdown(footer_html, unsafe_allow_html=True)
