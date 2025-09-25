# AI Lead Scoring Service 🚀

This project is an intelligent backend service designed to qualify and score sales leads. It accepts product information and a list of prospects (as a CSV), then uses a combination of rule-based logic and generative AI (Google Gemini) to assign a buying intent score (**High**, **Medium**, or **Low**) to each lead. The primary goal is to help sales teams save time by automatically prioritizing their outreach efforts.

***
## Tech Stack 🛠️

* **Backend:** Python, Flask
* **AI:** Google Gemini API
* **Data Handling:** Pandas
* **Containerization:** Docker
* **Production Server:** Gunicorn

***
## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

* Python 3.8+
* Git
* Docker

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/boorrring/Backend-_service.git
    cd lead_scorer_project
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_GOES_HERE"
    ```

5.  **Run the development server:**
    ```bash
    python main.py
    ```
    The server will start on `http://127.0.0.1:5000`.



***
## Running with Docker 🐳

The recommended way to run this application is with Docker.

1.  **Build the Docker image:**
    ```bash
    docker build -t lead-scorer-app .
    ```

2.  **Run the Docker container:**
    This command starts the container, maps the port, and securely passes your API key.
    ```bash
    docker run -p 5000:5000 -e GEMINI_API_KEY="YOUR_GEMINI_API_KEY_GOES_HERE" lead-scorer-app
    ```
    The application will be accessible at `http://localhost:5000`.

***
## API Usage

You can interact with the API using a tool like `curl` or Postman.


### 1. Set the Offer Details
Upload your product/offer information.
```bash
curl -X POST -H "Content-Type: application/json" -d @test_files/offer.json http://127.0.0.1:5000/offer
```
### 2. Upload the Leads CSV
Upload your list of leads.
```bash
curl -X POST -F "file=@test_files/leads.csv" http://127.0.0.1:5000/leads/upload
```
### 3. Trigger the Scoring Pipeline
Tell the service to process the data you've uploaded.
```bash
curl -X POST http://127.0.0.1:5000/score
```
### 4. View Results in Terminal
Get the results as a JSON array.
```bash
curl -X GET http://127.0.0.1:5000/results
```

### 5. Download Results as a CSV File
Use your browser or curl to download the final report.
```bash
curl -X GET http://127.0.0.1:5000/results/download
```
