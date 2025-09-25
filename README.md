# **Deskbird Hybrid Workplace Intelligence**
This project demonstrates an end-to-end Data Analytics and Business Intelligence workflow for a modern SaaS company (Deskbird). It is designed to solve the problem of fragmented sales and usage data, providing a single source of truth for strategic decision-making and automated reporting.



## **Problem Statement**
Sales and product usage data are typically isolated (CRM, web events, product logs), making it impossible to answer high-value questions like, "Which company size is most likely to convert, and how do we optimize our office utilization product?" This project creates a robust data pipeline to unify these disparate sources, establish data integrity, and provide predictive and prescriptive insights for revenue growth and client advisory services.



## **Architecture & Workflow**
The pipeline follows a modern ELT (Extract, Load, Transform) workflow using the dbt (Data Build Tool) framework to manage all transformations, ensuring governance and modularity.

- **Extract & Load (EL):** Raw, synthetic sales, CRM, web event, and product usage data are generated using Python (Pandas/Faker) and loaded into MySQL (acting as the Data Warehouse).

- **Transform (T - dbt):** Transformations are executed using dbt and SQL. Models are built in stages:

    - **Staging:** Isolates and cleans raw source tables.
    
    - **Intermediate:** Joins core dimensions (Users, Companies) early to resolve ambiguity and create clean relationships (e.g., int_user_company_map).
    
    - **Marts:** Creates final analytical tables (growth_funnel_mart, office_utilization_mart) ready for analysis.

- **Analyze & Visualize (Streamlit):** The cleaned data marts are connected to a Python analytics layer for advanced modeling and an interactive dashboard built with Streamlit.



## **Technologies Used**
- **dbt (Data Build Tool):** The core framework for defining, testing, and executing modular SQL transformations (the 'T' in ELT).

- **MySQL:** Used as the persistent data warehouse for both raw and transformed data.

- **Python:** Used for generating synthetic raw data, statistical analysis (Propensity Modeling), and building the final application.

- **Streamlit:** Used to create the interactive, executive-facing dashboard that presents all key insights and recommendations.

- **Pandas/Statsmodels:** Key Python libraries for data manipulation and building the Logistic Regression propensity model.



## Key Insights & Analytics
The unified data marts enable highly strategic analytics that drive direct revenue action:

- **Sales Propensity:** A Logistic Regression Model revealed that Enterprise leads have the highest statistical propensity to convert, while Mid-Market leads, despite their high Average Deal Value, have a 72% lower chance of closing.

- **Funnel Optimization:** Analysis identified the Mid-Market funnel as the most critical bottleneck due to its high value ($10,636 ADV) and low conversion rate, demanding immediate sales process intervention.

- **Product Utilization:** Data revealed highly non-traditional client usage (e.g., Enterprise weekend utilization and high SMB demand for meeting rooms), enabling the creation of a new Utilization Advisory Service as a product differentiator.

- **A/B Testing:** Statistical analysis confirmed that a new free trial offer generated a 37.5% statistically significant uplift in conversions.



## **Key Visualization & Application**
The final output is an interactive analytics application built using Streamlit, designed for executive stakeholders. It provides a real-time, consolidated view of revenue performance, sales pipeline health, and customer utilization patterns.
