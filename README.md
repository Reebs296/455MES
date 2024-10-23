# Manufacturing Execution System (MES) Project

## Overview

This project is part of the **Factory Planning (MANF 455)** course. The primary objective is to design and implement a **Manufacturing Execution System (MES)** that integrates with factory-level systems, providing seamless communication between production facilities and enterprise systems. Through this project, we will apply concepts from Level 0 to Level 3 of factory control and planning.

## Project Purpose

In modern manufacturing, companies face challenges like networking, rapid technological changes, and market fluctuations. An MES addresses these by connecting various production and business processes, ensuring efficiency, quality control, and real-time data acquisition. Our MES will focus on:

- **Production functions**: Scheduling, order generation, downtime tracking.
- **Communication layer**: Data transmission between factory-level devices and ERP systems.
- **Databases**: Storing and retrieving production data.
- **User interfaces**: For monitoring and controlling production.
- **Data analytics**: Measuring key performance indicators (KPIs) like Overall Equipment Efficiency (OEE).

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
- **HTML/CSS/JavaScript**: Frontend for the MES user interface.
- **Web services**: For communication between MES and ERP systems (using standard protocols such as OPC UA and web services for data exchange).

## Team Roles

- **Frontend Development**: Responsible for building the user interface.
- **Backend Development**: Implements production functions and communication layers.
- **Database Management**: Designs and manages the relational database.
- **System Integration**: Ensures smooth communication between the MES and production equipment.

## Project Milestones

1. **Week 1-2**: Define functional specifications and outline system architecture.
2. **Week 3-4**: Develop core MES production features and communication layers.
3. **Week 5-6**: Implement database and integrate with frontend interfaces.
4. **Week 7-8**: Add advanced functionality following the MESA model, including analytics.
5. **Week 9-10**: Test the system, analyze performance, and make necessary improvements.

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
   python app.py
   ```

## Step 6: Access the MES Interface

Once the server is running, open your web browser and navigate to the following URL to access the MES system:

   ```bash
   http://localhost:5000
   ```
