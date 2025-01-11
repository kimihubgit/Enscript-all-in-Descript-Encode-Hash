function customHash(input) {
  let hash = 0;

  for (let i = 0; i < input.length; i++) {
    let char = input.charCodeAt(i);
    hash = ((hash << 5) - hash) + char; // Phép nhân và phép cộng
    hash = hash & hash; // Chuyển hash thành một số nguyên 32 bit
  }

  // Trộn kết quả bằng cách sử dụng XOR với một số ngẫu nhiên
  hash = hash ^ 0xABCDEF;

  // Đảm bảo kết quả là một giá trị dương
  return Math.abs(hash).toString(16); // Trả về dưới dạng hex
}

// Ví dụ sử dụng hàm
console.log(customHash('hello My Friend'));
