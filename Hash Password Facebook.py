import requests
from bs4 import BeautifulSoup
import random
import sys
import json
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from nacl.public import SealedBox, PublicKey
import nacl.utils
import time
import requests
import re
import string
import urllib.parse
PUBLIC_KEY_LENGTH = 64
I = 1
J = 1
K = 1
L = 48  
M = 2
N = 32
O = 16
P = J + K + M + N + L + O

def seal(buffer, public_key):
    box = SealedBox(PublicKey(public_key))
    return box.encrypt(buffer)

def r(a):
    return bytes.fromhex(a)

def hash_password(a, c, d, e):
    f = P + len(d)
    if  (c) != PUBLIC_KEY_LENGTH:
        raise ValueError('public key is not a valid hex string')
    
    s = r(c)
    if not s:
        raise ValueError('public key is not a valid hex string')
    
    t = bytearray(f)
    u = 0
    t[u] = I
    u += J
    t[u] = a
    u += K

    key = nacl.utils.random(N)
    iv = bytes(12) 
    aes_gcm = AESGCM(key)
    
    encrypted_data = aes_gcm.encrypt(iv, d, e)
    
    sealed_key = seal(key, s)
    t[u] = len(sealed_key) & 255
    t[u + 1] = (len(sealed_key) >> 8) & 255
    u += M
    t[u:u+len(sealed_key)] = sealed_key
    u += N + L
    if len(sealed_key) != N + L:
        raise ValueError('encrypted key is the wrong length')
    
    tag = encrypted_data[-O:]
    encrypted_data_without_tag = encrypted_data[:-O]
    t[u:u+O] = tag
    u += O
    t[u:] = encrypted_data_without_tag

    return bytes(t)

def hash_manager(public_key_data, timestamp, password):
    h = password.encode('utf-8')
    i = timestamp.encode('utf-8')
    result = hash_password(int(public_key_data['keyId']), public_key_data['publicKey'], h, i)
    return base64.b64encode(result).decode('utf-8')

def get_public_key():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9',
        'cache-control': 'max-age=0',
        'dpr': '2',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.122", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"14.3.1"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'viewport-width': '2072'
    }
    
    response = requests.get('https://www.facebook.com/', headers=headers)
    public_key_pattern = r'"publicKey":"([a-zA-Z0-9]+)"'
    key_id_pattern = r'"keyId":(\d+)'
        
    public_key_match = re.search(public_key_pattern, response.text)
    key_id_match = re.search(key_id_pattern, response.text)
    
    if public_key_match and key_id_match:
        return {
            'publicKey': public_key_match.group(1),
            'keyId': int(key_id_match.group(1))
        }
    else:
        print("Không tìm thấy public key hoặc key ID.")
        return None

def Encrypt_Password(password):
    current_time = str(int(time.time()))
    try:
        public_key_data = get_public_key()
        print(public_key_data)
        if public_key_data:
            hashed_password = hash_manager(public_key_data, current_time, password)
            return f"#PWD_BROWSER:5:{current_time}:{hashed_password}"
        else:
            print("Failed to retrieve public key data.")
            return None
    except Exception as error:
        print("Error hashing password:", error)
        return None


def Check_Live_Fb(uid):
    url = f"https://graph2.facebook.com/v3.3/{uid}/picture?redirect=0"
    response = requests.get(url, timeout=30)
    check_data = response.json()
    
    if not check_data.get('data', {}).get('height') or not check_data.get('data', {}).get('width'):
        return 'DIE'
    return 'LIVE'

def Login_M_Facebook(Username, Password):
    session = requests.Session()
    headers = {
        "sec-ch-prefers-color-scheme": "dark",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "accept": "*/*",
        "origin": "https://m.facebook.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://m.facebook.com/",
        "accept-encoding": "gzip, deflate",
        "accept-language": "vi-VN,vi;q=0.9",
    }

    response = session.get('https://m.facebook.com', headers=headers)

    pattern2 = r'"LSD".*?"token":\s*"([^"]+)"'
    match = re.search(pattern2, response.text)

    if match:
        lsd_token = match.group(1)
    else:
        print('Không lấy được LSD TOKEN')
        return

    jazoest = re.search(r'"jazoest"\s*,\s*"(\d+)"', response.text).group(1) if re.search(r'"jazoest"\s*,\s*"(\d+)"', response.text) else None
    lsd = re.search(r'"tokenName":"lsd","token":"([^"]+)"', response.text).group(1) if re.search(r'"tokenName":"lsd","token":"([^"]+)"', response.text) else None  
    dtsg = re.search(r'"dtsg":\s*{\s*"token":\s*"([^"]+)"', response.text).group(1) if re.search(r'"dtsg":\s*{\s*"token":\s*"([^"]+)"', response.text) else None
    hsi = re.search(r'"hsi":"(\d+)"', response.text).group(1) if re.search(r'"hsi":"(\d+)"', response.text) else None
    haste_session = re.search(r'"haste_session"\s*:\s*"([^"]+)"', response.text).group(1) if re.search(r'"haste_session"\s*:\s*"([^"]+)"', response.text) else None
    id_matches = re.findall(r'id:"([a-zA-Z0-9]+:\d+)"', response.text)

    if id_matches:
        userinput = id_matches[3]
        passinput = id_matches[7]
    else:
        userinput = 'ro0q40:69'
        passinput = 'ro0q40:70'

    match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', response.text)

    if match:
        UUID =  match.group(1)
    else:
        UUID = 'bfab7c2e-8bb0-4287-a51b-36e26785f3e3'

    pattern = r'\(bk\.action\.i64\.Const,\s*(\d+)\)'
    match = re.search(pattern, response.text)

    if match:
        number = match.group(1)

    data = {
        "__aaid": "0",
        "__user": "0",
        "__a": "1",
        "__req": "y",
        "__hs": haste_session,
        "dpr": "3",
        "__ccg": "EXCELLENT",
        "__rev": "1019105191",
        "__s": f":{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}:{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}",
        "__hsi": hsi,
        "__dyn": "0wzpawlE72fDg9ppo5S12wAxu13w9y1DxW0Oohw5ux60Vo1a852q1ew2io0D24o1MUaE1Do1u81x82ewnE3Mw4WwSyE25w8W0Lo6-1CwOw5jw4JwzK0zo3jw",
        "__csr": "",
        "fb_dtsg": dtsg,
        "jazoest": jazoest,
        "lsd": lsd_token,
        "params": '{"params":"{\\"server_params\\":{\\"credential_type\\":\\"password\\",\\"username_text_input_id\\":\\"'+userinput+'\\",\\"password_text_input_id\\":\\"'+passinput+'\\",\\"login_source\\":\\"Login\\",\\"login_credential_type\\":\\"none\\",\\"server_login_source\\":\\"login\\",\\"ar_event_source\\":\\"login_home_page\\",\\"should_trigger_override_login_success_action\\":0,\\"should_trigger_override_login_2fa_action\\":0,\\"is_caa_perf_enabled\\":0,\\"reg_flow_source\\":\\"login_home_native_integration_point\\",\\"caller\\":\\"gslr\\",\\"is_from_landing_page\\":0,\\"is_from_empty_password\\":0,\\"is_from_password_entry_page\\":0,\\"is_from_assistive_id\\":0,\\"is_from_msplit_fallback\\":0,\\"INTERNAL__latency_qpl_marker_id\\":36707139,\\"INTERNAL__latency_qpl_instance_id\\":\\"'+str(number)+'\\",\\"device_id\\":null,\\"family_device_id\\":null,\\"waterfall_id\\":\\"'+UUID+'\\",\\"offline_experiment_group\\":null,\\"layered_homepage_experiment_group\\":null,\\"is_platform_login\\":0,\\"is_from_logged_in_switcher\\":0,\\"is_from_logged_out\\":0,\\"access_flow_version\\":\\"F2_FLOW\\"},\\"client_input_params\\":{\\"machine_id\\":\\"\\",\\"contact_point\\":\\"'+Username+'\\",\\"password\\":\\"'+Password+'\\",\\"accounts_list\\":[],\\"fb_ig_device_id\\":[]}}"}'
    }

    headerss = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "vi-VN,vi;q=0.9",
        "content-length": str(len(str(data))),
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "origin": "https://m.facebook.com",
        "priority": "u=1, i",
        "referer": "https://m.facebook.com/",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    session.cookies.set('m_pixel_ratio', '3')
    session.cookies.set('locale', 'vi_VN')
    session.cookies.set('wd', '430x932')
    session.cookies.set('ps_l', '1')
    session.cookies.set('ps_n', '1')

    url = 'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.login.async.send_login_request&type=action&__bkv=e83b925010f428c02e9a28277ebe1ac259315059ef636d91d59afb3de1f921fa'

    response = session.post(url, data=data, headers=headerss, allow_redirects=True)
    # print(response.text)
    json_data = json.loads(response.text.split('for (;;);')[1])

    payload = json_data.get("payload", {})
    bloks_payload = payload.get("layout", {}).get("bloks_payload", {})
    embedded_payloads = bloks_payload.get("embedded_payloads", [])

    if 'currentUser' in response.text:
       cookies_dict = session.cookies.get_dict() 
       c_user = cookies_dict.get('c_user')
       
       if c_user:
           check_live = Check_Live_Fb(c_user)
           if check_live == 'DIE':
               print(f"{c_user}|Cookie DIE")
           else:
               print("Get thành công Cookie:")
               print('; '.join(f"{k}={v}" for k, v in cookies_dict.items()))
       else:
           print("Không tìm thấy c_user trong cookie")
           
    elif 'server_data' in response.text:
       print("CheckPoint") 
       print(response.text)


    else:
       if embedded_payloads:
           dialog = (embedded_payloads[0]
                   .get("payload", {})
                   .get("layout", {})
                   .get("bloks_payload", {})
                   .get("tree", {})
                   .get("bk.components.dialog.Dialog", {}))
           
           print("Title:", dialog.get("title"))
           print("Message:", dialog.get("message"))
       else:
           print("Không có embedded payloads")
           print("Response Text:", response.text)


Username = 'dxp65t6n@boranora.com'
Password = Encrypt_Password("Haikbhb123")

Login_M_Facebook(Username, Password)



