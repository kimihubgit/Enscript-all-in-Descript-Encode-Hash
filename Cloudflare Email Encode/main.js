function cfDecodeEmail(encodedString) {
    var email = "", r = parseInt(encodedString.substr(0, 2), 16), n, i;
    for (n = 2; encodedString.length - n; n += 2){
    	i = parseInt(encodedString.substr(n, 2), 16) ^ r;
		email += String.fromCharCode(i);
    }
    return email;
}

console.log(cfDecodeEmail("543931142127353935313e352e7a373b39")); // usage