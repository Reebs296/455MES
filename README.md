# Manufacturing Execution System (MES)

## Overview

The **Manufacturing Execution System (MES)** is a user-friendly application developed using PyQt5. Its purpose is to streamline manufacturing processes with the following key features:

1. **Login Authentication** – Secure, role-based access for operators and administrators.
2. **Order Management** – Submit, manage, and track manufacturing orders.
3. **Real-Time Monitoring** – Displays machine data and order progress.

---

## Features

### **1. Login Authentication**
- Role-based access for Operators and Admins.
- Credentials are securely stored and verified.

### **2. Order Management**
- Operators can submit and track production orders.
- Admins have additional rights to view and manage all orders.

### **3. Real-Time Monitoring**
- Displays live data of the machine’s operational status.
- Tracks the progress of orders in real time.

---

## Technical Details

The application is built using:
- **Frontend:** PyQt5 (for UI)
- **Backend:** SQLite3 database for storing user credentials, order details, and machine data.
- **Languages:** Python (Primary)

---

## Project Structure (WILL BE UPDATED)

```plaintext
MES/
├── main.py          # Main application entry point
├── ui/              # UI-related files
│   ├── login.ui     # Login interface
│   ├── dashboard.ui # Main dashboard
├── db/              # Database-related files
│   ├── init_db.py   # Database initialization script
│   ├── database.db  # SQLite3 database file
├── modules/         # Custom modules
│   ├── auth.py      # Authentication logic
│   ├── orders.py    # Order management logic
│   ├── monitoring.py# Real-time monitoring logic
└── README.md        # Project documentation (this file)
```

## Learning Objectives

This project allows us to:
1. Gain hands-on experience in **factory-scale planning and control**.
2. Build on the concepts from **Level 0 (Field)**, **Level 1 (Control)**, and **Level 2 (Supervisory)** systems.
3. Implement core MES functionalities, addressing **Level 3 (Planning)** requirements.
4. Apply concepts from the **MESA** and **ISA S 95** standards for MES design.

## Key Features

1. **Production Functions**: Includes work order generation, scheduling, and calculating OEE.
2. **Communication Layer**: Allows real-time data exchange between machines and the MES.
3. **Databases**: A relational database will store machine data, production times, material consumption, and more.
4. **User Interfaces**: We will design a simple, web-based data visualization and control interface.
5. **Data Analytics**: Built-in analytics for measuring production efficiency, quality, and performance metrics.

## Technology Stack

- **Python**: For backend scripting and system logic.
- **SQL**: Database management for production data.
- **PyQt5 Designer**: Frontend for the MES user interface.
- **Tia Portal**: This is for communication between MES and ERP systems (using standard protocols such as OPC UA and web services for data exchange).

## Installation

Follow these steps to set up the project on your local machine. Ensure Git and Python are installed before proceeding.

### Step 1: Verify the Directory for Cloning

Before cloning the repository, ensure you are in the correct directory on your computer where you want to download the project files.

1. Open a terminal or command prompt.
2. Navigate to the directory where you want to clone the repository using the `cd` (change directory) command:

   ```bash
   cd path/to/your/desired/folder
   ```

To check your current directory:

   ```bash
   pwd   # for Mac/Linux
   ```
or

   ```bash
   cd    # for Windows
   ```

## Step 2: Clone the Repository

Once you are in the desired directory, clone the repository by running the following command:

   ```bash
   git clone https://github.com/Reebs296/455MES.git
   ```

This will download the project files into a folder named after the repository.

## Step 3: Navigate to the Project Directory

After cloning the repository, navigate to the project directory:

   ```bash
   cd MES_Project
   ```

## Step 4: Install Dependencies

To install the required dependencies, make sure you are in the project directory and run:

   ```bash
   pip install -r requirements.txt
   ```

## Step 5: Run the MES Server

Once the dependencies are installed, start the MES application by running:

   ```bash
   run TestRun.py
   ```
