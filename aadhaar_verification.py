import
import json
import base64
import hashlib
import hmac
import time
import urllib.parse

# Set up API endpoint and headers
api_endpoint = "https://api.uidai.gov.in/aadhaarapi/v2/"
headers = {
    "Content-Type": "application/json",
    "Date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
    "Digest": "SHA-256=",
    "Accept": "application/json",
}

# Set up API credentials
uidai_client_id = "YOUR_CLIENT_ID"
uidai_client_secret = "YOUR_CLIENT_SECRET"
uidai_api_key = "YOUR_API_KEY"

# Set up Aadhaar number and mobile number
aadhaar_number = "123456789012"

# Set up API request payload
request_payload = {
    "req": {
        "regId": aadhaar_number,
        "txnType": "AUTHENTICATE",
        "biometric": {
            "encryptedBiometric": "BASE64_ENCODED_ENCRYPTED_BIOMETRIC_DATA"
        },
        "channel": "WEB",
        "deviceFingerPrint": "DEVICE_FINGERPRINT",
        "msg": "Authentication Request",
        "udid": "UDID"
    }
}

# Calculate the digest for the API request
string_to_sign = (headers["Date"] + "\n" + api_endpoint).encode("utf-8")
signature = base64.b64encode(hmac.new(uidai_client_secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()).decode("utf-8")
headers["Digest"] = f"SHA-256={signature}"

# Send the API request
response = requests.post(api_endpoint, headers=headers, data=json.dumps(request_payload))

# Check the API response status code
if response.status_code == 200:
    # Parse the API response
    response_payload = json.loads(response.content)

    # Get the Aadhaar holder's mobile number
    mobile_number = response_payload["res"]["mobile"]
    print(f"Aadhaar holder's mobile number: {mobile_number}")
else:
    print(f"API request failed with status code {response.status_code}")