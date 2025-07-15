 Amazon Price Tracker (Python Script)

This is a basic Python web scraper that tracks the price of a product on Amazon.ca and sends an email alert when the price drops below a specified target.

Inspiration:

This project was inspired by this YouTube tutorial - https://www.youtube.com/watch?v=HiOtQMcI5wg.
I've made some tweaks and added a few improvements for better error handling and flexibility.

Disclaimer!

This is for learning purposes only not for commercial scrapes and may not work consistently due to website changes.
Amazon may show CAPTCHA or block frequent scraping requests. Use responsibly.

The script scrapes:
- Product title
- Current price
- Date of check
  
Each run appends the result to a CSV file (`AmazonWebScraper.csv`). If the price drops below your target, it sends an email notification using your Gmail account.

---------------------------------------

 Features

- Web scraping using `requests` and `BeautifulSoup`
- Email alert via `smtplib` (requires a Gmail App Password)
- Simple CSV logging
- `.env` support to protect credentials

----------------------------------------

 Setup Instructions

1. **Clone the repo** or download the script.
2. Install the dependencies:
   
   pip install requests beautifulsoup4 python-dotenv
3. Create a .env file in the same folder with:
 
    EMAIL_ADDRESS=your@gmail.com
    EMAIL_PASSWORD=your_16_char_app_password
4. Run the script:
    python amazon_scraper.py

Happy Learning :)
