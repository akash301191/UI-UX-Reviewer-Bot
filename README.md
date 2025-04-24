# UI/UX Reviewer Bot

UI/UX Reviewer Bot is a smart Streamlit application that helps you analyze user interface screenshots for layout, accessibility, and design quality. Powered by [Agno](https://github.com/agno-agi/agno) and OpenAI's GPT-4o, the bot acts as a digital design critic—offering insightful, structured feedback to improve your app or website’s user experience.

## Folder Structure

```
UI-UX-Reviewer-Bot/
├── ui-ux-reviewer-bot.py
├── README.md
└── requirements.txt
```

- **ui-ux-reviewer-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## Features

- **Screenshot Upload**  
  Upload a UI screenshot of your website or mobile app for automated analysis.

- **Optional Metadata**  
  Specify the platform (Web, Mobile, etc.) and choose focus areas such as layout, visual hierarchy, accessibility, or color contrast.

- **AI-Powered Review**  
  The UI/UX Reviewer Agent examines the screenshot and generates a structured critique based on visual elements, platform context, and best UX practices.

- **Markdown-Based Review Report**  
  The review is presented in clean, sectioned Markdown format including visual assessments, UX observations, improvement suggestions, and a final summary.

- **Downloadable Output**  
  Download your complete review report as a `.md` file for further reference, documentation, or team collaboration.

- **Streamlit UI**  
  Designed with a clean, intuitive layout to keep your workflow simple and efficient.

## Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/UI-UX-Reviewer-Bot.git
   cd UI-UX-Reviewer-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:
   ```bash
   streamlit run ui-ux-reviewer-bot.py
   ```

2. **In your browser**:
   - Enter your OpenAI API key in the sidebar.
   - Upload a screenshot of your UI.
   - Optionally select platform type and review focus areas.
   - Click **🔍 Generate Review**.
   - View and download your personalized design critique.

3. **Download Option**  
   Use the **📥 Download Review Report** button to save your review as a `.md` file.


## Code Overview

- **`render_uiux_review_input()`**: Collects the uploaded screenshot and optional review preferences.
- **`render_sidebar()`**: Allows users to enter and store their OpenAI API key.
- **`generate_uiux_review()`**:  
  - Passes the uploaded screenshot and inputs to the `UI/UX Reviewer Agent`.  
  - Generates a well-structured Markdown report based on the visual content and focus.
- **`main()`**: Manages page layout, user interactions, agent calls, and output display.

## Contributions

Contributions are welcome! Feel free to fork the repo, suggest new features, report bugs, or open a pull request. Make sure your changes are clean, meaningful, and aligned with the purpose of this bot.