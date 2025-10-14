from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize the Flask application
app = Flask(__name__)

# --- Google Sheets Integration ---
# Define the scope of the APIs
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Add your credentials file
CREDS = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPE)

# Authorize the client
client = gspread.authorize(CREDS)

# Find the spreadsheet by its name and open the first sheet
# Make sure the name matches your Google Sheet's name exactly
sheet = client.open("FOSSHACK Registrations").sheet1
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data as a list in the correct order
    name = request.form.get('name')
    year = request.form.get('year')
    semester = request.form.get('semester')
    department = request.form.get('department')
    section = request.form.get('section')
    phone = request.form.get('phone')

    # Create a list of values to append to the sheet
    new_row = [name, year, semester, department, section, phone]

    # Append the new row to the Google Sheet
    sheet.append_row(new_row)

    # Redirect to a success page
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

# This part is for local testing. Render will use its own command.
if __name__ == '__main__':
    app.run(debug=True)