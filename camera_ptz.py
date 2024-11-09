import requests
from requests.auth import HTTPDigestAuth
from util import camera_ip


# URL for the pan control with relative movement
url = f"http://{camera_ip()}/axis-cgi/com/ptz.cgi"

def turn_camera(degree,direction):
    # Parameters for a 40-degree relative pan movement to the right

    if(direction=='tilt'):
        params = {
            'rtilt': degree   # Relative tilt position
        }
    if(direction=='zoom'):
        params = {
            'rzoom': degree   # Relative zoom position
        }
    elif(direction=='gohome'):
        params = {
            'pan': '0',   # Absolute pan position
            'tilt': '0',   # Absolute tilt position,
            'zoom': '1'
        }
    else:
        params = {
            'rpan': degree,  # Relative pan
        }
    
    try:
        # Send the request to move the camera
        # auth=HTTPDigestAuth(username, password),
        response = requests.get(url,  params=params) 
        
        # Check for a successful response
        if response.status_code in [200,204]:
            print("Camera moved.")
        else:
            print(f"Failed to move camera. Status code: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"Error communicating with the camera: {e}")

#turn_camera(20,'pan') # pan/tilt/gohome/zoom, 20/-20
#turn_camera(20,'tilt') # Turn,left,right, 20
turn_camera(20,'gohome') # Turn,left,right, 20
#turn_camera(500,'zoom') # Turn,left,right, 20
