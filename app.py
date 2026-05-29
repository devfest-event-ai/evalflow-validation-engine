import os
import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="EvalFlow Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Title
st.title("EvalFlow - Clinical Validation Dashboard")
st.markdown("AI-powered clinical note extraction and validation")

# Sidebar
st.sidebar.header("Configuration")
# api_url = st.sidebar.text_input("API URL", "http://localhost:8000")
# Cek apakah environment variable API_URL ada, kalau tidak pakai default
api_default_url = os.getenv("API_URL", "http://api:8000")

# Sidebar Input
api_url = st.sidebar.text_input("API URL", api_default_url)

# Main tabs
tab1, tab2, tab3 = st.tabs(["Extraction", "Metrics", "About"])

# TAB 1: Extraction
with tab1:
    st.header("Clinical Note Extraction")
    
    # Input area
    clinical_note = st.text_area(
        "Enter Clinical Note:",
        height=200,
        placeholder="Patient presents with BP 140/90. Prescribed Lisinopril 10mg once daily..."
    )
    
    note_id = st.text_input("Note ID", value=f"NOTE_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        extract_btn = st.button("Extract", type="primary")
    
    # Extraction result
    if extract_btn and clinical_note:
        with st.spinner("Processing..."):
            try:
                payload = {
                    "note_id": note_id,
                    "text": clinical_note,
                    "category": "nursing"
                }
                
                response = requests.post(f"{api_url}/extract", json=payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("Extraction Complete!")
                    
                    # Metrics columns
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Confidence Score", f"{result['confidence_score']:.2f}")
                    col2.metric("Status", result['validation_status'])
                    col3.metric("Medications Found", len(result['medications']))
                    
                    # Detailed results
                    st.subheader("Extracted Data")
                    
                    # Medications
                    if result['medications']:
                        st.write("**Medications:**")
                        meds_df = pd.DataFrame(result['medications'])
                        #st.dataframe(meds_df, use_container_width=True)
                        st.dataframe(meds_df, width="stretch")
                    else:
                        st.info("No medications extracted")
                    
                    # Vital Signs
                    if result['vital_signs']:
                        st.write("**Vital Signs:**")
                        vitals_df = pd.DataFrame([result['vital_signs']])
                        #st.dataframe(vitals_df, use_container_width=True)
                        st.dataframe(vitals_df, width="stretch")
                    # Diagnosis
                    if result['diagnosis']:
                        st.write(f"**Diagnosis:** {result['diagnosis']}")
                    
                    # Fallback Action
                    if result.get('fallback_action'):
                        st.warning(f"**Action:** {result['fallback_action'].get('action')}")
                        st.write(f"Reason: {result['fallback_action'].get('reason')}")
                    
                    # Raw JSON
                    with st.expander("View Raw JSON"):
                        st.json(result)
                        
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure the server is running.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif extract_btn and not clinical_note:
        st.warning("Please enter a clinical note")

# TAB 2: Metrics
with tab2:
    st.header("Performance Metrics")
    
    try:
        with open('metrics_report.json', 'r') as f:
            metrics_data = json.load(f)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Precision", f"{metrics_data['precision']:.3f}")
        col2.metric("Recall", f"{metrics_data['recall']:.3f}")
        col3.metric("F1-Score", f"{metrics_data['f1_score']:.3f}")
        
        st.subheader("Performance Rating")
        st.info(f"**{metrics_data['performance_rating']}**")
        
        # Detailed stats
        st.subheader("Detailed Statistics")
        stats_col1, stats_col2 = st.columns(2)
        stats_col1.write(f"**Total Samples:** {metrics_data['total_samples']}")
        stats_col1.write(f"**Correct Extractions:** {metrics_data['correct_extractions']}")
        stats_col2.write(f"**Missed Extractions:** {metrics_data['missed_extractions']}")
        stats_col2.write(f"**False Extractions:** {metrics_data['false_extractions']}")
        
        # Raw metrics
        with st.expander("View Raw Metrics JSON"):
            st.json(metrics_data)
            
    except FileNotFoundError:
        st.warning("metrics_report.json not found. Run evaluate.py first.")
    except json.JSONDecodeError:
        st.error("Error reading metrics file. File may be corrupted.")

# TAB 3: About
with tab3:
    st.header("About EvalFlow")
    st.markdown("""
    **EvalFlow** is a clinical validation engine that:
    
    - Extracts structured data from unstructured clinical notes
    - Validates extraction using FMR confidence scoring
    - Provides automated decision routing (approve/review/reject)
    
    ### Tech Stack
    - Backend: FastAPI + Pydantic
    - Frontend: Streamlit
    - Validation: Custom FMR Scoring Engine
    
    ### Architecture
    1. **Extraction Layer**: Regex-based pattern matching
    2. **Scoring Engine**: Completeness + Pattern Quality + Consistency
    3. **Decision Layer**: Auto-routing based on confidence score
    """)