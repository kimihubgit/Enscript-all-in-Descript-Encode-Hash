const CryptoJS = require('crypto-js');
const fs = require('fs');
var os = require('os');

const prompt = msg => {
    fs.writeSync(1, String(msg));
    let s = '',
    buf = Buffer.alloc(1);
    while (buf[0] - 10 && buf[0] - 13)
        s += buf, fs.readSync(0, buf, 0, 1, 0);
    return s.slice(1);
};

const key = CryptoJS.enc.Utf8.parse("nFgAIwYQumyveJTblowsalary");
const iv = CryptoJS.enc.Utf8.parse("lowbTJevymuQYwIAgFnsalary");

console.log(`
         ████████               How to uses:
         ██    ██               1. Get API from MyTV, modify whatever you want
         ██    ██               2. Get nosalary string
         ████████               3. Run the code, put nosalary string
            ██                  4. Profit
       ███████████████          
     ███    ██                  
     █      █████               
     ██     ██                  
      ██    ██                  
       ███  ██                  
         ██ ██   SalaryDecrypt  
          ████   by bang1338    
            ██                  
            ████                
            ██ ██               
            ██  ██              
            ██    ██            
            ██     ██           
         █████      █           
            ██     ██           
      ██████████████            
            ██                  
         ████████               
         ██    ██               
         ██    ██               
         ████████               
`)

const input = prompt('Input nosalary here: ');
const encryptedText = input.replace("nosalary!@#bXVsdGlwYXNz123-", "");

const decrypted = CryptoJS.AES.decrypt(encryptedText, key, {
    iv: iv,
    mode: CryptoJS.mode.CFB,
    padding: CryptoJS.pad.NoPadding
}).toString(CryptoJS.enc.Utf8);

console.log(os.EOL)
console.log(decrypted);
const data = JSON.parse(decrypted);
console.log(os.EOL + 'URL:')
console.log(data.url)
console.log("DRM: " + data.is_bitmovin)
