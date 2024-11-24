const fs = require('fs');

exports.handler = async (event) => {
    const data = JSON.parse(event.body);
    const filePath = './data/vouchers.json';

    try {
        let vouchers = [];
        if (fs.existsSync(filePath)) {
            vouchers = JSON.parse(fs.readFileSync(filePath));
        }
        vouchers.push(data);
        fs.writeFileSync(filePath, JSON.stringify(vouchers, null, 2));
        return {
            statusCode: 200,
            body: JSON.stringify({ success: true }),
        };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ error }) };
    }
};
