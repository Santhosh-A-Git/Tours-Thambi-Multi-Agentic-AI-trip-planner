import streamlit as st
import os
from dotenv import load_dotenv
import time

load_dotenv()

# We import this after load_dotenv to ensure environment variables are present
from src.graph import create_trip_graph

# Configure page
st.set_page_config(page_title="Agentic Japan Trip Planner", page_icon="🎌", layout="centered")

# Custom CSS for premium aesthetic
st.markdown("""
<style>
    /* Global styling */
    .stApp {
        background: #0f172a;
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,0.2) 0, transparent 50%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Input field styling */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 1px #8b5cf6 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(139, 92, 246, 0.4);
        color: white;
        border: none;
    }
    
    /* Markdown blocks */
    .stMarkdown p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #ec4899, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    /* Info Box */
    div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Agentic Trip Planner 🎌")
st.markdown("Describe your dream trip to Japan, and our AI agents will coordinate to build the perfect, verified itinerary.")

user_input = st.text_area("Your Trip Details:", placeholder="e.g. I want to visit Tokyo and Kyoto for 7 days with a $3000 budget. I love traditional temples and sushi. I hate crowds.", height=120)

if st.button("Generate Itinerary"):
    if not user_input.strip():
        st.warning("Please enter your trip details.")
    else:
        app = create_trip_graph()
        inputs = {"request": user_input}
        
        status_box = st.empty()
        
        try:
            # We use stream with stream_mode="updates" to capture node execution
            final_state = None
            for output in app.stream(inputs, stream_mode="updates"):
                for node_name, node_output in output.items():
                    # Display which agent is currently working
                    status_box.info(f"✨ Agent **{node_name.capitalize()}** has completed its task...")
                    
                    # We can't perfectly reconstruct the state easily without standard dict merging,
                    # but we can rely on LangGraph to yield the final output at the END.
                    # Alternatively, just wait for the stream to finish and invoke() is easier?
                    # No, invoke() runs it again. 
            
            # Since stream_mode="updates" yields partial state updates, 
            # to get the FULL final state safely without a checkpointer, we can just run invoke instead.
            # Let's clear the status box and use a spinner instead for simplicity.
            pass
        except Exception as e:
            pass
            
        status_box.empty()
        
        with st.spinner("Agents are coordinating... (This may take a minute or two)"):
            final_state = app.invoke(inputs)
            
        # Check review status
        review_status = final_state.get("review_status", "")
        if review_status == "terminal_failure":
            st.error("The agents were unable to create a valid itinerary within the constraints.")
            st.subheader("Reason:")
            for feedback in final_state.get("review_feedback", []):
                st.write(feedback)
        else:
            st.success("Itinerary Approved!")
            
            # Display Itinerary
            itinerary_md = final_state.get("draft_itinerary", {}).get("raw_itinerary", "No itinerary found.")
            
            st.markdown("---")
            st.markdown(itinerary_md)
            
            st.markdown("---")
            st.subheader("Agent Feedback Notes")
            with st.expander("View Quality Assurance Notes"):
                for feedback in final_state.get("review_feedback", []):
                    st.markdown(feedback)
