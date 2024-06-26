## 🚀 About The Project

This application, developed by [@Erik Petrosyan](https://github.com/PetrosyanDev), is designed to parse .mrc files from the Library of Congress and adjust them for use in Google Sheets.

### Getting Started

Follow these steps to set up and run the project:

1. **Install Dependencies**

   Ensure you have all the necessary packages by running:

   ```bash
   pip install -r requirements.txt
   ```

2. **Add Configuration**

   Create a secrets.json file with the following content, replacing "YOUR_OPENAI_API_KEY" with your actual OpenAI API key:

   ```json
   {
   	"api_key": "YOUR_OPENAI_API_KEY"
   }
   ```

3. **Run the Application**

   Execute the main script:

   ```bash
   python main.py
   ```
