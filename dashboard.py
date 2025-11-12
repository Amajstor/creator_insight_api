import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from config import API_BASE_URL
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Creator Insight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CreatorDashboard:
    def __init__(self):
        self.api_base_url = st.session_state.get('api_url', API_BASE_URL)
    
    def check_api_health(self):
        """Check if the API is running and healthy"""
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def fetch_creator_data(self, youtube_id):
        """Fetch data from the Creator Insight API"""
        try:
            url = f"{self.api_base_url}/creator"
            params = {'youtube_id': youtube_id}
            
            with st.spinner('🔄 Fetching creator data...'):
                response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
            return None
    
    def display_metrics(self, data):
        """Display key metrics in a nice layout"""
        if data.get('status') != 'success' or not data.get('youtube_data'):
            st.error("No valid data to display")
            return None
        
        yt_data = data['youtube_data']
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            subscribers = yt_data.get('subscriber_count', 0)
            st.metric(
                label="👥 Subscribers",
                value=f"{subscribers:,}",
                help="Total channel subscribers"
            )
        
        with col2:
            videos = yt_data.get('video_count', 0)
            st.metric(
                label="🎬 Videos",
                value=f"{videos:,}",
                help="Total videos uploaded"
            )
        
        with col3:
            views = yt_data.get('view_count', 0)
            st.metric(
                label="👀 Total Views",
                value=f"{views:,}",
                help="Total channel views"
            )
        
        with col4:
            avg_views = (views / videos) if videos > 0 else 0
            st.metric(
                label="📈 Avg Views/Video",
                value=f"{avg_views:,.0f}",
                help="Average views per video"
            )
        
        return {
            'subscribers': subscribers,
            'videos': videos,
            'views': views,
            'avg_views': avg_views
        }
    
    def create_engagement_chart(self, metrics):
        """Create simple engagement metrics chart with dark theme"""
        if not metrics:
            st.error("No metrics data available for chart")
            return
        
        # Extract values
        subscribers = metrics.get('subscribers', 0)
        videos = metrics.get('videos', 0)
        views = metrics.get('views', 0)
        
        # Create simple bar chart using plotly.graph_objects with dark theme
        fig = go.Figure()
        
        # Add bars for each metric
        fig.add_trace(go.Bar(
            x=['Subscribers', 'Videos', 'Views'],
            y=[subscribers, videos, views],
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'],
            text=[f"{subscribers:,}", f"{videos:,}", f"{views:,}"],
            textposition='outside',
            textfont=dict(color='white')
        ))
        
        # Update layout with dark theme
        fig.update_layout(
            title='📊 Channel Engagement Metrics',
            showlegend=False,
            height=400,
            xaxis_title="",
            yaxis_title="Count",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                tickfont=dict(color='white'),
                gridcolor='rgba(128,128,128,0.3)'
            ),
            yaxis=dict(
                tickfont=dict(color='white'),
                gridcolor='rgba(128,128,128,0.3)'
            ),
            title_font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_subscriber_ratio_chart(self, metrics):
        """Create simple ratio chart with dark theme"""
        if not metrics:
            st.error("No metrics data available for ratio chart")
            return
        
        subscribers = metrics.get('subscribers', 1)
        views = metrics.get('views', 0)
        videos = metrics.get('videos', 1)
        
        # Calculate ratios
        views_per_subscriber = views / subscribers if subscribers > 0 else 0
        views_per_video = views / videos if videos > 0 else 0
        
        # Create simple bar chart with dark theme
        fig = go.Figure()
        
        # Add bars for ratios
        fig.add_trace(go.Bar(
            x=['Views per Subscriber', 'Views per Video'],
            y=[views_per_subscriber, views_per_video],
            marker_color=['#9467bd', '#8c564b'],
            text=[f"{views_per_subscriber:,.1f}", f"{views_per_video:,.1f}"],
            textposition='outside',
            textfont=dict(color='white')
        ))
        
        # Update layout with dark theme
        fig.update_layout(
            title='📈 Engagement Ratios',
            showlegend=False,
            height=400,
            xaxis_title="",
            yaxis_title="Ratio Value",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                tickfont=dict(color='white'),
                gridcolor='rgba(128,128,128,0.3)'
            ),
            yaxis=dict(
                tickfont=dict(color='white'),
                gridcolor='rgba(128,128,128,0.3)'
            ),
            title_font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_channel_info(self, data):
        """Display channel information"""
        if data.get('status') != 'success' or not data.get('youtube_data'):
            return
        
        yt_data = data['youtube_data']
        
        st.markdown("### 📺 Channel Information")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Channel Title:** `{yt_data.get('channel_title', 'N/A')}`")
            description = yt_data.get('description', 'N/A')
            if len(description) > 200:
                description = description[:200] + "..."
            st.markdown(f"**Description:** {description}")
        
        with col2:
            st.markdown(f"**Status:** 🟢 **{data.get('status', 'unknown').upper()}**")
            st.markdown(f"**Platforms:** {', '.join(data.get('summary', {}).get('platforms', ['YouTube']))}")

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Creator Insight Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize dashboard
    dashboard = CreatorDashboard()
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        api_url = st.text_input(
            "API Base URL",
            value="http://localhost:5000",
            help="URL where your Creator Insight API is running"
        )
        st.session_state.api_url = api_url
        dashboard.api_base_url = api_url
        
        # API health check
        st.markdown("---")
        st.markdown("### 🔧 API Status")
        if dashboard.check_api_health():
            st.success("✅ API is running")
        else:
            st.error("❌ API is not running")
            st.markdown("""
            **To fix this:**
            1. Open a new Command Prompt
            2. Navigate to your project folder
            3. Run: `venv\\Scripts\\activate`
            4. Run: `python app.py`
            5. Keep that window open!
            """)
        
        st.markdown("---")
        st.markdown("### 📝 How to Use")
        st.markdown("""
        1. **Start the API** (see instructions above)
        2. Click 'Analyze Creator' to fetch data
        3. View insights and metrics in the main panel
        
        The dashboard will automatically analyze the **Jenna Marbles** channel.
        """)
    
    # Show warning if API isn't running
    if not dashboard.check_api_health():
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ API Not Running</h3>
        <p>Your Flask API needs to be started before you can use the dashboard.</p>
        <p><strong>Quick fix:</strong> Open a new Command Prompt and run:</p>
        <code>venv\\Scripts\\activate && python app.py</code>
        <p>Then keep that window open and return here.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Main content area - only shown when API is running
    st.markdown("### 🔍 Analyze Creator")
    
    # Create a row for input and button - AUTO-FILL with the specified channel ID
    input_col, button_col = st.columns([3, 1])
    
    with input_col:
        youtube_id = st.text_input(
            "YouTube Channel ID",
            value="UC9gFih9rw0zNCK3ZtoKQQyA",  # Auto-filled with Jenna Marbles channel
            placeholder="Enter YouTube Channel ID",
            help="YouTube Channel ID to analyze",
            label_visibility="collapsed"
        )
    
    with button_col:
        analyze_clicked = st.button(
            "🎯 Analyze Creator",
            type="primary",
            use_container_width=True
        )
    
    # Auto-analyze when the page loads
    if dashboard.check_api_health() and youtube_id == "UC9gFih9rw0zNCK3ZtoKQQyA" and not st.session_state.get('auto_analyzed', False):
        st.session_state.auto_analyzed = True
        analyze_clicked = True
    
    # Fetch and display data when analyze is clicked
    if analyze_clicked and youtube_id:
        data = dashboard.fetch_creator_data(youtube_id)
        
        if data:
            if data.get('status') == 'success':
                st.markdown('<div class="success-box">✅ Successfully fetched creator data!</div>', unsafe_allow_html=True)
                
                # Display metrics and get the metrics dictionary
                metrics = dashboard.display_metrics(data)
                
                if metrics:
                    # Create charts in columns using the metrics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        dashboard.create_engagement_chart(metrics)
                    
                    with col2:
                        dashboard.create_subscriber_ratio_chart(metrics)
                
                # Channel information
                dashboard.display_channel_info(data)
                    
            else:
                error_msg = data.get('youtube_data', {}).get('error', 'Unknown error')
                st.markdown(f'<div class="error-box">❌ Error: {error_msg}</div>', unsafe_allow_html=True)
    
    elif analyze_clicked and not youtube_id:
        st.warning("⚠️ Please enter a YouTube Channel ID")
    
    # Show instructions when no data is loaded but API is running
    elif not analyze_clicked and dashboard.check_api_health():
        st.markdown("---")
        st.markdown("### 👆 Get Started")
        st.markdown("""
        Click **Analyze Creator** to see insights for the **Jenna Marbles** channel, or enter a different Channel ID above.
        
        You'll see:
        - 📊 **Channel metrics** (subscribers, videos, views)
        - 📈 **Engagement charts** with colored bars
        - 📺 **Channel information** and description
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit & Flask | Creator Insight API Dashboard"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()