# Onboarding system agents

This project is a proof-of-concept for a set of agents to interact with our onboarding system. The goal is to demonstrate how agents can be used to automate and streamline the onboarding process for new employees.

## Agents

We will start by creating two agents:

1. **Service Catalog Agent:** This agent will help employees with their tasks. It will be able to provide information about services, create service requests, and track their status.
2. **Employee Catalog Agent:** This agent will be used to manage employee data. It will provide functionality to get and set employee attributes, as well as search for employees.

## Getting Started

1. Install dependencies:

   ```bash
   pip install -e .
   ```

2. Set up your environment variables by creating a `.env` file. You will need an `OPENAI_API_KEY`.
3. Run the application:

   ```bash
   python main.py
   ```
