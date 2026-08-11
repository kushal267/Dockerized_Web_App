# 🚀 Smart Task Manager (Cloud-Native Web App)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Serverless-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?logo=render)

A production-ready, highly scalable Task Management Platform engineered with a cloud-first architecture. It integrates secure Google OAuth authentication, interactive Kanban boards, advanced data analytics, and is fully containerized for seamless CI/CD pipeline deployments.

**[🔴 Live Demo: Click Here to View Application](https://smart-task-manager-yhb8.onrender.com)** 

---

## ☁️ Cloud Architecture & DevOps (The Backend Engine)

This application is built to be robust, stateless, and optimized for cloud environments.

*   **Serverless Database (Neon.tech):** Utilizes a managed, serverless PostgreSQL database ensuring high availability and seamless connection pooling.
*   **Containerization (Docker):** Fully containerized with a custom `Dockerfile`, ensuring 100% environment consistency across development, testing, and production (Render).
*   **Ephemeral Storage Handling:** Engineered to work flawlessly on stateless cloud instances. For instance, the **Excel Export** feature utilizes `Pandas` and `io.BytesIO` to generate `.xlsx` files entirely in RAM (in-memory buffer), preventing data leaks and bypassing the need for persistent disk storage.
*   **On-the-Fly Image Processing:** User profile image are processed server-side using `Pillow (PIL)`. Images are automatically converted to standard RGB/JPEG formats, resized, and compressed to optimize bandwidth and cloud storage before database commit.
*   **Robust Error Handling:** Implements SQLAlchemy session rollbacks (`db.session.rollback()`) and transaction management to prevent server crashes during concurrent database operations or connection timeouts.

---
## 🚀 Quick Feature Summary
*   ** Responsive UI:** Fully responsive interface for mobile and desktop screens.
*   ** Authentication:** User registration and secure login (including Google OAuth).
*   ** Task Management:** Create, edit, and delete tasks seamlessly.
*   ** Priority Levels and Status Tracking:** Categorize tasks into Low, Medium, or High priorities.Move tasks through Pending, In Progress, and Completed states.
*   ** Search & Filters:** Instantly find tasks using search and quick filters.
*   ** Calendar View and Task Management:** Calendar-based task visualization for deadline management and Add task directly with calender 
*   ** Analytics:** Dashboard statistics and interactive task analytics (Chart.js).
*   ** Progress Tracking:** Visual completion progress tracking.
*   ** Profile Management:** User profile customization, Profile-picture upload.
*   ** Theme Toggle:** Persistent Light and Dark mode preferences.
*   ** Data Export:** One-click export of tasks to Excel (`.xlsx`).
*   ** Cloud Hosted:** Public deployment on Render with a Neon Serverless Database.

## ✨ Deep Dive: Features & Workflow

Here is a deep dive into the core features and how the application operates from a user's perspective.

### 1. Secure Authentication & Onboarding
The entry point features a modern auth UI with traditional email/password registration (secured via `Werkzeug` password hashing) alongside **Google OAuth 2.0**.
*   *Tech Highlight:* OAuth integration via `Authlib`, ensuring secure, token-based social logins without storing sensitive third-party credentials.

<div align="center">
  <img src="screenshots/loginpage.png" alt="Login Page" width="700"/>
  <br>
  <em>Fig 1: Secure Login Portal with Google OAuth Integration</em>
</div>

### 2. Interactive Dashboard & Real-Time Analytics
A comprehensive dashboard provides users with an immediate overview of their productivity. It includes dynamic charts that render data client-side based on database queries.
*   *Tech Highlight:* Uses `Chart.js` for rendering responsive Doughnut (Status) and Bar (Priority) charts. The UI supports persistent **Dark/Light Mode** utilizing `localStorage`.

<div align="center">
  <img src="screenshots/dashboard2.1.png" alt="Dashboard Analytics" width="700"/>
  <img src="screenshots/search quick filter.png"  width="700"/>
  <br>
  <em>Fig 2: Light Mode Dashboard showing dynamic Chart.js analytics, quick filters, and progress tracking.</em>
</div>

### 3. Agile Kanban Board (Drag-and-Drop)
Task state management is handled through a highly interactive Kanban interface. Users can seamlessly move tasks between 'Pending', 'In Progress', and 'Completed' states.
*   *Tech Highlight:* Implemented using `SortableJS` for smooth DOM manipulation. State changes trigger asynchronous `fetch` API calls to the Flask backend to update PostgreSQL in real-time, accompanied by `SweetAlert2` toast notifications.

<div align="center">
  <img src="screenshots/dashboard2.2.png" alt="Kanban Board" width="700"/>
  <br>
  <em>Fig 3: Active Kanban Board with color-coded priority badges and drag-and-drop capability.</em>
</div>

### 6. Seamless Task Editing & Edge-Case Handling
Dedicated views for task modification ensure data integrity.
*   *Tech Highlight:* The application utilizes URL query parameters (e.g., `?next=/dashboard#kanban-board-section`) to redirect users precisely back to their previous scroll position after an update.

<div align="center">
  <img src="screenshots/edit task.png" alt="Edit Task Form" width="700"/>
  <br>
  <em>Fig 6: Clean and focused Task Editing interface.</em>
</div>

### 4. Dynamic Calendar Integration
For deadline-focused users, tasks are mapped onto a full-month interactive calendar.
*   *Tech Highlight:* Powered by `FullCalendar.io`. Tasks are fetched dynamically via an internal JSON API endpoint (`/api/tasks`). Overdue tasks are automatically flagged in red through backend logic.
User can Add new task by clicking any date and Edit previous task from Calendar
<div align="center">
  <img src="screenshots/calender add and edit task.png" alt="Calendar View" width="700"/>
  
  <br>
  <em>Fig 4: FullCalendar view mapping tasks to their specific due dates.</em>
</div>

### 5. Advanced Profile Management & UI Modals
Users can manage their personal data and profile picture. The UI employs sleek modals and hover states for an intuitive experience.
*   *Tech Highlight:* Clicking the pencil button on profile triggers a `SweetAlert2` modal intercepting standard form behavior, allowing users to choose between uploading a new file or triggering a backend deletion route.

<div align="center">
  <img src="screenshots/profile1.1.png" alt="Profile Upload Modal" width="400"/> 
  <img src="screenshots/profile1.2.png" alt="Updated Profile" width="400"/>
  <br>
  <em>Fig 5: Interactive profile picture update flow using SweetAlert2 and Python PIL for backend processing.</em>
</div>


---

## 🛠️ Comprehensive Tech Stack

**Frontend Layer:**
*   HTML5, CSS3, Bootstrap 5
*   Vanilla JavaScript (ES6+)
*   **Libraries:** Chart.js (Analytics), SortableJS (Drag-and-Drop), SweetAlert2 (Popups), FullCalendar (Scheduling)

**Backend Layer (Microframework):**
*   **Python 3.9+**
*   **Flask:** Core application routing and session management.
*   **Flask-SQLAlchemy:** ORM for database queries and schema management.
*   **Pandas & OpenPyXL:** For generating complex Excel data exports.
*   **Pillow (PIL):** Server-side image rendering and optimization.
*   **Werkzeug:** Cryptographic password hashing.

**Database & Cloud Infrastructure:**
*   **Neon.tech:** Serverless PostgreSQL Database.
*   **Docker:** Application containerization.
*   **Render:** Cloud PaaS for automated CI/CD deployment.
*   **Google Cloud Console:** Identity and Access Management (OAuth 2.0 API).

---

## ⚙️ Local Development Setup

Follow these steps to run the containerized application on your local machine.

### Prerequisites
*   Docker & Docker Compose installed.
*   A PostgreSQL Database string (or fallback to SQLite).
*   Google OAuth Client Credentials.

## 1. Clone the Repository
```bash
git clone [https://github.com/kushal267/Dockerized_Web_App.git](https://github.com/kushal267/Dockerized_Web_App.git)
cd Dockerized_Web_App
```
---

## 2. Environment Configuration
Create a `.env` file in the root directory of the project.
Add the following environment variables:
```env
SECRET_KEY=your_highly_secure_random_string
DATABASE_URL=postgresql://user:password@host/dbname
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
```
---

## 3. Run Locally Using Python
This method is recommended for development and debugging.
### Create a Virtual Environment
```bash
python -m venv .venv
```
### Activate the Virtual Environment
```bash
.venv\Scripts\activate
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Start the Flask Application
```bash
python app.py
```
The application will be available at:
```text
http://127.0.0.1:5000
```
---

# 🐳 Run Using Docker
Docker can be used to run the application inside a container.
## Build the Docker Image
```bash
docker build -t smart-task-manager .
```
## Run the Docker Container
```bash
docker run -p 5000:5000 --env-file .env smart-task-manager
```
The application will be available at:
```text
http://localhost:5000
```

---

# 🚀 Production Deployment

The application can be deployed using **Render + Neon PostgreSQL + Docker**.

---

## Step 1: Setup Neon PostgreSQL
1. Create an account on [Neon](https://neon.tech).
2. Create a new PostgreSQL project.
3. Open the database dashboard.
4. Copy the PostgreSQL connection string.
5. Add the connection string to your deployment environment variables.
Example:
```env
DATABASE_URL=postgresql://user:password@host/dbname
```
**Keep the database credentials private.**
---

## Step 2: Configure Google OAuth
1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a Google Cloud project.
3. Configure the OAuth Consent Screen.
4. Create an **OAuth 2.0 Client ID**.
5. Select **Web Application**.
6. Add your production domain to the authorized origins.
7. Add your OAuth callback URL under **Authorized redirect URIs**.
Example:
```text
https://your-app.onrender.com/login/callback
```
Add the generated credentials to your environment variables:
```env
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret
```
---

## Step 3: Deploy on Render
1. Create an account on [Render](https://render.com).
2. Select **New → Web Service**.
3. Connect your GitHub account.
4. Select the `smart-task-manager` repository.
5. Configure the service to use the project's `Dockerfile`.
6. Add the required environment variables.
7. Start the deployment.

Render will build the Docker image and deploy the application.
After successful deployment, Render will provide a public URL similar to:
```text
https://your-app.onrender.com
```

---

# 📄 License

This project is currently provided for **educational, portfolio, and demonstration purposes**.

All rights reserved unless otherwise stated

# 👨‍💻 Developed By

## Kushal Patel
- **GitHub:** [@kushal267](https://github.com/kushal267)
- **LinkedIn:** linkedin.com/in/kushal-patel-5195bb381

---

# ⭐ Support

If you find this project useful or learned something from it, consider giving the repository a ⭐ on GitHub.

**Thank you for checking out Smart Task Manager!**
