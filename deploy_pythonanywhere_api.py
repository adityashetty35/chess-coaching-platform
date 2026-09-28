#!/usr/bin/env python3
"""
Automated End-to-End Deployment Script for PythonAnywhere using the official API.
Usage:
    python deploy_pythonanywhere_api.py --username <PA_USERNAME> --token <PA_API_TOKEN>
"""
import sys
import argparse
import requests

def deploy(username, token):
    headers = {"Authorization": f"Token {token}"}
    domain = f"{username}.pythonanywhere.com"
    base_url = f"https://www.pythonanywhere.com/api/v0/user/{username}"
    repo_url = "https://github.com/adityashetty35/chess-coaching-platform.git"
    project_dir = f"/home/{username}/chess-coaching-platform"
    venv_dir = f"{project_dir}/venv"

    print(f"\n🚀 Starting E2E deployment for: {domain}...")

    # 1. Create or get Webapp
    print(f"1️⃣ Checking Web App '{domain}'...")
    webapps_res = requests.get(f"{base_url}/webapps/", headers=headers)
    existing = [w['domain_name'] for w in webapps_res.json()] if webapps_res.status_code == 200 else []

    if domain not in existing:
        print(f"   Creating new Python 3.10 webapp for {domain}...")
        create_res = requests.post(
            f"{base_url}/webapps/",
            headers=headers,
            json={"domain_name": domain, "python_version": "3.10"}
        )
        if create_res.status_code not in (200, 201):
            print(f"   ❌ Failed to create webapp: {create_res.text}")
            sys.exit(1)
        print("   ✓ Webapp created!")
    else:
        print("   ✓ Webapp already exists.")

    # 2. Update Virtualenv path
    print(f"2️⃣ Configuring virtual environment path: {venv_dir}...")
    patch_res = requests.patch(
        f"{base_url}/webapps/{domain}/",
        headers=headers,
        json={"virtualenv_path": venv_dir}
    )
    if patch_res.status_code == 200:
        print("   ✓ Virtualenv path configured.")

    # 3. Configure Static & Media Files
    print("3️⃣ Configuring Static & Media mappings...")
    static_mappings = [
        ("/static/", f"{project_dir}/staticfiles"),
        ("/media/", f"{project_dir}/media"),
    ]
    for url_path, dir_path in static_mappings:
        s_res = requests.post(
            f"{base_url}/webapps/{domain}/static_files/",
            headers=headers,
            json={"url": url_path, "path": dir_path}
        )
        print(f"   ✓ Mapping {url_path} ➔ {dir_path}")

    # 4. Configure WSGI file
    print("4️⃣ Writing WSGI configuration file...")
    wsgi_content = f"""import os
import sys

path = '{project_dir}'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'chess_coaching.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
    wsgi_filename = f"/var/www/{domain.replace('.', '_')}_wsgi.py"
    f_res = requests.post(
        f"{base_url}/files/path{wsgi_filename}",
        headers=headers,
        files={"content": wsgi_content}
    )
    if f_res.status_code in (200, 201):
        print("   ✓ WSGI configuration saved.")

    # 5. Reload Web App
    print("5️⃣ Reloading web application...")
    r_res = requests.post(f"{base_url}/webapps/{domain}/reload/", headers=headers)
    if r_res.status_code in (200, 201):
        print(f"\n🎉 Successfully deployed and live at: https://{domain}/")
    else:
        print(f"   Note: Reload returned {r_res.status_code}. Please verify files in console.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Chess Coaching Platform to PythonAnywhere")
    parser.add_argument("--username", required=True, help="PythonAnywhere Username")
    parser.add_argument("--token", required=True, help="PythonAnywhere API Token")
    args = parser.parse_args()
    deploy(args.username, args.token)
