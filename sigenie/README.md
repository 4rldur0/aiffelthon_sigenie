# SIGenie - Shipping Document Management System

SIGenie is an early access version (v0.02) of a comprehensive shipping document management system. It allows users to manage and view Bookings, Shipping Instructions, and Bills of Lading through a user-friendly web interface.

## Features

- Manage Bookings (BKG)
- Edit Shipping Instructions (SI)
- View Bills of Lading (BL)
- MongoDB integration for data storage
- Custom Freesentation font applied throughout the application

## Prerequisites

- Python 3.9+
- MongoDB
- Poetry (for dependency management)

## Installation

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

4. Set up your MongoDB connection by creating a `.env` file in the root directory with the following content:
   ```
   MONGODB_URI=your_mongodb_connection_string
   MONGODB_DB_NAME=your_database_name
   ```

## Usage

1. Activate the virtual environment:
   ```
   poetry shell
   ```

2. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

3. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Use the sidebar to select the document type you want to work with (Booking, Shipping Instructions, or Bill of Lading).

## Project Structure

- `main.py`: The main Streamlit application entry point.
- `json_bkg.py`: Handles Booking (BKG) document operations.
- `json_si.py`: Manages Shipping Instruction (SI) document operations.
- `json_bl.py`: Displays Bill of Lading (BL) documents.
- `search_si.py`: Provides search functionality for Shipping Instructions.
- `search_booking.py`: Provides search functionality for Bookings.
- `fonts/`: Contains the custom Freesentation font.
- `img/`: Stores images used in the application.
- `bkg/`: Directory for storing Booking JSON files.
- `si/`: Directory for storing Shipping Instruction JSON files.


## Directory Descriptions

### bkg/ and si/
These directories contain JSON files for Booking and Shipping Instruction documents, respectively. Each file represents a single document and follows a specific structure. The application reads these files to populate the database and display information.

### bkg_new/ and si_new/
These directories are used for storing new Booking and Shipping Instruction JSON files that are yet to be processed and added to the main directories.

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
---


Copyright (c) 2024 Tongyang Systems.
All rights reserved. This project and its source code are proprietary and confidential. Unauthorized copying, modification, distribution, or use of this project, via any medium, is strictly prohibited without the express written permission of the copyright holder.