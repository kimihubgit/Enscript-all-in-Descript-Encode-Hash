// Import các module cần thiết
const express = require('express');
const crypto = require('crypto');

// Khởi tạo Express app
const app = express();
const port = 4000; // Cổng mà server sẽ chạy

// Khởi tạo đối tượng E
function E() {}

// Thêm phương thức checkAbcXyz vào prototype của E
E.prototype.checkAbcXyz = function(t, username) {
    return crypto.createHash("md5")
        .update(
            "1732012318" + "8b0366fcea61d91a" + "Android" + username + "ce771e92fefac8cc3a3ae5795339232b"
        )
        .digest("hex");
};

// Khởi tạo một instance của E
const e = new E();

// Middleware để parse JSON request body
app.use(express.json());

// Định nghĩa endpoint API
app.post('/generate-hash', (req, res) => {
    const { username } = req.body;

    // Kiểm tra đầu vào
    if (!username) {
        return res.status(400).json({ error: 'Username is required' });
    }

    const t = Date.now(); // Thời gian hiện tại dạng timestamp
    const hash = e.checkAbcXyz(t, username); // Gọi hàm để tạo hash

    // Trả về kết quả
    res.json({
        timestamp: t,
        username: username,
        hash: hash,
    });
});

// Khởi động server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
