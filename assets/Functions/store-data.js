const { google } = require('googleapis');
const sheets = google.sheets('v4');
const serviceAccount = require('./serviceAccountKey.json'); // Path to your service account key

const auth = new google.auth.GoogleAuth({
    credentials: serviceAccount,
    scopes: ['https://www.googleapis.com/auth/spreadsheets'],
});

exports.handler = async (event) => {
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ message: 'Method Not Allowed' }),
        };
    }

    try {
        const data = JSON.parse(event.body);
        const authClient = await auth.getClient();

        await sheets.spreadsheets.values.append({
            auth: authClient,
            spreadsheetId: 'YOUR_SPREADSHEET_ID', // Replace with your Google Sheet ID
            range: 'Sheet1!A1:F1', // Replace with your desired range
            valueInputOption: 'RAW',
            requestBody: {
                values: [
                    [
                        data.orderNo,
                        data.companyName,
                        data.vehicleReg,
                        data.odometerReading,
                        data.litresSupplied,
                        data.date,
                    ],
                ],
            },
        });

        return {
            statusCode: 200,
            body: JSON.stringify({ success: true, message: 'Data saved successfully!' }),
        };
    } catch (error) {
        console.error('Error saving data:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Failed to save data' }),
        };
    }
};

