# Deploying the Anki API

This guide explains how to deploy your Anki API to a server so it can be accessed by your Custom GPT or other applications.

## Option 1: Deploy to a VPS (Virtual Private Server)

### Prerequisites
- A VPS with Ubuntu/Debian (e.g., DigitalOcean Droplet, Linode, AWS EC2)
- SSH access to your server
- Domain name (optional but recommended)

### Step 1: Set Up Your Server

1. SSH into your server:
   ```
   ssh username@your-server-ip
   ```

2. Update the system:
   ```
   sudo apt update && sudo apt upgrade -y
   ```

3. Install Python and pip:
   ```
   sudo apt install python3 python3-pip python3-venv -y
   ```

4. Install Nginx (for reverse proxy):
   ```
   sudo apt install nginx -y
   ```

### Step 2: Set Up Your Application

1. Create a directory for your application:
   ```
   mkdir -p ~/anki-api
   cd ~/anki-api
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Upload your application files or clone from a repository:
   ```
   # If using git:
   git clone https://your-repository-url.git .
   
   # Or upload files using SCP:
   # (Run this on your local machine)
   # scp -r /path/to/your/local/files username@your-server-ip:~/anki-api/
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file with your Anki cookie:
   ```
   echo 'ANKI_COOKIE="has_auth=1; ankiweb=your_actual_cookie_value_here"' > .env
   echo 'PORT=8000' >> .env
   ```

### Step 3: Set Up Systemd Service

1. Create a systemd service file:
   ```
   sudo nano /etc/systemd/system/anki-api.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Anki API
   After=network.target
   
   [Service]
   User=your-username
   WorkingDirectory=/home/your-username/anki-api
   ExecStart=/home/your-username/anki-api/venv/bin/python anki_fastapi.py
   Restart=always
   RestartSec=10
   Environment=PATH=/home/your-username/anki-api/venv/bin:/usr/bin:/bin
   
   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```
   sudo systemctl enable anki-api
   sudo systemctl start anki-api
   ```

4. Check the status:
   ```
   sudo systemctl status anki-api
   ```

### Step 4: Configure Nginx as a Reverse Proxy

1. Create an Nginx configuration file:
   ```
   sudo nano /etc/nginx/sites-available/anki-api
   ```

2. Add the following content:
   ```
   server {
       listen 80;
       server_name your-domain.com;  # Or your server IP if no domain
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. Enable the site:
   ```
   sudo ln -s /etc/nginx/sites-available/anki-api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

4. (Optional) Set up SSL with Let's Encrypt:
   ```
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com
   ```

## Option 2: Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Prepare Your Application

1. Create a `Procfile` in your project directory:
   ```
   echo "web: uvicorn anki_fastapi:app --host=0.0.0.0 --port=\$PORT" > Procfile
   ```

2. Create a `runtime.txt` file:
   ```
   echo "python-3.9.16" > runtime.txt
   ```

### Step 2: Deploy to Heroku

1. Login to Heroku:
   ```
   heroku login
   ```

2. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

3. Set environment variables:
   ```
   heroku config:set ANKI_COOKIE="has_auth=1; ankiweb=your_actual_cookie_value_here"
   ```

4. Deploy your application:
   ```
   git add .
   git commit -m "Ready for deployment"
   git push heroku main
   ```

5. Open your application:
   ```
   heroku open
   ```

## Option 3: Deploy to Railway

Railway is a modern platform that makes deployment simple.

1. Sign up for Railway: https://railway.app/
2. Connect your GitHub repository
3. Create a new project from your repository
4. Add environment variables in the Railway dashboard
5. Railway will automatically deploy your application

## Keeping Your Anki Cookie Updated

The Anki cookie will expire periodically. To keep your API working:

1. Log in to AnkiWeb in your browser
2. Use browser developer tools to copy the new cookie value
3. Update the cookie in your server's `.env` file or environment variables
4. Restart your application:
   ```
   sudo systemctl restart anki-api  # For systemd
   # or
   heroku config:set ANKI_COOKIE="new_cookie_value_here"  # For Heroku
   ```

## Security Considerations

- Add authentication to your API for production use
- Use HTTPS to encrypt traffic
- Keep your server and dependencies updated
- Consider adding rate limiting to prevent abuse 