# 🚢 SIGenie - Shipping Intelligence Genie 🧞‍♂️

SIGenie is an early access version (v0.04-5368) of a comprehensive shipping document management system. It provides a user-friendly web interface for managing Bookings, Shipping Instructions, and Bills of Lading.

## ✨ Key Features

- 🎫 Booking (BKG) management
- 📄 Shipping Instructions (SI) editing
- 🚢 Bill of Lading (BL) viewing
- 🔍 Shipping Instruction search (including vector search)
- 💾 MongoDB integrated data storage

## 🛠 Prerequisites

- Python 3.11+
- MongoDB
- OpenAI API key
- Poetry (for dependency management)

## 🚀 Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/sigenie.git
   cd sigenie
   ```

2. Install Poetry (if not already installed):

   ```
   pip install poetry
   ```

3. Install project dependencies:

   ```
   poetry install
   ```

4. Set up the `.env` file in the project root:
   ```
   MONGODB_URI=your_mongodb_connection_string
   MONGODB_DB_NAME=your_database_name
   OPENAI_API_KEY=your_openai_api_key
   ```

## 🏃‍♂️ Usage

1. Activate the poetry environment:

   ```
   poetry shell
   ```

2. Run the Streamlit app:

   ```
   streamlit run main.py
   ```

3. Navigate to the provided URL in your web browser (usually `http://localhost:8501`)

4. Use the sidebar to select the desired document type (Booking, Shipping Instructions, Bill of Lading, Shipping Instruction Search)

## 📁 Project Structure

```
sigenie/
│
├── app/
│ ├── init.py
│ ├── json_bkg.py 🎫 (Booking handling)
│ ├── json_si.py 📄 (Shipping Instructions handling)
│ ├── json_bl.py 🚢 (Bill of Lading handling)
│ ├──  search_si.py 🔍 (Search functionality)
│ └── search_compliance.py 🔍 (Search company policy)
│
├── prompts/
│ └──compliance_rag_prompt.yaml 💬 (System prompt for rag)
│
├── utils/
│ ├── init.py
│ └── helpers.py 🛠️ (Utility functions)
│
├── vector/
│ └── si_faiss_index/ 🧠 (Shipping nstruction vector database)
│
├── img/
│ └── containergenie.png 🖼️ (Logo image)
│
├── fonts/
│ └── Freesentation.ttf 🔠 (Font)
│
├── main.py 🎭 (Main application entry point)
├── db.py 💾 (Database operations)
├── .env 🔐 (Environment variables)
├── .gitignore
├── pyproject.toml 📦 (Poetry configuration)
├── poetry.lock 🔒 (Poetry lock file)
└── README.md 📖 (This file)
```

## Directory Descriptions

### bkg/ and si/

These directories contain JSON files for Booking and Shipping Instruction documents, respectively. Each file represents a single document and follows a specific structure. The application reads these files to populate the database and display information.

## Contributing

This is an early access version. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements

- Freesentation font
- Streamlit for the web application framework
- MongoDB for database management

## Version History

- v0.01 (2024-09-15): Initial early access release

  - Basic functionality for managing Bookings, Shipping Instructions, and Bills of Lading
  - MongoDB integration
  - Custom font implementation

- v0.02 (2024-09-25): Current early access version

  - Improved user interface
  - Added support for special cargo information in Shipping Instructions
  - Enhanced error handling and data validation
  - Performance optimizations for large datasets
  - Implemented Poetry for dependency management

- v0.03 (2024-09-29):

  - dataset 3263
  - draft watermark
  - dataset 3518 (2024-10-01)
  - dataset 3782 (2024-10-03)
  - dataset 4115 (2024-10-04)
  - dataset 4308 (2024-10-07)
  - dataset 4476 (2024-10-08)
  - dataset 4654 (2024-10-09)
  - dataset 4853 (2024-10-10)
  - dataset 5009 (2024-10-11)

- v0.04 (2024-10-12)

  - Shipping Instruction vector search in MongoDB
  - Restructue folder
  - dataset 5372 (2024-10-13)

- v0.05 (2024-10-13)

  - Company policy search
  - dataset 5570 (2024-10-14)

- v0.06 (2024-10-14)
  - Doc splitter with customized function in compliance search
  - Reranker in compliance search
  - dataset 5573 (2024-10-14)
  - dataset 5858 (2024-10-15)
  - dataset 6036 (2024-10-16)

---

Copyright (c) 2024 Tongyang Systems.
All rights reserved. This project and its source code are proprietary and confidential. Unauthorized copying, modification, distribution, or use of this project, via any medium, is strictly prohibited without the express written permission of the copyright holder.
