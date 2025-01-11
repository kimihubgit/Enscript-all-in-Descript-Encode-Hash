function cfDecodeEmail(encodedString) {
    var email = "", r = parseInt(encodedString.substr(0, 2), 16), n, i;
    for (n = 2; encodedString.length - n; n += 2){
    	i = parseInt(encodedString.substr(n, 2), 16) ^ r;
		email += String.fromCharCode(i);
    }
    return email;
}

console.log(cfDecodeEmail("b4d9d1f4c1c7d5d9d5d1ded5ce9ad7dbd9"));


function cfEncodeEmail(email) {
  var encodedString = "";
  var r = Math.floor(Math.random() * 256); // Tạo một giá trị ngẫu nhiên từ 0 đến 255
  encodedString += r.toString(16).padStart(2, '0'); // Chuyển đổi r sang hệ thập lục phân và thêm vào chuỗi mã hóa
  for (var n = 0; n < email.length; n++) {
      var i = email.charCodeAt(n) ^ r; // Lấy mã ASCII của ký tự tại vị trí n và thực hiện phép XOR với r
      encodedString += i.toString(16).padStart(2, '0'); // Chuyển đổi kết quả sang hệ thập lục phân và thêm vào chuỗi mã hóa
  }

  return encodedString;
}
// Ví dụ sử dụng
var encodedEmail = cfEncodeEmail("me@usamaejaz.com");
console.log(encodedEmail);




