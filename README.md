# Client Project Setup Guide

This guide will walk you through the process of setting up your client project. Please follow the steps below:

## Prerequisites

- Node.js and npm installed on your machine.
- Python and pip installed on your machine.
- Virtualenv installed globally (`pip install virtualenv`).

## Steps

1. **Clone the Repository:**

    ```bash
    git clone <repository_url>
    ```

2. **Navigate to the Client Folder:**

    ```bash
    cd client
    ```

3. **Install Dependencies:**

    ```bash
    npm install
    ```

4. **Run the Client Development Server:**

    ```bash
    npm run dev
    ```

    This command starts the development server for the client application.

5. **Navigate to the Root Directory:**

    ```bash
    cd ..
    ```

6. **Set Up Virtual Environment:**

    ```bash
    virtualenv venv
    ```

7. **Activate Virtual Environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

8. **Install Python Dependencies:**

    ```bash
    pip install -r ./server/requirements.txt
    ```

9. **Create .env File:**

    Create a file named `.env` in the root directory and add the following content:

    ```plaintext
    GOOGLE_SERP_API_KEY = 'YOUR_GOOGLE_SERP_API_KEY'
    SERPER_API_KEY1 = 'YOUR_SERPER_API_KEY1'
    SERPER_API_KEY2 = 'YOUR_SERPER_API_KEY2'
    TAVILY_API_KEY1 = 'YOUR_TAVILY_API_KEY1'
    TAVILY_API_KEY2 = 'YOUR_TAVILY_API_KEY2'
    TAVILY_API_KEY3 = 'YOUR_TAVILY_API_KEY3'
    GOOGLE_API_KEY1 = 'YOUR_GOOGLE_API_KEY1'
    GOOGLE_API_KEY2 = 'YOUR_GOOGLE_API_KEY2'
    GOOGLE_API_KEY3 = 'YOUR_GOOGLE_API_KEY3'
    SECRET_KEY = 'YOUR_SECRET_KEY'
    ```

    Replace `YOUR_GOOGLE_SERP_API_KEY`, `YOUR_SERPER_API_KEY1`, `YOUR_SERPER_API_KEY2`, `YOUR_TAVILY_API_KEY1`, `YOUR_TAVILY_API_KEY2`, `YOUR_TAVILY_API_KEY3`, `YOUR_GOOGLE_API_KEY1`, `YOUR_GOOGLE_API_KEY2`, `YOUR_GOOGLE_API_KEY3`, and `YOUR_SECRET_KEY` with your actual API keys and secret key.

10. **Run Flask Server:**

    ```bash
    python app.py
    ```

11. **Access Your Application:**


    Once the Flask server is running, you can access your application by visiting `http://localhost:5000` in your web browser.

    
    
![WhatsApp Image 2024-04-24 at 11 28 28 PM](https://github.com/Mehekjain05/MindCraft/assets/85340069/652d6648-4c39-47e8-b1e2-8929abf7334c)



![WhatsApp Image 2024-04-24 at 11 28 54 PM](https://github.com/Mehekjain05/MindCraft/assets/85340069/b48491bc-9aa1-4b84-8912-a30fd904ef24)




![WhatsApp Image 2024-04-24 at 11 32 15 PM](https://github.com/Mehekjain05/MindCraft/assets/85340069/6dea0ee7-5798-4353-a54f-b9398c4a5e13)



![WhatsApp Image 2024-04-24 at 11 31 32 PM](https://github.com/Mehekjain05/MindCraft/assets/85340069/3ea0ddd7-0bff-4e41-b144-89d74c8a6fc8)


