# WebSocket Testing

## Problem
App connects to: `ws://84.54.30.211/api/v1/ws/{user_id}?token={token}`
Backend returns: **404 Not Found**

## Test Commands

### 1. Check if WebSocket endpoint exists (using curl)
```powershell
# Test WebSocket upgrade request
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: test" "http://84.54.30.211/api/v1/ws/a5723fbe-36ad-403b-9b05-aa3b1d6aa92f?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhNTcyM2ZiZS0zNmFkLTQwM2ItOWIwNS1hYTNiMWQ2YWE5MmYiLCJyb2xlIjoicmVzY3VlciIsImV4cCI6MTc2MDE1OTM3NCwidHlwZSI6ImFjY2VzcyJ9.9_y_lWHQ8QEoV4WDns-rfidQ-ektYoWOC812UEKWFBo"
```

### 2. Check FastAPI docs
Open in browser:
- http://84.54.30.211/docs
- Check if `/api/v1/ws/{user_id}` is listed

### 3. Check nginx configuration
The problem might be that nginx doesn't proxy WebSocket correctly!

## Possible Solutions

### Solution 1: Fix nginx WebSocket proxy
nginx needs special configuration for WebSocket:

```nginx
location /api/v1/ws/ {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Timeouts for WebSocket
    proxy_read_timeout 86400;
    proxy_send_timeout 86400;
}
```

### Solution 2: Use different WebSocket path
Maybe nginx blocks `/api/v1/ws/` specifically?

Try `/ws/` directly without `/api/v1/` prefix.
