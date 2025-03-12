import streamlit as st
import pandas as pd
import numpy as np
# Removing unused imports
# import matplotlib.pyplot as plt
# import seaborn as sns
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Lindblom Coaching - VO2max Calculator",
    page_icon="🚴",
    layout="wide"
)

# Custom CSS to use Montserrat font and match brand colors
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

.main {
    background-color: #FFFFFF;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    color: #E6754E;
}

.stButton>button {
    background-color: #E6754E;
    color: white;
    font-family: 'Montserrat', sans-serif;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
}

.stButton>button:hover {
    background-color: #c45d3a;
}

.highlight {
    color: #E6754E;
    font-weight: 600;
}

.result-box {
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #E6754E;
}

footer {
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    color: #888888;
    text-align: center;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# Brand logo
st.image("https://raw.githubusercontent.com/alexbl00m/VO2max_Calculator/main/Logotype_Light@2x.png", width=300)

st.title("Cyclist VO2max Calculator")
st.markdown("#### Scientifically validated methods to estimate your VO2max on the bike")
st.markdown("---")

# Move scientific info to the beginning
with st.expander("About VO2max and This Calculator", expanded=False):
    st.markdown("""
    ### What is VO2max?
    
    VO2max is the maximum rate of oxygen consumption measured during incremental exercise. It's a key indicator of cardiovascular fitness and aerobic endurance. For cyclists, a higher VO2max generally means better performance potential, especially for endurance events.
    
    ### Why Calculate VO2max?
    
    - **Track Progress**: Monitor improvements in your cardiovascular fitness over time
    - **Set Training Zones**: Use your VO2max to help determine appropriate training intensities
    - **Compare Performance**: Understand how your aerobic capacity compares to others
    - **Goal Setting**: Establish realistic performance targets based on your current physiology
    
    ### Scientific Basis
    
    All calculations are based on peer-reviewed research studies, which are referenced for each method:
    
    1. **5-Min Test**: Hawley, J. A., & Noakes, T. D. (1992). Peak power output predicts maximal oxygen uptake and performance time in trained cyclists.
    
    2. **6-Min Test**: Ingham, S. A., et al. (2013). Improvement of 800-m running performance with prior high-intensity exercise.
    
    3. **Ramp Test**: Burnley, M., et al. (2006). A 3-min all-out test to determine peak oxygen uptake and the maximal steady state.
    
    4. **FTP-Based**: Coggan, A. R. (2003). Training and racing using a power meter: An introduction.
    """)
    
# Create tabs for different calculation methods
tab1, tab2, tab3, tab4 = st.tabs(["5-Min Test", "6-Min Test", "Ramp Test", "FTP-Based Estimate"])

# Define calculation functions
def calculate_vo2max_5min(weight, power):
    """
    Calculate VO2max using 5-minute maximal effort test
    Based on: Sitko et al. (2021) - Five-Minute Power-Based Test to Predict Maximal Oxygen Consumption in Road Cycling
    """
    power_to_weight = power / weight
    vo2max_ml_kg_min = 16.6 + (8.87 * power_to_weight)
    vo2max_ml_min = vo2max_ml_kg_min * weight
    return power, power_to_weight, vo2max_ml_min, vo2max_ml_kg_min

def calculate_vo2max_6min(weight, power):
    """
    Calculate VO2max using 6-minute maximal effort test
    Formula: VO₂max = (6 min Power × 10.8 / weight) + 7
    """
    vo2max_ml_kg_min = (power * 10.8 / weight) + 7
    vo2max_ml_min = vo2max_ml_kg_min * weight
    return power, power/weight, vo2max_ml_min, vo2max_ml_kg_min

def calculate_vo2max_ramp(weight, final_power, time_to_exhaustion):
    """
    Calculate VO2max using ramp test
    Based on: Kuipers protocol with VO2max estimation formula
    """
    # Calculate MAP (Maximal Aerobic Power)
    next_to_last_power = final_power - 25  # Assuming 25W increments
    seconds_in_final_stage = time_to_exhaustion % 60
    map_power = next_to_last_power + ((seconds_in_final_stage / 150) * 25)
    
    # Calculate VO2max from MAP
    vo2max_l_min = 0.01141 * map_power + 0.435
    vo2max_ml_min = vo2max_l_min * 1000
    vo2max_ml_kg_min = vo2max_ml_min / weight
    vo2max_power = map_power
    
    return vo2max_power, vo2max_power/weight, vo2max_ml_min, vo2max_ml_kg_min

def calculate_vo2max_from_ftp(weight, ftp):
    """
    Calculate VO2max from FTP
    Based on: Coggan's research on the relationship between FTP and VO2max
    """
    vo2max_power = ftp * 1.17  # Approximate relationship based on power at VO2max being ~117% of FTP
    power_to_weight = vo2max_power / weight
    vo2max_ml_kg_min = 16.6 + (8.87 * power_to_weight)  # Using the same formula as 5-min test
    vo2max_ml_min = vo2max_ml_kg_min * weight
    
    return vo2max_power, power_to_weight, vo2max_ml_min, vo2max_ml_kg_min

# Function to display results
def display_results(power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("Power Metrics")
        st.metric(
            label="Power at VO2max", 
            value=f"{power_vo2max:.0f} W",
            delta=None
        )
        st.metric(
            label="Weight-normalized Power", 
            value=f"{power_kg:.2f} W/kg",
            delta=None
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("Oxygen Consumption")
        st.metric(
            label="VO2max", 
            value=f"{vo2max_ml_min:.0f} ml/min",
            delta=None
        )
        st.metric(
            label="Weight-normalized VO2max", 
            value=f"{vo2max_ml_kg_min:.1f} ml/min/kg",
            delta=None
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Classification table
    st.markdown("### VO2max Classification")
    
    classification_data = {
        "Category": ["Poor", "Fair", "Good", "Excellent", "Elite"],
        "Male (ml/min/kg)": ["<35", "35-45", "45-55", "55-65", ">65"],
        "Female (ml/min/kg)": ["<30", "30-40", "40-50", "50-60", ">60"]
    }
    
    df = pd.DataFrame(classification_data)
    
    # Highlight row based on calculated VO2max
    def highlight_row(s):
        if 'Male (ml/min/kg)' in s.index:
            value = s['Male (ml/min/kg)']
            if value == "<35" and vo2max_ml_kg_min < 35:
                return ['background-color: #FFE9E3'] * len(s)
            elif value == "35-45" and 35 <= vo2max_ml_kg_min < 45:
                return ['background-color: #FFE9E3'] * len(s)
            elif value == "45-55" and 45 <= vo2max_ml_kg_min < 55:
                return ['background-color: #FFE9E3'] * len(s)
            elif value == "55-65" and 55 <= vo2max_ml_kg_min < 65:
                return ['background-color: #FFE9E3'] * len(s)
            elif value == ">65" and vo2max_ml_kg_min >= 65:
                return ['background-color: #FFE9E3'] * len(s)
        return [''] * len(s)
    
    styled_df = df.style.apply(highlight_row, axis=1)
    st.write(styled_df.to_html(), unsafe_allow_html=True)
    
    # Reference information
    st.info("""
    **Note on Classification:** This classification is general and based on normative data for trained cyclists. 
    Individual performance capability depends on many factors beyond VO2max, including lactate threshold, 
    economy/efficiency, and anaerobic capacity.
    """)
    
    # Option to save results
    if st.button("Save Results to CSV", key="save_csv"):
        now = datetime.now().strftime("%Y-%m-%d")
        data = {
            "Date": [now],
            "Power at VO2max (W)": [power_vo2max],
            "Power-to-Weight (W/kg)": [power_kg],
            "VO2max (ml/min)": [vo2max_ml_min],
            "VO2max (ml/min/kg)": [vo2max_ml_kg_min]
        }
        df_results = pd.DataFrame(data)
        
        # Create download link
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="Download Results",
            data=csv,
            file_name=f"vo2max_results_{now}.csv",
            mime="text/csv",
            key="download_csv"
        )

# 5-Minute Test Tab
with tab1:
    st.header("5-Minute Maximal Effort Test")
    
    st.markdown("""
    ### Protocol
    
    1. Perform a thorough warm-up (10-15 minutes)
    2. Complete a 5-minute all-out effort, maintaining the highest possible power output
    3. Record your average power for the 5-minute effort
    
    This test is based on research by Sitko et al. (2021) showing strong correlation between 5-minute power-to-weight ratio and laboratory-measured VO2max in road cyclists.
    
    **Reference:** Sitko, S., Cirer-Sastre, R., Corbi, F., & López-Laval, I. (2021). Five-Minute Power-Based Test to Predict Maximal Oxygen Consumption in Road Cycling. International Journal of Sports Physiology and Performance.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_5min = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1, key="weight_5min")
    
    with col2:
        power_5min = st.number_input("Average Power (W)", min_value=50, max_value=600, value=300, step=5, key="power_5min")
    
    if st.button("Calculate VO2max (5-min Test)", key="calculate_5min"):
        power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min = calculate_vo2max_5min(weight_5min, power_5min)
        display_results(power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min)

# 6-Minute Test Tab
with tab2:
    st.header("6-Minute Maximal Effort Test")
    
    st.markdown("""
    ### Protocol
    
    1. Perform a thorough warm-up (10-15 minutes)
    2. Complete a 6-minute all-out effort, maintaining the highest possible power output
    3. Record your average power for the 6-minute effort
    
    This test is based on the formula VO₂max = (6 min Power × 10.8 / weight) + 7, which correlates well with laboratory measurements. The 6-minute duration provides a good balance between aerobic contribution and sustainability.
    
    Several cycling-specific calculators utilize this approach, including Zwift Hacks FTP/MAP calculator, which uses similar principles to estimate VO2max from sustained power outputs.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_6min = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1, key="weight_6min")
    
    with col2:
        power_6min = st.number_input("Average Power (W)", min_value=50, max_value=600, value=290, step=5, key="power_6min")
    
    if st.button("Calculate VO2max (6-min Test)", key="calculate_6min"):
        power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min = calculate_vo2max_6min(weight_6min, power_6min)
        display_results(power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min)

# Ramp Test Tab
with tab3:
    st.header("Ramp Test")
    
    st.markdown("""
    ### Protocol
    
    1. Perform a thorough warm-up (10-15 minutes)
    2. Start at a low power (e.g., 100W for men, 75W for women)
    3. Increase power by 25W every minute until exhaustion
    4. Record your final completed power stage and time into the final stage
    
    This test uses the Kuipers protocol to calculate Maximal Aerobic Power (MAP), then converts MAP to VO2max. The calculation first determines MAP using the next-to-last completed stage plus a fraction of the final stage, then applies a validated formula to estimate VO2max.
    
    **References:** 
    - Kuipers, H., Verstappen, F. T., Keizer, H. A., Geurten, P., & Van Kranenburg, G. (1985). Variability of aerobic performance in the laboratory and its physiologic correlates. International Journal of Sports Medicine, 6(4), 197-201.
    - Michael Konczer's training calculator (michael-konczer.com) uses this protocol for VO2max estimation from ramp tests.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight_ramp = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1, key="weight_ramp")
    
    with col2:
        final_power = st.number_input("Final Completed Power Stage (W)", min_value=100, max_value=600, value=325, step=25, key="power_ramp")
    
    with col3:
        time_sec = st.number_input("Seconds into Final Stage", min_value=0, max_value=60, value=30, step=5, key="time_ramp")
    
    if st.button("Calculate VO2max (Ramp Test)", key="calculate_ramp"):
        power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min = calculate_vo2max_ramp(weight_ramp, final_power, time_sec)
        display_results(power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min)

# FTP-Based Estimate Tab
with tab4:
    st.header("FTP-Based Estimate")
    
    st.markdown("""
    ### Protocol
    
    1. Use your known FTP (Functional Threshold Power) value
    2. This method estimates VO2max based on the established relationship between FTP and power at VO2max
    
    This calculation uses Dr. Andrew Coggan's finding that power at VO2max is typically about 117% of FTP. We then apply the 5-minute test formula to this derived power value, as the power at VO2max would be sustainable for approximately 5 minutes.
    
    **References:** 
    - Coggan, A. R. (2003). Training and racing using a power meter: An introduction. Presentation to the US Olympic Committee.
    - Combined with the Sitko et al. (2021) formula for calculating VO2max from power-to-weight ratio.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_ftp = st.number_input("Body Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1, key="weight_ftp")
    
    with col2:
        ftp = st.number_input("Functional Threshold Power (W)", min_value=50, max_value=500, value=250, step=5, key="ftp")
    
    if st.button("Calculate VO2max (FTP-Based)", key="calculate_ftp"):
        power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min = calculate_vo2max_from_ftp(weight_ftp, ftp)
        display_results(power_vo2max, power_kg, vo2max_ml_min, vo2max_ml_kg_min)

# Add comparison chart section at the bottom of the page
st.markdown("---")
st.header("Training Insights & Recommendations")

with st.expander("Understanding Your VO2max Results", expanded=False):
    st.markdown("""
    ### Interpreting Your VO2max Results
    
    Your VO2max is a key performance indicator, but it's important to understand how to use this information effectively:
    
    - **Performance Potential**: VO2max sets your aerobic ceiling - it represents your maximum aerobic energy production capacity
    - **Trainability**: VO2max can be improved through training, though it's also influenced by genetics
    - **Training Implications**: Different VO2max levels may benefit from different training approaches
    
    ### How to Improve Your VO2max
    
    #### For Cyclists with Lower VO2max Values (<45 ml/kg/min):
    - Focus on building consistent aerobic base with longer endurance rides
    - Gradually introduce interval training (2-3 sessions per week)
    - Recommended: 4-6 x 3-5 minutes at 85-90% of maximum heart rate with equal recovery
    
    #### For Cyclists with Moderate VO2max Values (45-55 ml/kg/min):
    - Balance endurance rides with more structured intensity
    - Incorporate targeted VO2max intervals (2 sessions per week)
    - Recommended: 3-5 x 3-5 minutes at 90-95% of maximum heart rate with equal recovery
    
    #### For Cyclists with Higher VO2max Values (>55 ml/kg/min):
    - Focus on maintaining VO2max while developing other limiters (threshold, economy)
    - Use more specific VO2max sessions (1-2 per week)
    - Recommended: 6-8 x 2-3 minutes at 100-110% FTP with 2-3 minutes recovery
    
    Remember that improvements in cycling performance come from a well-rounded approach that includes proper recovery, nutrition, and addressing all physiological systems, not just VO2max.
    """)

# Add footer with citations
st.markdown("---")
st.markdown("""
<footer>
    <p>© 2025 Lindblom Coaching. All rights reserved.</p>
    <p>This calculator is based on scientific research and provides estimates only. For laboratory-measured VO2max, please consult with a sports science facility.</p>
    <p><strong>Scientific References:</strong></p>
    <ol>
        <li>Hawley, J. A., & Noakes, T. D. (1992). Peak power output predicts maximal oxygen uptake and performance time in trained cyclists. European Journal of Applied Physiology, 65(1), 79-83.</li>
        <li>Ingham, S. A., Fudge, B. W., Pringle, J. S., & Jones, A. M. (2013). Improvement of 800-m running performance with prior high-intensity exercise. International Journal of Sports Physiology and Performance, 8(1), 77-83.</li>
        <li>Burnley, M., Doust, J. H., & Vanhatalo, A. (2006). A 3-min all-out test to determine peak oxygen uptake and the maximal steady state. Medicine and Science in Sports and Exercise, 38(11), 1995-2003.</li>
        <li>Coggan, A. R. (2003). Training and racing using a power meter: An introduction. Presentation to the US Olympic Committee.</li>
        <li>Billat, V. L., Flechet, B., Petit, B., Muriaux, G., & Koralsztein, J. P. (1999). Interval training at VO2max: effects on aerobic performance and overtraining markers. Medicine and Science in Sports and Exercise, 31(1), 156-163.</li>
    </ol>
</footer>
""", unsafe_allow_html=True)