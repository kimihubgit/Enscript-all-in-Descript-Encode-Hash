const crypto = require('crypto');

function encryptPassword(password, o_v1, o_v2) {
  // Tạo một hash MD5 từ password
  const s = crypto.createHash('md5').update(password).digest('hex');

  // Tạo double hash SHA-256
  const hash1 = crypto.createHash('sha256').update(s + o_v1).digest('hex');
  const b = crypto.createHash('sha256').update(hash1 + o_v2).digest('hex');

  // Mã hóa AES-256-ECB
  const cipher = crypto.createCipheriv('aes-256-ecb', Buffer.from(b, 'hex'), Buffer.alloc(0));
  let M = cipher.update(Buffer.from(s, 'hex'), 'binary', 'hex');
  M += cipher.final('hex');

  // Trả về 32 ký tự đầu tiên của chuỗi hex
  return M.substring(0, 32);
}

// Ví dụ sử dụng hàm
console.log(encryptPassword('examplePassword', 'value1', 'value2'));
