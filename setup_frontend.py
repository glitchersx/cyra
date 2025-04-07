import os
import subprocess
import sys
import shutil

def run_command(command):
    """Run a command and print output"""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    # Print output in real-time
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")
    
    # Wait for process to complete
    process.stdout.close()
    return_code = process.wait()
    
    if return_code != 0:
        print(f"Command failed with return code {return_code}")
        stderr = process.stderr.read()
        print(f"Error: {stderr}")
        return False
    
    return True

def check_node_npm():
    """Check if Node.js and npm are installed"""
    try:
        # Use shell=True specifically for Windows
        node_process = subprocess.run("node --version", shell=True, check=False, 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        npm_process = subprocess.run("npm --version", shell=True, check=False,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the commands returned valid versions
        if node_process.returncode == 0 and npm_process.returncode == 0:
            print(f"Found Node.js: {node_process.stdout.strip()}")
            print(f"Found npm: {npm_process.stdout.strip()}")
            return True
        else:
            print("Node.js and npm are required. Please install them first.")
            print("Visit https://nodejs.org/ to download and install Node.js")
            return False
    except Exception as e:
        print(f"Error checking Node.js and npm: {e}")
        print("Node.js and npm are required. Please install them first.")
        print("Visit https://nodejs.org/ to download and install Node.js")
        return False

def create_react_public_files():
    """Create the required public files for React"""
    # Create public directory if it doesn't exist
    public_dir = "public"
    if not os.path.exists(public_dir):
        print(f"Creating {public_dir} directory...")
        os.makedirs(public_dir)
    
    # Create index.html
    with open(os.path.join(public_dir, "index.html"), "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="ElevenLabs Conversation Manager - Web Interface"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <title>ElevenLabs Conversation Manager</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>""")
    
    # Create manifest.json
    with open(os.path.join(public_dir, "manifest.json"), "w") as f:
        f.write("""{
  "short_name": "ElevenLabs Manager",
  "name": "ElevenLabs Conversation Manager",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}""")
    
    # Create robots.txt
    with open(os.path.join(public_dir, "robots.txt"), "w") as f:
        f.write("""# https://www.robotstxt.org/robotstxt.html
User-agent: *
Disallow:""")
    
    # Create placeholder favicon.ico
    with open(os.path.join(public_dir, "favicon.ico"), "w") as f:
        f.write("Placeholder favicon")
    
    print("Created public files for React app")

def main():
    """Set up the React frontend"""
    # Make sure Node.js and npm are installed
    if not check_node_npm():
        return
    
    # Create frontend directory
    frontend_dir = "frontend"
    if not os.path.exists(frontend_dir):
        print(f"Creating {frontend_dir} directory...")
        os.makedirs(frontend_dir)
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Create React app public files first
    create_react_public_files()
    
    # Create package.json if it doesn't exist
    if not os.path.exists("package.json"):
        print("Creating package.json...")
        with open("package.json", "w") as f:
            f.write("""{
  "name": "elevenlabs-conversations-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.4.0",
    "bootstrap": "^5.3.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.14.1",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "proxy": "http://localhost:5000"
}""")
    
    # Install dependencies
    print("Installing dependencies...")
    if not run_command("npm install"):
        return
    
    # Install additional dependencies
    print("Installing additional dependencies...")
    if not run_command("npm install axios react-router-dom bootstrap"):
        return
    
    # Create needed directories
    os.makedirs("src/components", exist_ok=True)
    os.makedirs("src/pages", exist_ok=True)
    
    print("\nFrontend setup completed successfully!")
    print("\nTo start the development server:")
    print("1. In one terminal window, run: python api.py")
    print("2. In another terminal window, navigate to the frontend directory and run: npm start")

if __name__ == "__main__":
    main() 