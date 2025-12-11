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

## Testing MCP Servers with Inspector

The agents use Model Context Protocol (MCP) servers for their functionality. You can test and inspect these servers using the MCP inspector tool.

### Prerequisites

1. **Install Node.js** (if not already installed):
   ```bash
   winget install OpenJS.NodeJS
   ```

2. **Make Node.js available in new terminals**:
   
   **Option A: Restart your computer** (Recommended - ensures PATH is updated system-wide)
   
   **Option B: Refresh PATH in current session**:
   ```powershell
   $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
   ```
   
   **Option C: Manually add to PATH for current session**:
   ```powershell
   $env:PATH += ";C:\Program Files\nodejs"
   ```

3. **Verify Node.js is available**:
   ```bash
   node --version
   npx --version
   ```

### Running MCP Servers

1. **Start the Service Catalog MCP Server**:
   ```bash
   # Activate virtual environment
   .venv\Scripts\Activate.ps1
   
   # Run the server
   cd group1
   python -m agents.service_catalog.service_catalog_mcp.server
   ```
   Server will be available at: `http://0.0.0.0:8003/mcp`

2. **Start the Employee Catalog MCP Server**:
   ```bash
   # In a separate terminal
   cd group1
   python -m agents.employee_catalog.employee_catalog_mcp.server
   ```
   Server will be available at: `http://0.0.0.0:8002/mcp`

### Using the MCP Inspector

1. **Launch the inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **Set Transport Type**
Set Transport Type to Streamable HTTP

3. **Set URL**:
   - Service Catalog: `http://0.0.0.0:8003/mcp`
   - Employee Catalog: `http://0.0.0.0:8002/mcp`

4. **Test available tools**:
   - **Service Catalog**: `get_all_services`, `get_service_by_name`, `get_service_access_requirements`
   - **Employee Catalog**: `get_all_employees`, `get_employee_by_name`, `get_employee_by_id`

The inspector provides a web interface to test MCP server functionality, view available tools, and debug interactions.
