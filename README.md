# Jeffrey Crum - Python Portfolio

A modern web portfolio built with Streamlit to showcase Python projects and applications.

## Overview

This portfolio website displays a curated collection of Python projects, from web applications to data analysis tools. The site features a clean, responsive design with project descriptions, source code links, and visual previews.

## Features

- **Responsive Design**: Two-column layout that adapts to different screen sizes
- **Project Showcase**: Dynamic display of projects loaded from CSV data
- **Visual Portfolio**: Image previews for each project
- **Direct Links**: Quick access to source code repositories
- **Professional Profile**: Personal introduction and contact information

## Tech Stack

- **Framework**: Streamlit
- **Data Handling**: Pandas
- **Language**: Python
- **Styling**: Streamlit's built-in components

## Project Categories

The portfolio includes projects across various domains:
- Web Applications (Todo App, Restaurant Menu, Online Store)
- Data Analysis & Visualization (Weather Forecast, Internet Speed Analysis)
- Automation Tools (Download Cleaner, Tour Scraper, Motion Detector)
- APIs & Chatbots (Weather API, Helper Chatbot)
- Desktop Applications (Student Management System)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd web-portfolio
```

2. Install dependencies:
```bash
pip install streamlit pandas
```

3. Run the application:
```bash
streamlit run main.py
```

## Project Structure

```
web-portfolio/
├── main.py           # Main Streamlit application
├── data.csv          # Project data (titles, descriptions, URLs, images)
├── images/           # Project screenshots and profile photo
│   ├── IMG_2797.JPG  # Profile photo
│   └── *.png         # Project screenshots (1-20.png)
└── README.md         # This file
```

## Data Format

Projects are stored in `data.csv` with the following structure:
- `title`: Project name
- `description`: Brief project description
- `url`: Link to source code
- `image`: Screenshot filename

## Customization

To add new projects:
1. Add project details to `data.csv`
2. Place project screenshot in `images/` folder
3. The app will automatically display the new project

## Live Demo

Visit the deployed application: [Your Portfolio URL]

## Contact

- **LinkedIn**: [Your LinkedIn]
- **GitHub**: [Your GitHub]
- **Email**: [Your Email]

---

Built with ❤️ using Python and Streamlit
