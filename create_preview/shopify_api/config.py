import os

SHOPIFY_API_KEY = os.environ.get("SHOPIFY_API_KEY")
SHOPIFY_SECRET = os.environ.get("SHOPIFY_SECRET")

APP_NAME = "Paperplace Custom Stationary Applet"
SERVER_HOSTNAME = "pp-custom-stationary-preview.herokuapp.com"
SERVER_BASE_URL = f"https://{SERVER_HOSTNAME}"
INSTALL_REDIRECT_URL = f"{SERVER_BASE_URL}/app_installed"

WEBHOOK_APP_UNINSTALL_URL = f"https://{SERVER_HOSTNAME}/app_uninstalled"
