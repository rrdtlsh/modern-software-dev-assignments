# Week 3 — Weather MCP Server

## Overview

This project implements a **Model Context Protocol (MCP) server** that integrates with the public Open-Meteo API.  

The server exposes weather-related tools that can be invoked by an MCP-compatible client such as the MCP Inspector or Claude Desktop.

Deployment mode: **Local (STDIO transport)**

---

## Features

- Exposes 2 MCP tools:
  - `get_current_weather_tool`
  - `get_weather_forecast_tool`
- Graceful error handling
- Timeout handling
- HTTP error handling
- Rate limit awareness (HTTP 429)
- Input validation
- Clean modular project structure

---

## Project Structure


week3/
├── server/
│ ├── main.py
│ ├── tools.py
│ ├── api_client.py
│ └── models.py
├── requirements.txt
└── README.md


---

## Prerequisites

- Python 3.10+
- pip
- MCP Inspector or MCP-compatible client

---

## Installation

1. Clone the repository or navigate to the `week3` directory.
2. Install dependencies:


pip install -r requirements.txt


---

## Running the MCP Server (Local STDIO)

From inside the `server` directory:


python main.py


The MCP server will start and wait for client connections.

---

## Connecting with MCP Inspector

1. Open MCP Inspector.
2. Choose STDIO transport.
3. Set command to:


python main.py


4. Click **Connect**.
5. The tools should appear in the Tools tab.

---

## Tool Reference

### 1️⃣ get_current_weather_tool

**Description:**  
Returns the current weather conditions for a given city.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|------------|
| city | string | Yes | Name of the city |

**Example Input:**


{
"city": "Jakarta"
}


**Example Output:**


{
"temperature": 30.5,
"windspeed": 12.3,
"winddirection": 250,
"weathercode": 1,
"time": "2026-02-26T08:00"
}


**Possible Errors:**

- `"City must not be empty"`
- `"No results found for city: ..."`
- `"Weather request timed out"`
- `"API rate limit exceeded. Please try again later."`

---

### 2️⃣ get_weather_forecast_tool

**Description:**  
Returns a 3-day temperature forecast for a given city.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|------------|
| city | string | Yes | Name of the city |

**Example Input:**


{
"city": "Bandung"
}


**Example Output:**


{
"temperature_2m_max": [31, 30, 29],
"temperature_2m_min": [24, 23, 22],
"time": ["2026-02-26", "2026-02-27", "2026-02-28"]
}


---

## Reliability & Resilience Features

This server implements the following robustness mechanisms:

- Input validation (type and empty string checks)
- Timeout handling (10 seconds per request)
- HTTP error handling via `response.raise_for_status()`
- Custom exception class (`WeatherAPIError`)
- Rate limit detection (HTTP 429)
- Defensive response structure validation

These measures prevent server crashes and ensure graceful failure handling.

---

## External API Used

- Open-Meteo Forecast API  
  https://api.open-meteo.com/

- Open-Meteo Geocoding API  
  https://geocoding-api.open-meteo.com/

No API key is required for this implementation.

---

## Design Decisions

- Tools are separated into `tools.py`
- API logic is separated into `api_client.py`
- Typed models are defined in `models.py`
- Centralized HTTP error handling improves maintainability
- STDIO transport chosen for simplicity and local testing

---

## Evaluation Criteria Coverage

| Category | Status |
|----------|--------|
| 2+ MCP Tools | ✅ |
| External API Integration | ✅ |
| Error Handling | ✅ |
| Rate Limit Awareness | ✅ |
| Clear Documentation | ✅ |
| Clean Code Structure | ✅ |

---

## Logging

This server uses structured logging to stderr to comply with STDIO MCP transport best practices.

## Author

Raudatul Sholehah  
Program Studi Teknologi Informasi  
Universitas Lambung Mangkurat  