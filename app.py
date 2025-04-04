import streamlit as st

# Base constants
BASE_BRANDED_COST = 178750
BASE_UNBRANDED_DISCOUNT = 0.20
ADDITIONAL_PAGE_COST = 17875
ADDITIONAL_REVIEW_COST = 13406.25
BASE_FULL_CONTENT_COST = 424875
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

# Cost Calculation
cost = BASE_BRANDED_COST

# Adjust for branded/unbranded
if branded == 'Unbranded':
    cost -= cost * BASE_UNBRANDED_DISCOUNT

# Adjust pages
cost += (pages - 2) * ADDITIONAL_PAGE_COST

# Adjust reviews
additional_reviews = (client_reviews - 2 + prc_reviews - 2)
cost += additional_reviews * ADDITIONAL_REVIEW_COST

# Adjust for content reuse
content_multiplier = {
    '0%': BASE_FULL_CONTENT_COST,
    '25%': BASE_BRANDED_COST + (BASE_FULL_CONTENT_COST - BASE_BRANDED_COST) * 0.75,
    '50%': BASE_BRANDED_COST + (BASE_FULL_CONTENT_COST - BASE_BRANDED_COST) * 0.50,
    '75%': BASE_BRANDED_COST + (BASE_FULL_CONTENT_COST - BASE_BRANDED_COST) * 0.25,
    '100%': BASE_BRANDED_COST
}
cost = content_multiplier[existing_content_pct] + (pages - 2) * ADDITIONAL_PAGE_COST + additional_reviews * ADDITIONAL_REVIEW_COST

# Adjust for coding
if doing_dev == 'No':
    cost -= cost * NO_CODING_DISCOUNT

# Adjust for CMS
if has_cms == 'Yes':
    cost += cost * CMS_COST_INCREASE

# Final presentation
st.subheader('Total Estimated Cost')
st.markdown(f"## ${cost:,.2f}")

# Display assumptions
st.markdown('### Assumptions:')
st.write(f'- Branded: {branded}')
st.write(f'- Number of Pages: {pages}')
st.write(f'- Number of Client Reviews: {client_reviews}')
st.write(f'- Number of PRC Reviews: {prc_reviews}')
st.write(f'- Existing Content Usage: {existing_content_pct}')
st.write(f'- Development Included: {doing_dev}')
st.write(f'- CMS Backend: {has_cms}')
st.write(f'- Hourly Rate: ${hourly_rate}/hr (Fixed)')

if doing_dev == 'Yes':
    st.write('- Assumption: We are hosting in our environment for both production and development.')
else:
    st.write('- Assumption: We are not responsible for coding, hosting, testing, or launch.')
