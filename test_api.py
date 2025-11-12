import requests
import time

def test_api_connection():
    print("🔍 Testing API connection...")
    
    try:
        # Test basic connection
        response = requests.get("http://localhost:5000/", timeout=5)
        print(f"✅ API Homepage: {response.status_code}")
        
        # Test health endpoint
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        
        # Test creator endpoint with a known channel
        test_channel = "UC9gFih9rw0zNCK3ZtoKQQyA"  # Jenna Marbles
        print(f"🧪 Testing with channel: {test_channel}")
        
        response = requests.get(
            "http://localhost:5000/creator", 
            params={'youtube_id': test_channel},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Creator Endpoint: SUCCESS")
            print(f"   Status: {data.get('status')}")
            if data.get('youtube_data'):
                print(f"   Channel: {data['youtube_data'].get('channel_title', 'N/A')}")
        else:
            print(f"❌ Creator Endpoint: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running?")
        print("   Run: python app.py")
    except requests.exceptions.Timeout:
        print("❌ API connection timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_connection()