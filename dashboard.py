import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SCA Risk Dashboard", layout="wide", page_icon="")

# --- DATA TABLES ---

# 1. Asset Valuation
asset_data = {
    'Asset ID': [1, 2, 3, 4, 5, 6, 7],
    'Asset Category': ['People', 'People', 'Procedures', 'Data', 'Software', 'Hardware', 'Hardware'],
    'Subcategory': ['Employed by this company', 'Employed by partners', 'Ops Procedures', 
                    'Electronic data', 'RMS & apps', 'System Devices', 'Networking Devices'],
    'Weighted Score': [3.4, 2.4, 3.2, 5.0, 3.8, 2.8, 3.2],
    '% of Max': [68.0, 48.0, 64.0, 100.0, 76.0, 56.0, 64.0]
}
df_assets = pd.DataFrame(asset_data)

# 2. Threat Valuation
threat_data = {
    'Threat ID': ['T-01', 'T-02', 'T-03', 'T-04', 'T-05', 'T-06'],
    'Threat Name': ['Social Engineering', 'Power Interruptions', 'Human Error', 'Cross-Site Scripting', 'SQL Injections', 'Data Breach'],
    'Likelihood': [9, 9, 8, 7, 6, 6],
    'Rank': [1, 2, 3, 4, 5, 6]
}
df_threats = pd.DataFrame(threat_data)

# 3. TVA Table (Qualitative - Lab 12)
tva_data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8],
    'Asset': ['Electronic Data', 'Electronic Data', 'Electronic Data', 'Electronic Data', 'RMS Software', 'RMS Software', 'Hardware', 'Staff'],
    'Threat': ['Human Error', 'Human Error', 'SQL Injections', 'Data Breach', 'XSS Attack', 'XSS Attack', 'Power Loss', 'Social Engineering'],
    'Vulnerability': ['Mental Stress / Fatigue', 'Fear to Consult', 'Malfunctioned queries', 'Backdoors in code', 
                      'Susceptibility to Malicious Code', 'Unsanitized input fields', 'No long-term UPS', 'Gullibility'],
    'Asset Value': [5, 5, 5, 5, 3.8, 3.8, 2.8, 3.8],
    'Likelihood': [8, 8, 6, 6, 7, 7, 9, 9],
    'Severity': [9, 8, 9, 8, 10, 10, 9, 9],
    'Risk Score': [360, 320, 270, 240, 266, 266, 226, 307]
}
df_tva = pd.DataFrame(tva_data)

# 4. Risk Assessment (Quantitative - Lab 13)
risk_calc_data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8],
    'Asset': ['Elec. Data', 'Elec. Data', 'Elec. Data', 'Elec. Data', 'RMS Soft', 'RMS Soft', 'Hardware', 'Staff / Data'],
    'Threat': ['Human Error', 'Human Error', 'SQL Injection', 'Data Breach', 'XSS Attack', 'XSS Attack', 'Power Loss', 'Social Engineering'],
    'Asset Value': [1000000, 1000000, 1000000, 1000000, 250000, 250000, 50000, 1000000],
    'RISK ($)': [33000, 33000, 110000, 110000, 13750, 13750, 28600, 114400]
}
df_risk_calc = pd.DataFrame(risk_calc_data)

# 5. Cost Benefit Analysis (CBA)
cba_data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8],
    'Asset': ['Elec. Data', 'Elec. Data', 'Elec. Data', 'Elec. Data', 'RMS Soft', 'RMS Soft', 'Hardware', 'Staff / Data'],
    'Threat': ['Human Error', 'Human Error', 'SQL Injection', 'Data Breach', 'XSS Attack', 'XSS Attack', 'Power Loss', 'Social Engineering'],
    'Proposed Control': ['Input Validation', '4-Eyes Approval', 'WAF & Code Audit', 'WAF & Code Audit', 
                         'Input Sanitization', 'Input Sanitization', 'UPS & Generator', 'Training & MFA'],
    'RISK Prior ($)': [33000, 33000, 110000, 110000, 13750, 13750, 28600, 114400],
    'New RISK Post ($)': [6600, 6600, 11000, 11000, 2750, 2750, 1430, 22880],
    'ACS (Cost)': [5000, 5000, 25000, 25000, 2000, 2000, 10000, 15000],
    'CBA (Savings)': [21400, 21400, 74000, 74000, 8999, 8999, 17170, 76520]
}
df_cba = pd.DataFrame(cba_data)


# --- DASHBOARD LAYOUT ---

st.sidebar.title("SCA Risk Mgmt")
st.sidebar.info("Lab 13: Risk Assessment & Control")
page = st.sidebar.radio("Navigate:", ["Overview", "1. Identification (TVA)", "2. Assessment (Quant)", "3. Control (CBA)"])

if page == "Overview":
    st.title("Risk Dashboard")
    
    # KPIs
    total_risk = df_risk_calc['RISK ($)'].sum()
    total_save = df_cba['CBA (Savings)'].sum()
    total_cost = df_cba['ACS (Cost)'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Annual Risk Exposure", f"${total_risk:,.0f}", delta_color="inverse")
    col2.metric("Projected Savings (CBA)", f"${total_save:,.0f}", delta="Positive ROI")
    col3.metric("Required Investment", f"${total_cost:,.0f}", delta_color="off")
    
    st.divider()
    st.subheader("High Priority Risks")
    fig = px.bar(df_risk_calc.sort_values(by="RISK ($)"), x="RISK ($)", y="Threat", orientation='h', color="Asset", title="Financial Impact by Threat")
    st.plotly_chart(fig, use_container_width=True)

elif page == "1. Identification (TVA)":
    st.title("Risk Identification (Lab 12)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Asset Valuation")
        st.dataframe(df_assets[['Subcategory', '% of Max']], use_container_width=True)
    with col2:
        st.subheader("Threat Valuation")
        st.dataframe(df_threats, use_container_width=True)
        
    st.subheader("TVA Table (Qualitative Risk Scores)")
    st.dataframe(df_tva.style.background_gradient(subset=['Risk Score'], cmap='Reds'), use_container_width=True)

elif page == "2. Assessment (Quant)":
    st.title("Quantitative Assessment (Lab 13)")
    
    st.dataframe(df_risk_calc.style.format({"Asset Value": "${:,.0f}", "RISK ($)": "${:,.0f}"}), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(df_risk_calc, values='RISK ($)', names='Asset', title="Risk Share by Asset")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(df_risk_calc, x='Threat', y='RISK ($)', color='RISK ($)', title="Monetary Risk per Threat")
        st.plotly_chart(fig2, use_container_width=True)

elif page == "3. Control (CBA)":
    st.title("Risk Control & CBA")
    
    # Before vs After Chart
    df_chart = df_cba[['Threat', 'RISK Prior ($)', 'New RISK Post ($)']].copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_chart['Threat'], y=df_chart['RISK Prior ($)'], name='Risk PRIOR', marker_color='#ff4b4b'))
    fig.add_trace(go.Bar(x=df_chart['Threat'], y=df_chart['New RISK Post ($)'], name='Risk POST', marker_color='#09ab3b'))
    fig.update_layout(barmode='group', title="Risk Reduction Analysis")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Cost Benefit Analysis Table")
    st.dataframe(df_cba.style.format({"RISK Prior ($)": "${:,.0f}", "New RISK Post ($)": "${:,.0f}", "ACS (Cost)": "${:,.0f}", "CBA (Savings)": "${:,.0f}"}), use_container_width=True)