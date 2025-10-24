# Task 2: Samsung Phone Advisor

This project is a smart assistant designed for a tech review platform. It helps users make informed decisions when buying Samsung smartphones by providing both detailed specifications and natural-language reviews or recommendations through a single, unified API.

The system leverages a modern tech stack, including web scraping for data collection, PostgreSQL for data storage, and a sophisticated RAG (Retrieval-Augmented Generation) + Multi-Agent architecture to process and respond to user queries in natural language. The entire service is containerized with Docker and exposed via a FastAPI endpoint.

## ✨ Features

-   **Automated Data Collection**: Scrapes phone data (20-30 models) from GSMArena.
-   **Structured Data Storage**: Persists scraped data (model name, release date, display, battery, camera, etc.) in a PostgreSQL database.
-   **Natural Language Interaction**: Users can ask complex questions in plain English.
-   **Unified RAG + Multi-Agent System**:
    -   **RAG Module**: Retrieves structured specifications directly from PostgreSQL to answer factual questions.
    -   **Multi-Agent System**:
        -   *Data Extractor Agent*: Pulls relevant data from the database based on the query.
        -   *Review Generator Agent*: Generates comparative analysis and recommendations using a powerful language model (via Groq).
-   **Unified API Endpoint**: A single `/ask` endpoint powered by FastAPI intelligently routes queries to deliver specs, comparisons, or recommendations.
-   **Containerized & Reproducible**: The entire application stack is managed by Docker and Docker Compose for easy setup and deployment.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI
-   **Database**: PostgreSQL
-   **Web Scraping**: Firecrawl (or a similar Python library like `requests`/`BeautifulSoup`)
-   **AI/LLM**: RAG, Multi-Agent Architecture, Groq API
-   **Containerization**: Docker, Docker Compose

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-directory>
```

### 2. Configure Environment Variables

The application requires API keys for Firecrawl (for web scraping) and Groq (for LLM-powered generation).

1.  Create a `.env` file in the root of the project directory by copying the example file:
    ```bash
    cp .env.example .env
    ```

2.  Open the newly created `.env` file and add your personal API keys:
    ```dotenv
    # .env

    # Get your Firecrawl API key from https://www.firecrawl.dev/
    FIRECRAWL_API_KEY="YOUR_FIRECRAWL_API_KEY"

    # Get your Groq API key from https://console.groq.com/keys
    GROQ_API_KEY="YOUR_GROQ_API_KEY"

    ```

### 3. Build and Run with Docker Compose

With Docker running, execute the following command from the project's root directory:

```bash
docker-compose up --build
```

-   `--build`: This flag ensures that the Docker images are rebuilt from scratch, incorporating any changes you've made.
-   The first time you run this, it may take a few minutes to pull the base images, build the application image, and start the containers.
-   The scraping and data population process will run automatically upon the application's startup. Please be patient as the database is populated.

The FastAPI server will be available at `http://localhost:8000`.

## 🤖 How to Use the API

The application exposes a single `POST` endpoint to handle all user queries.

**Endpoint**: `POST /ask`

### Using `curl`

You can test the endpoint from your terminal using `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/ask' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "Compare Samsung Galaxy S23 Ultra and S22 Ultra for photography"
}'
```

### Example Queries

Try asking different types of questions to see the system in action:

-   **Direct Factual Question**:
    `"What are the specs of Samsung Galaxy S23 Ultra?"`
-   **Comparative Question**:
    `"Compare Galaxy S23 Ultra and S22 Ultra for photography."`
-   **Recommendation Question**:
    `"Which Samsung phone has the best battery under $1000?"`

### Using the Interactive API Docs (Swagger UI)

For a more user-friendly interface, you can use the auto-generated FastAPI documentation:

1.  Open your web browser and navigate to **http://localhost:8000/docs**.
2.  Click on the `/ask` endpoint, then "Try it out".
3.  Enter your question in the request body and click "Execute".

## 📹 Video Demonstration

A short video demonstrating the project's setup and functionality can be found here:

**[[Video Tutorial](https://youtu.be/FCkK9Zc3YOA)]**