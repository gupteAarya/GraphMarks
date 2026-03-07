
# Graph Marks

Graph Marks is a lightweight automation tool that tracks test scores, generates performance graphs, and sends analysis directly to Telegram.

![Version](https://img.shields.io/badge/version-v2.1.0-orange)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

🌐 **Live Demo:** https://graphmarks.onrender.com
> **Note:** This is a demo deployment of the repository, so some random or test entries may appear in the database.


## About the Project

Graph Marks is a small automation tool designed to help students track and analyze their test performance over time.

It automatically:
- stores test scores
- generates visual graphs of performance
- calculates improvements between tests
- sends summaries directly to Telegram

This allows quick feedback after every test without manually analyzing marks.

<img width="2842" height="1912" alt="Group 175" src="https://github.com/user-attachments/assets/bc3009c5-09e2-40a3-a21e-62ed8d171080" />


## 💻 Tech Stack
- Charts: Matplotlib, Numpy, Pandas
- Frontend: HTML, CSS, JavaScript
- Charts: Matplotlib, Numpy, Pandas
- Database: SQL
- Backend: Python3
- Messaging: Telegram Bot API ( Telethon )
- Deployment: Render
  

## 📝 How it works

The two main capabilities of this tool are:
| **Having your marks plotted on a graph, calculating the improvements and sending it all to your Telegram inbox** | **Viewing a detailed analysis page where I can compare my past test scores with my current ones** |
|---|---|
| ![Screen Recording 2026-03-06 at 09 09 12](https://github.com/user-attachments/assets/c1a5f1bf-3099-42e7-ab06-9062ac7132b0)| ![Screen Recording 2026-03-06 at 09 10 51](https://github.com/user-attachments/assets/2aa86622-aa14-497b-8e58-f2dcbe176c52) |

The results are received in my Telegram inbox in seconds

<img width="2763" height="2887" alt="Group 48-1" src="https://github.com/user-attachments/assets/fd5ba8aa-7c9a-4ff5-9988-27f1226b825a" />


## ⭐ Features
- Intuitive interface
- Score tracking
- Graph visualization
- Versatile comparisons for scores
- Telegram notifications
- Individual and cumulative statistics sent to Telegram inbox
- Responsive website


## 🚀 Deployment

### Deployment Platform

<p align="center">
<img width="1096" alt="Render Dashboard" src="https://github.com/user-attachments/assets/c71a3f5d-f38b-4ff7-9bb2-f261fce33cf0">
</p>

This project is deployed using **[Render](https://render.com/)**

<img src="https://github.com/user-attachments/assets/5789000e-7767-4cfc-8ef4-e5f324a27763" width="350">

### Continuous Build Status
Render is connected directly to this GitHub repository.  

<img src="https://github.com/user-attachments/assets/603325aa-8198-478e-bf34-e1a6868d309c" width="250">

The hosted version can reflect any **stable commit**.


## 📈 Benefits of This Automation

A principle emphasized in the *Google IT Automation* course on Coursera is that automation should ideally justify itself in terms of **time saved versus time invested**.

### Development Cost

This automation took approximately **3 hours 15 minutes** to develop.

```
3.25 hours × 60 minutes = 195 minutes
```

### Time Saved Per Month

The automation replaces **two manual tasks per month**, each of which previously required **15 minutes**.

```
2 tasks × 15 minutes = 30 minutes saved per month
```

### Break-even Analysis

```
195 minutes ÷ 30 minutes/month ≈ 6.5 months
```

Based on this calculation, it would take approximately **6.5 months** for the time saved by the automation to exceed the time spent building it.

### Practical Benefit

However, the benefit is not purely numerical.  
Because the automation significantly **reduces the effort required**, it increases the likelihood that the task will actually be completed regularly, making the workflow easier and more consistent.


# Local Installation

> ⚠️ **Note on Local Installation**
>
> This project was primarily developed and tested in a **deployed environment**, and local installation was not the primary development workflow.  
> As a result, some parts of the setup — particularly around **secret files and environment configuration** — may require minor debugging depending on your system.
>
> The installation steps below were generated with the assistance of **Windsurf** to provide a structured setup guide. They accurately reflect the project configuration, but if you encounter issues during local setup, please feel free to open an issue in the repository.

### 1. Clone the Repository
```bash
git clone https://github.com/gupteAarya/GraphMarks.git
cd GraphMarks
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
```

### 5. Get Telegram API Credentials
1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Sign in with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy the `api_id` and `api_hash` values to your `.env` file

### 6. Run the Application
```bash
python app.py
```
The app will start on `http://localhost:4000`

### 7. First-Time Setup
- The first time you run the app, you'll be prompted to enter your phone number
- Enter the verification code you receive on Telegram
- The app will remember your session for future runs

## Deployment on Render

### 1. Prepare Your Repository
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Create Render Account
1. Sign up at [https://render.com](https://render.com)
2. Connect your GitHub account

### 3. Create New Web Service
1. Click "New" → "Web Service"
2. Select your repository from GitHub
3. Configure the service:
   - **Name**: marktrack (or your preferred name)
   - **Region**: Choose nearest to your users
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

### 4. Set Environment Variables
In your Render dashboard, add these environment variables:
```
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PORT=4000
```

### 5. Advanced Configuration (Optional)
Create a `render.yaml` file in your repository root:
```yaml
services:
  - type: web
    name: marktrack
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: PORT
        value: 4000
```

### 6. Secret Files
In the secret files section, create a file called ```data.db```
###### (Optional) Directly create a .env file and add your Environment Variables there 

### 7. Deploy
Click "Create Web Service" and Render will:
1. Clone your repository
2. Install dependencies
3. Start the application
4. Provide a public URL

## Troubleshooting

### Common Issues

#### 1. Telegram Session Errors
If you encounter session-related errors:
```bash
# Delete existing session files
rm session.session*
```

#### 2. Database Permission Issues
The app will create `data.db` automatically. Ensure write permissions in the deployment directory.

#### 3. Font Warnings (Optional)
To fix matplotlib font warnings:
```bash
# Install additional fonts (optional)
sudo apt-get install fonts-dejavu-core  # On Ubuntu/Debian
```

#### 4. Port Binding
The app is configured to bind to `0.0.0.0` and use the `PORT` environment variable, which is standard for cloud deployments.

### Environment Variables Reference
- `API_ID`: Telegram API ID (required)
- `API_HASH`: Telegram API hash (required)
- `PORT`: Application port (defaults to 4000)

## Demo Screenshots
<details>
<summary><strong>Demo Screenshots</strong></summary>

<br>

<p align="center">
  <img src="https://github.com/user-attachments/assets/ef5075e3-762e-4225-b178-162603cda51e" width="300"><br>
  <sub>Home Page</sub>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/85da23c9-7d78-45d2-ad0d-24ccd9b1614c" width="300"><br>
  <sub>Analysis Page</sub>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c4072bd7-5e4f-42b9-ab32-90f879ccb542" width="300"><br>
  <sub>Message Status Page</sub>
</p>

</details>

## Project structure

```
GraphMarks/
├── app.py              # Main Flask application
├── df_manager.py       # Database operations
├── analysis_manager.py # Graph generation and analysis
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .gitignore         # Git ignore rules
├── templates/         # HTML templates
│   ├── index.html     # Main form page
│   ├── sent.html      # Success page
│   └── view.html      # Data visualization page
├── static/            # Generated graphs
│   ├── marks_ADV.png
│   ├── marks_JEM.png
│   ├── marks_PAT.png
│   ├── marks_line.png
│   └── markslogo.png
└── data.db           # SQLite database (auto-created)
```

## Future Improvements

This project was primarily built as a **quick automation tool** to solve a specific workflow problem. While it currently fulfills its intended purpose, several improvements could be explored if the project were expanded further:

- **Improved local setup support**  
  Streamline the installation process and eliminate manual debugging steps, particularly around secret files and environment configuration.

- **More robust error handling**  
  Add clearer logging and exception handling for Telegram API interactions and database operations.

- **Configuration management**  
  Replace manual environment variable setup with a more structured configuration system.

- **Better deployment automation**  
  Introduce CI/CD pipelines for automated testing and deployment validation.

- **User interface improvements**  
  Expand the UI to make the tool easier to use without manual configuration.

For now, the project remains a **lightweight automation utility**, and further development would depend on future use cases or feature requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
