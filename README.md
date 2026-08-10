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
*   **On-the-Fly Image Processing:** User avatars are processed server-side using `Pillow (PIL)`. Images are automatically converted to standard RGB/JPEG formats, resized, and compressed to optimize bandwidth and cloud storage before database commit.
*   **Robust Error Handling:** Implements SQLAlchemy session rollbacks (`db.session.rollback()`) and transaction management to prevent server crashes during concurrent database operations or connection timeouts.

---

## ✨ Application Features & Development Workflow

Here is a deep dive into the core features and how the application operates from a user's perspective.

### 1. Secure Authentication & Onboarding
The entry point features a modern auth UI with traditional email/password registration (secured via `Werkzeug` password hashing) alongside **Google OAuth 2.0**.
*   *Tech Highlight:* OAuth integration via `Authlib`, ensuring secure, token-based social logins without storing sensitive third-party credentials.

<div align="center">
  <img src="assets/loginpage.png" alt="Login Page" width="700"/>
  <br>
  <em>Fig 1: Secure Login Portal with Google OAuth Integration</em>
</div>

### 2. Interactive Dashboard & Real-Time Analytics
A comprehensive dashboard provides users with an immediate overview of their productivity. It includes dynamic charts that render data client-side based on database queries.
*   *Tech Highlight:* Uses `Chart.js` for rendering responsive Doughnut (Status) and Bar (Priority) charts. The UI supports persistent **Dark/Light Mode** utilizing `localStorage`.

<div align="center">
  <img src="assets/dashboard2.1.png" alt="Dashboard Analytics" width="700"/>
  <br>
  <em>Fig 2: Light Mode Dashboard showing dynamic Chart.js analytics, quick filters, and progress tracking.</em>
</div>

### 3. Agile Kanban Board (Drag-and-Drop)
Task state management is handled through a highly interactive Kanban interface. Users can seamlessly move tasks between 'Pending', 'In Progress', and 'Completed' states.
*   *Tech Highlight:* Implemented using `SortableJS` for smooth DOM manipulation. State changes trigger asynchronous `fetch` API calls to the Flask backend to update PostgreSQL in real-time, accompanied by `SweetAlert2` toast notifications.

<div align="center">
  <img src="assets/dashboard2.2.png" alt="Kanban Board" width="700"/>
  <br>
  <em>Fig 3: Active Kanban Board with color-coded priority badges and drag-and-drop capability.</em>
</div>

### 4. Dynamic Calendar Integration
For deadline-focused users, tasks are mapped onto a full-month interactive calendar.
*   *Tech Highlight:* Powered by `FullCalendar.io`. Tasks are fetched dynamically via an internal JSON API endpoint (`/api/tasks`). Overdue tasks are automatically flagged in red through backend logic.

<div align="center">
  <img src="assets/calender add and edit task.png" alt="Calendar View" width="700"/>
  <br>
  <em>Fig 4: Dark Mode FullCalendar view mapping tasks to their specific due dates.</em>
</div>

### 5. Advanced Profile Management & UI Modals
Users can manage their personal data and avatars. The UI employs sleek modals and hover states for an intuitive experience.
*   *Tech Highlight:* Clicking the avatar triggers a `SweetAlert2` modal intercepting standard form behavior, allowing users to choose between uploading a new file or triggering a backend deletion route.

<div align="center">
  <img src="assets/profile1.1.png" alt="Profile Upload Modal" width="400"/> 
  <img src="assets/profile1.2.png" alt="Updated Profile" width="400"/>
  <br>
  <em>Fig 5: Interactive Avatar update flow using SweetAlert2 and Python PIL for backend processing.</em>
</div>

### 6. Seamless Task Editing & Edge-Case Handling
Dedicated views for task modification ensure data integrity.
*   *Tech Highlight:* The application utilizes URL query parameters (e.g., `?next=/dashboard#kanban-board-section`) to redirect users precisely back to their previous scroll position after an update.

<div align="center">
  <img src="assets/edit task.png" alt="Edit Task Form" width="700"/>
  <br>
  <em>Fig 6: Clean and focused Task Editing interface.</em>
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

### 1. Clone the Repository
```bash
git clone [https://github.com/kushal267/Dockerized_Web_App.git](https://github.com/kushal267/Dockerized_Web_App.git)
cd Dockerized_Web_App
