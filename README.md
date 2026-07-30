# 📊 Log Analyzer & Monitoring Dashboard

Hey there! Welcome to the **Log Analyzer & Monitoring Dashboard**. 👋

Whether you're a seasoned developer or just starting your coding journey, managing system logs can feel a bit overwhelming. You're usually staring at thousands of lines of text trying to find that one specific error that crashed your app. 

That's exactly why this tool was built! It takes those messy, endless log files and turns them into a beautiful, easy-to-read visual dashboard. It automatically scans your logs for errors, highlights anomalies, and gives you a nice summary of your system's health. 

---

## ✨ Features
- **Lightning Fast:** Uses Python generators under the hood, meaning it can process massive log files without eating up all your computer's memory.
- **Smart Pattern Matching:** Automatically detects things like database timeouts, authentication failures, and custom errors using Regular Expressions.
- **Beautiful UI:** A sleek, minimalist web dashboard built with HTML/CSS and Chart.js. No more staring at a black terminal!
- **Drag-and-Drop:** Simply drag your `.log` file into the browser to see the magic happen.

---

## 🚀 How to Run It (Beginner Friendly!)

Getting this up and running on your own machine is super easy. Just follow these steps:

### 1. Prerequisites
First, make sure you have **Python** installed on your computer. You can download it from [python.org](https://www.python.org/).

### 2. Clone the Project
Download this project to your computer. Open your terminal or command prompt and run:
```bash
git clone https://github.com/lvenkatasai/Log_analyser.git
cd Log_analyser
```

### 3. Install the Required Tools
We use a lightweight Python framework called Flask to run the web server. Install it by running:
```bash
pip install -r requirements.txt
```

### 4. Start the Application!
Now, just start the server with this command:
```bash
python app.py
```

### 5. View Your Dashboard
Open your favorite web browser (like Chrome, Edge, or Safari) and go to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Boom! You should see the Log Analyzer dashboard. 

---

## 🧪 Testing it Out

Don't have a log file handy? No problem! We've included a script that generates a massive, realistic log file for you to play with.

1. In your terminal, run `python generate_logs.py`
2. It will create a file called `large_sample_logs.log` (with about 15,000 lines of data!).
3. Drag and drop that file into your dashboard and watch how fast it gets analyzed!

---

## 🛠️ How it Works (Under the Hood)
- **`log_parser.py`**: The engine. It reads files line-by-line using Python `yield` generators.
- **`patterns.py`**: The brain. It stores the Regular Expressions (RegEx) that tell the parser what an "error" or a "timestamp" looks like.
- **`app.py`**: The server. It handles the file upload and sends the data to your browser.
- **`static/`**: The face. Contains the HTML, CSS, and JavaScript that makes everything look pretty.

Enjoy analyzing your logs! If you run into any issues or want to add a new feature, feel free to dive into the code! 💻✨
