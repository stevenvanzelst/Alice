# Alice

## Overview

This educational software demonstrates how to create a simple keylogger and browser history tracker in Python. It captures keystrokes, logs browser history, and sends the collected data via email. The code is designed for educational purposes only, to help you understand the concepts of file handling, email communication, and the use of Python libraries.

**Important:** This software should only be used in a legal and ethical manner, such as on your own devices or with explicit permission from users.

## Features

- **Keylogging**: Captures keystrokes and logs them to a text file.
- **Browser History Tracking**: Retrieves browser history and saves it in a JSON file.
- **Email Reporting**: Sends logs and history via email.
- **Startup Integration**: Automatically adds the script to Windows startup for persistence.
  
## Requirements

- Python 3.x
- Libraries: 
  - `ctypes`
  - `os`
  - `shutil`
  - `smtplib`
  - `email`
  - `browser_history`
  - `pynput`
  
You can install the required libraries using pip:

```bash
pip install browser-history pynput
```

## How to Use

1. **Setup**:
   - Ensure you have Python 3.x installed on your system.
   - Install the required libraries using the command mentioned above.
   - Modify the email settings in the `main()` function:
     - Replace `example@tuta.com` with your actual email address.
     - Update the SMTP server and port if necessary.

2. **Run the Script**:
   - Execute the script using Python:
   ```bash
   python alice.py
   ```

3. **Data Collection**:
   - The script will run for a specified duration (2 minutes) before entering a loop where it collects browser history and keystrokes.
   - Every 20 seconds, the collected data will be sent to the specified email address.

4. **Accessing Logs**:
   - Keystrokes will be stored in `keyfile.txt`.
   - Browser history will be saved in `history.json`.

## Important Notes

- **Ethical Use**: Ensure you comply with local laws and regulations regarding privacy and data collection.
- **Testing**: The script is intended for educational purposes. Test it only in safe environments, like your own computer.
- **Security**: Consider the security implications of storing and transmitting sensitive data like keystrokes.

## Disclaimer

This software is provided for educational purposes only. The author does not assume any responsibility for its use in any unlawful or unethical manner. Always respect the privacy of others and comply with applicable laws. 

## License

This project is licensed under the MIT License - see below for details:

MIT License Copyright (c) [year] [fullname] Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Author

- Steven van Zelst
