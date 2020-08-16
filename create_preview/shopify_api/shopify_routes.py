import uuid
import os
import json
import logging

from flask import Flask, redirect, request, render_template

import create_preview.shopify_api.helpers as helpers
from create_preview.shopify_api.shopify_client import ShopifyStoreClient

from create_preview.shopify_api.config import WEBHOOK_APP_UNINSTALL_URL

from create_preview import APP

ACCESS_TOKEN = None
NONCE = None
ACCESS_MODE = []  # Defaults to offline access mode if left blank or omitted. https://shopify.dev/concepts/about-apis/authentication#api-access-modes
SCOPES = ['write_script_tags']  # https://shopify.dev/docs/admin-api/access-scopes


@APP.route('/app_launched', methods=['GET'])
@helpers.verify_web_call
def app_launched():
    shop = request.args.get('shop')
    global ACCESS_TOKEN, NONCE

    if ACCESS_TOKEN:
        paper_place = ShopifyStoreClient(shop=shop, access_token=ACCESS_TOKEN)
        paper_place_script_tags = paper_place.get_script_tags()
        print(paper_place_script_tags)
        return render_template('welcome.html', tags=paper_place_script_tags)

    # The NONCE is a single-use random value we send to Shopify so we know the next call from Shopify is valid (see #app_installed)
    #   https://en.wikipedia.org/wiki/Cryptographic_nonce
    NONCE = uuid.uuid4().hex
    redirect_url = helpers.generate_install_redirect_url(shop=shop, scopes=SCOPES, nonce=NONCE, access_mode=ACCESS_MODE)
    return redirect(redirect_url, code=302)

@APP.route('/add_script')
@helpers.verify_web_call
def add_script():
    shop = request.args.get('shop')
    global ACCESS_TOKEN, NONCE

    if ACCESS_TOKEN:
        paper_place = ShopifyStoreClient(shop=shop, access_token=ACCESS_TOKEN)
        paper_place.update_script_tag(src="https://pp-custom-stationary-preview.herokuapp.com/static/product_handlers.js")
        
    return redirect('/app_launched')

@APP.route('/app_installed', methods=['GET'])
@helpers.verify_web_call
def app_installed():
    state = request.args.get('state')
    global NONCE, ACCESS_TOKEN

    # Shopify passes our NONCE, created in #app_launched, as the `state` parameter, we need to ensure it matches!
    if state != NONCE:
        return "Invalid `state` received", 400
    NONCE = None

    # Ok, NONCE matches, we can get rid of it now (a nonce, by definition, should only be used once)
    # Using the `code` received from Shopify we can now generate an access token that is specific to the specified `shop` with the
    #   ACCESS_MODE and SCOPES we asked for in #app_installed
    shop = request.args.get('shop')
    code = request.args.get('code')
    ACCESS_TOKEN = ShopifyStoreClient.authenticate(shop=shop, code=code)

    # We have an access token! Now let's register a webhook so Shopify will notify us if/when the app gets uninstalled
    # NOTE This webhook will call the #app_uninstalled function defined below
    shopify_client = ShopifyStoreClient(shop=shop, access_token=ACCESS_TOKEN)
    shopify_client.create_webook(address=WEBHOOK_APP_UNINSTALL_URL, topic="app/uninstalled")

    redirect_url = helpers.generate_post_install_redirect_url(shop=shop)
    return redirect(redirect_url, code=302)


@APP.route('/app_uninstalled', methods=['POST'])
@helpers.verify_webhook_call
def app_uninstalled():
    # https://shopify.dev/docs/admin-api/rest/reference/events/webhook?api[version]=2020-04
    # Someone uninstalled your app, clean up anything you need to
    # NOTE the shop ACCESS_TOKEN is now void!
    global ACCESS_TOKEN
    ACCESS_TOKEN = None

    webhook_topic = request.headers.get('X-Shopify-Topic')
    webhook_payload = request.get_json()
    logging.error(f"webhook call received {webhook_topic}:\n{json.dumps(webhook_payload, indent=4)}")

    return "OK"


@APP.route('/data_removal_request', methods=['POST'])
@helpers.verify_webhook_call
def data_removal_request():
    # https://shopify.dev/tutorials/add-gdpr-webhooks-to-your-app
    # Clear all personal information you may have stored about the specified shop
    return "OK"