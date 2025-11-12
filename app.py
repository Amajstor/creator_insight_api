from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment variable
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

@app.route('/')
def home():
    """Home page with API information"""
    return jsonify({
        "message": "Creator Insight API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "creator_data": "/creator?youtube_id=CHANNEL_ID"
        },
        "documentation": "Visit /creator?youtube_id=UC9gFih9rw0zNCK3ZtoKQQyA for example usage"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy", 
        "service": "Creator Insight API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/creator', methods=['GET'])
def get_creator_insights():
    """
    Aggregates creator data from YouTube.
    Query parameters:
    - youtube_id (string, required): The YouTube channel ID.
    """
    # 1. Get parameters from the incoming API request
    youtube_id = request.args.get('youtube_id')

    if not youtube_id:
        return jsonify({"error": "Missing required parameter 'youtube_id'"}), 400

    aggregated_data = {
        "requested_youtube_id": youtube_id,
        "youtube_data": {},
        "summary": {},
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

    # 2. Check if we have an API key
    if not YOUTUBE_API_KEY:
        aggregated_data["youtube_data"] = {"error": "YouTube API key not configured"}
        aggregated_data["status"] = "partial"
        return jsonify(aggregated_data)

    # 3. FETCH DATA FROM YOUTUBE API
    try:
        youtube_url = "https://www.googleapis.com/youtube/v3/channels"
        youtube_params = {
            'part': 'statistics,snippet',
            'id': youtube_id,
            'key': YOUTUBE_API_KEY
        }
        
        youtube_response = requests.get(youtube_url, params=youtube_params, timeout=10)
        youtube_data = youtube_response.json()

        # 4. Check if we got a successful response
        if youtube_response.status_code != 200:
            aggregated_data["youtube_data"] = {
                "error": f"YouTube API returned error: {youtube_data.get('error', {}).get('message', 'Unknown error')}"
            }
            aggregated_data["status"] = "error"
            return jsonify(aggregated_data)

        # 5. PARSE & TRANSFORM the data
        if youtube_data.get('items'):
            channel_data = youtube_data['items'][0]
            aggregated_data['youtube_data'] = {
                "channel_title": channel_data['snippet']['title'],
                "description": channel_data['snippet']['description'][:200] + "..." if len(channel_data['snippet']['description']) > 200 else channel_data['snippet']['description'],
                "subscriber_count": int(channel_data['statistics'].get('subscriberCount', 0)),
                "video_count": int(channel_data['statistics'].get('videoCount', 0)),
                "view_count": int(channel_data['statistics'].get('viewCount', 0))
            }
            
            # Build a simple summary
            aggregated_data['summary'] = {
                "platforms": ['YouTube'],
                "total_videos": aggregated_data['youtube_data']['video_count'],
                "total_subscribers": aggregated_data['youtube_data']['subscriber_count']
            }
        else:
            aggregated_data["youtube_data"] = {"error": "No channel found with this ID"}
            aggregated_data["status"] = "error"

    except requests.exceptions.Timeout:
        aggregated_data["youtube_data"] = {"error": "YouTube API request timed out"}
        aggregated_data["status"] = "error"
    except requests.exceptions.RequestException as e:
        aggregated_data["youtube_data"] = {"error": f"Failed to fetch data: {str(e)}"}
        aggregated_data["status"] = "error"
    except Exception as e:
        aggregated_data["youtube_data"] = {"error": f"Unexpected error: {str(e)}"}
        aggregated_data["status"] = "error"

    # 6. RETURN A UNIFIED JSON RESPONSE
    return jsonify(aggregated_data)

@app.route('/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    """
    Enhanced endpoint specifically for dashboard with more detailed data
    """
    youtube_id = request.args.get('youtube_id')
    
    if not youtube_id:
        return jsonify({"error": "Missing youtube_id"}), 400
    
    # Get the basic data using existing function
    basic_data = get_creator_insights().get_json()
    
    # Enhance with additional calculated metrics for dashboard
    if basic_data.get('status') == 'success' and basic_data.get('youtube_data'):
        yt_data = basic_data['youtube_data']
        
        # Calculate additional metrics
        subscribers = yt_data.get('subscriber_count', 0)
        views = yt_data.get('view_count', 0)
        videos = yt_data.get('video_count', 1)
        
        enhanced_data = {
            **basic_data,
            "dashboard_metrics": {
                "views_per_subscriber": views / subscribers if subscribers > 0 else 0,
                "views_per_video": views / videos if videos > 0 else 0,
                "engagement_score": min(100, (subscribers / max(1, views)) * 100000),
                "content_frequency_score": min(100, videos / 100)
            }
        }
        
        return jsonify(enhanced_data)
    
    return jsonify(basic_data)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found", "available_endpoints": ["/", "/health", "/creator"]}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)