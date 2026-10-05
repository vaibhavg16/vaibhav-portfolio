# 🚀 Personal Portfolio & Automated CI/CD Pipeline

A modern, responsive portfolio website showcasing my experience as a **Linux Administrator & DevOps Engineer**. This project includes both automated deployment to **GitHub Pages** and a self-hosted CI/CD pipeline using **GitHub Actions** and an **Nginx** web server running on WSL.

---

## 🌟 Features

* **Responsive Design:** Dark/light mode theme toggle, clean UI, interactive modal certification view, and PDF resume viewer.
* **Dual Deployment Pipeline:**
  * **GitHub Pages:** Automatic build and deployment on push to `main`.
  * **Self-Hosted Runner:** Automated local deployment to `/var/www/html/` via a custom GitHub Actions self-hosted runner.
* **Modular Workflows:** Separated GitHub Actions workflows for checking out code, building, testing, and deploying.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript
* **Web Server:** Nginx (Linux / WSL2)
* **CI/CD & DevOps:** GitHub Actions, Self-Hosted Runners, Bash Scripting, Git
* **Hosting:** GitHub Pages & Local Nginx

---

## 📁 Repository Structure

```text
.
├── .github/
│   └── workflows/
│       ├── build.yml    # Build step workflow
│       ├── cicd.yml     # Main workflow orchestration
│       ├── code.yml     # Checkout step workflow
│       ├── deploy.yml   # Deployment step workflow (Nginx)
│       └── test.yml     # Testing step workflow
├── index.html           # Portfolio source code
└── resume.pdf           # Embedded PDF resume
# Quick change for YOLO badge
