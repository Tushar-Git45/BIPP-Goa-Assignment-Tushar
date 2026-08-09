## FPS Sale Transaction Data Scraper \& Consolidation



### Project Overview



###### This project was developed as part of the BIPP Assignment.



The objective is to collect the FPS (Fair Price Shop) level sale transaction data for **Goa** from the official IMPDS Sale Portal for **March 2026 and April 2026,** and transformed the scraped data into a clean, consolidated dataset suitable for analysis.



###### The project consists of two independent scripts:



* **get\_raw\_data.py** - Scrapes FPS-level transaction data from the IMPDS portal.
* **consolidate\_data.py** - Cleans, transforms and consolidates all scraped records into one analysis-ready dataset.





#### **Section 1 - Data Scraping**



1. ##### **Objective**



Scrapes FPS-level sale transaction data from the IMPDS Sale Portal by navigating through the following hierarchy:



Year **->** Month **->** State(GOA) **->** District **->** Fair Price Shop(FPS)



For every FPS, the scraper collects:



* Four Summary Card Values
* Number of Transaction table
* Number of Transacted Ration Card table
* Distributed Quantity table
* Expanded Coarse Grains commodities



The scraper repeats this process for:



* March 2026
* April 2026
* North Goa
* South Goa
* Every available FPS





##### **2. Scraping Approach**



The scraper performs the following steps:



1. Opens the IMPDS Sale Portal.
2. Selects the required year and month.
3. Opens the Goa state page.
4. Iterates through both districts.
5. Opens the FPS list for each district.
6. Visits every FPS.
7. Extracts:
* Summary Cards
* Number of Transactions
* Number of Transacted Ration Cards
* Distributed Quantity Table

8\. Expands the Coarse Grains section and extracts each commodity individually.

9\. Save each FPS as an individual raw data file





##### **3. Error Handling**



The scraper includes:



* Retry mechanism for temporary failures
* Exception Handling
* Progress logging
* Skipping invalid FPS records without stopping the entire execution.



This allows interrupted scraping jobs to continue without losing previously collected data.



##### **4. Raw Data Structure**



data/

|- raw/

|  |- 2026-03/

|  |  |- north\_goa/

|  |  |- south\_goa/

|  |- 2026-04/

|     |- north\_goa/

|     |- south\_goa/

|

|-- processed/



Each FPS file contains:

* Year
* Month
* State
* District
* FPS ID
* FPS Name
* Summary Cards
* Number of Transactions Table
* Number of Transacted Ration Card Table
* Distributed Quantity Table





#### **Section 2 - Data Consolidation \& Transformation**



1. #### Objective

&#x20;   

The objective of Section 2 is to consolidate the FPS-level sale transaction data collected during the scraping process and transform it into a clean, structured, and analysis-ready dataset.



The data collected for different districts, FPSs, and months is combined into a single dataset while maintaining the required information such as month, district, FPS ID, FPS name, and transaction details.



#### 2\. Approach



The following approach was used for data consolidation and transformation:



**Raw Scraped Files → Data Loading → Data Consolidation → Data Cleaning → Data Transformation → Validation → Final Dataset**

#### 

#### 3\. Data Loading



The scraped files generated during Section 1 are loaded using the Pandas library.



The files are read from the raw data directory and stored as Pandas DataFrames for further processing.



The data includes records from:

* Goa
* North Goa
* South Goa
* March 2026
* April 2026
* Multiple FPS locations



#### 4\. Data Consolidation



Since the data is collected separately for different FPSs and months, the individual datasets are combined into a single DataFrame.



Pandas concat() is used to append the datasets while maintaining a consistent column structure.



The following information is retained during consolidation:

* Month
* Year
* State
* District
* FPS ID
* FPS Name
* Sale/Transaction details



This creates a unified dataset containing all available records.



#### 5\. Data Cleaning



After consolidation, the dataset is checked for data quality issues.



###### **Missing Values**



Missing or blank values are identified using Pandas.



Depending on the column, missing values are either:



* Retained when they represent unavailable information, or
* Removed/replaced when appropriate.



###### **Duplicate Records**



Duplicate records are identified using drop\_duplicates().



This ensures that the same transaction is not unnecessarily repeated in the final dataset.



###### **Empty Records**



Completely empty rows and irrelevant records are removed from the dataset.



#### 6\. Data Transformation



The consolidated dataset is transformed into a standardized structure.



###### **Column Standardization**



Column names are standardized for consistency and easier analysis.



For example:



* Spaces are removed or replaced with underscores.
* Column names are converted into a consistent naming format.
* Unnecessary columns are removed where applicable.



###### **Data Type Conversion**



Columns are converted into appropriate data types.



For example:



* Transaction quantities → Numeric
* Transaction amounts → Numeric
* Dates → Date/Datetime
* FPS IDs → String
* FPS Names → String



This ensures that numerical and date-based analysis can be performed correctly.



#### 7\. Adding Metadata



Additional metadata is maintained or added to each record wherever required.



Important metadata includes:



* State
* District
* Month
* Year
* FPS ID
* FPS Name



This allows the final dataset to be filtered and analyzed by location, FPS, and month.



#### 8\. Data Validation



After transformation, the dataset is validated to ensure data consistency.



The following checks are performed:



* Number of rows before and after cleaning
* Number of columns
* Missing values
* Duplicate records
* Correct month and year
* Correct district names
* Correct FPS IDs
* Correct data types
* Presence of required columns



Basic summary statistics and unique-value checks are also performed where applicable.



#### 9\. Final Dataset



After completing the consolidation and transformation process, the cleaned dataset is saved as the final output.



The final dataset is structured so that each row represents the corresponding FPS-level sale transaction information.



The dataset can be used for further:



* Data analysis
* Visualization
* Reporting
* Business insights



#### 10\. Tools Used



###### **Python**



Used as the primary programming language for data processing.



###### **Pandas**



Used for:



* Reading data
* Combining datasets
* Cleaning data
* Handling missing values
* Removing duplicates
* Data transformation
* Exporting the final dataset



###### **NumPy**



Used where required for numerical operations and handling missing values.

###### 

###### **Excel / CSV**



Used as input/output formats for storing and reviewing the processed data.



#### 11\. Processing Flow



**Raw Scraped Data**

&#x20;      **↓**

**Load Individual Files**

&#x20;      **↓**

**Combine All Files**

&#x20;      **↓**

**Check Column Structure**

&#x20;      **↓**

**Handle Missing Values**

&#x20;      **↓**

**Remove Duplicates**

&#x20;      **↓**

**Standardize Columns**

&#x20;      **↓**

**Convert Data Types**

&#x20;      **↓**

**Validate Dataset**

&#x20;      **↓**

**Export Final Dataset**



#### 12\. Expected Output



The final output is a consolidated and cleaned dataset containing FPS-level sale transaction information for Goa for:



* March 2026
* April 2026



covering the relevant districts and FPS records collected during the scraping process.



The final dataset is stored in CSV/Excel format and is ready for further analysis.



