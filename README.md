🌍 EarthMender AI

3MTT NextGen Cohort 2026 Project

EarthMender is an AI-assisted environmental monitoring system developed as part of the 3 Million Technical Talent (3MTT) NextGen Cohort 2026 Program.
The project focuses on leveraging digital skills and artificial intelligence to address real-world environmental challenges, particularly improper waste disposal.

🎯 Project Objective

The objective of this project is to design and implement a scalable, user-friendly system that:

Detects waste using artificial intelligence
Enables structured reporting of environmental issues
Provides data-driven insights through visualization
Promotes environmental awareness and education

This aligns with the 3MTT program’s mission of building technical solutions that create societal impact.


🧠 Problem Statement

Improper waste disposal remains a major environmental issue, especially in urban areas. Many communities lack:

* Efficient monitoring systems
* Structured reporting mechanisms
* Data for decision-making
* Public awareness and engagement tools

EarthMender AI addresses these gaps by combining AI detection, user reporting, and analytics into a single platform.


⚙️ System Design & Methodology

The system adopts a modular architecture, ensuring flexibility and scalability. It is divided into five functional components:

* Detection Module: Handles AI-based waste identification from images
* Reporting Module: Captures and stores user-submitted reports
* Mapping Module: Visualizes environmental data geographically
* Dashboard Module: Provides analytical insights
* Education Module: Promotes awareness through interactive content

This design supports independent development, testing, and future upgrades.

---

🔍 Key Features

 # AI-Powered Waste Detection

* Utilizes a trained YOLO model for image-based detection
* Supports both local and cloud-based inference
* Designed for real-world adaptability


# Waste Reporting System

* Allows users to submit reports with descriptions
* Stores structured environmental data
* Provides a foundation for future database integration


# Map-Based Visualization

* Displays reported waste locations
* Enhances situational awareness
* Can be extended to include real-time GPS and heatmaps


# Data Analytics Dashboard

* Summarizes collected data
* Provides insights for monitoring trends
* Supports decision-making processes


# Environmental Education Module

* Interactive quiz system
* Encourages community awareness
* Promotes behavioral change

 🧠 AI Integration Strategy

The AI model (`best.pt`) is integrated using a **flexible deployment approach**:

* Local execution (resource-intensive)
* Cloud-based inference via Google Colab (recommended)
* Modular fallback for low-resource environments

This ensures the system remains **accessible and deployable across varying hardware capabilities**, which is critical in resource-constrained settings.

 🖥️ Tools & Technologies

* Python – Core development language
* Streamlit – User interface framework
* Pandas – Data processing
* Pillow – Image handling
* Requests – API communication
* Ultralytics YOLO – Object detection

 ⚠️ Limitations

* The trained model file is excluded due to size constraints
* Cloud API endpoints are temporary and session-based
* Current map implementation uses placeholder coordinates


🔮 Future Enhancements

* Real-time GPS integration for accurate mapping
* Heatmap visualization of waste density
* Cloud database integration (e.g., Firebase, PostgreSQL)
* Deployment to scalable cloud platforms
* Mobile application development


📌 Impact & Relevance (3MTT Focus)

This project reflects the core goals of the 3MTT NextGen Cohort, including:

* Application of AI and software development skills
* Development of locally relevant solutions
* Promotion of digital innovation for societal impact
* Demonstration of problem-solving and system design capabilities

EarthMender AI showcases how technical knowledge can be applied to solve **environmental and community challenges.


👤 Author

Adeniji Yusuf
Mechanical Engineering Undergraduate
Track: AI/ML 
3MTT NextGen Cohort 2026 Fellow


🌱 Vision

> “Leveraging technology and innovation to build cleaner, smarter, and more sustainable communities.”
