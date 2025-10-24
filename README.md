# Samsung Phone Advisor

This project is a smart assistant designed for a tech review platform. It helps users make informed decisions when buying Samsung smartphones by providing both detailed specifications and natural-language reviews or recommendations through a single, unified API.

The system leverages a modern tech stack, including on-demand web scraping for data collection, PostgreSQL for data storage, and a sophisticated, tool-using agent built with **LangGraph** to process and respond to user queries. The entire service is containerized with Docker and exposed via a FastAPI endpoint.

## ✨ Features

-   **On-Demand Data Collection**: Scrape phone data for specific models from GSMArena via a dedicated API endpoint.
-   **Structured Data Storage**: Persists scraped data (model name, release date, display, battery, camera, etc.) in a PostgreSQL database.
-   **Natural Language Interaction**: Users can ask complex questions in plain English.
-   **Intelligent Agent Architecture (LangGraph)**:
    -   A central agent receives user queries.
    -   It intelligently decides whether to answer directly or use specialized tools.
    -   **`query_devices` Tool**: Retrieves structured specifications from PostgreSQL to answer factual and comparative questions.
    -   **`add_device` Tool**: Scrapes and adds new phone models to the database on command.
    -   The agent synthesizes tool outputs and conversation history to generate comprehensive, natural-language answers.
-   **Unified API Endpoints**: A primary `/ask` endpoint for user queries and admin endpoints for data management.
-   **Containerized & Reproducible**: The entire application stack is managed by Docker and Docker Compose for easy setup and deployment.

## 🛠️ Tech Stack

-   **Backend**: Python, FastAPI
-   **Database**: PostgreSQL
-   **Web Scraping**: Firecrawl
-   **AI/LLM**: LangGraph, Groq API, Tool-Using Agents
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

The application requires API keys for Firecrawl (for web scraping) and Groq (for the LLM).

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

-   `--build`: This flag ensures that the Docker images are rebuilt, incorporating any changes you've made.
-   The first time you run this, it may take a few minutes to pull the base images, build the application image, and start the containers.

The FastAPI server will be available at `http://localhost:8000`.

### 4. Populate the Database (Important!)

The database starts empty. You must add phone models before you can ask questions about them. Use the `/add_device` endpoint for each phone you want the advisor to know about.

Open a new terminal and run the following commands to add a few models:

```bash
# Add Samsung Galaxy S24 Ultra
curl -X 'POST' 'http://localhost:8000/api/v1/add_device/Samsung%20Galaxy%20S24%20Ultra'

# Add Samsung Galaxy S23 Ultra
curl -X 'POST' 'http://localhost:8000/api/v1/add_device/Samsung%20Galaxy%20S23%20Ultra'

# Add Samsung Galaxy A55
curl -X 'POST' 'http://localhost:8000/api/v1/add_device/Samsung%20Galaxy%20A55'
```
Wait for each command to complete before running the next. You can add any 20-30 models from GSMArena you wish.

## 🤖 API Endpoints

The application exposes several endpoints to handle user queries and data management.

### User-Facing Endpoint

#### `POST /api/v1/ask`

This is the main endpoint for asking the assistant questions.

**Using `curl`**

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/ask' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "Compare Samsung Galaxy S24 Ultra and S23 Ultra for photography"
}'
```

**Example Queries**

-   **Direct Factual Question**:
    `"What are the specs of Samsung Galaxy S24 Ultra?"`
-   **Comparative Question**:
    `"Compare Galaxy S24 Ultra and S23 Ultra."`
-   **Recommendation Question**:
    `"Which Samsung phone has the best battery under $1000?"`

---

### Admin Endpoints

These endpoints are used for managing the phone data in the database.

#### `POST /api/v1/add_device/{model_name}`

Scrapes GSMArena for the specified phone model and adds its data to the database. The `model_name` in the URL should be URL-encoded (e.g., spaces become `%20`).

**Using `curl`**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/add_device/Samsung%20Galaxy%20Z%20Fold5'
```

#### `GET /api/v1/query_devices`

Allows for direct, read-only querying of the database using a SQL `WHERE` clause. This is useful for debugging or advanced data retrieval.

**Using `curl`**
```bash
# Find all phones with more than 5000 mAh battery
curl -G \
  'http://localhost:8000/api/v1/query_devices' \
  --data-urlencode "where_clause=battery_mah > 5000"

# Find all phones that cost less than $800 (80000 cents)
curl -G \
  'http://localhost:8000/api/v1/query_devices' \
  --data-urlencode "where_clause=price_cents < 80000"
```

### Using the Interactive API Docs (Swagger UI)

For a more user-friendly interface to test all endpoints:

1.  Open your web browser and navigate to **http://localhost:8000/docs**.
2.  Click on any endpoint, then "Try it out".
3.  Enter your parameters or request body and click "Execute".

## 📹 Video Demonstration

A short video demonstrating the project's setup and functionality can be found here:

**[[Video Tutorial](https://youtu.be/FCkK9Zc3YOA)]**