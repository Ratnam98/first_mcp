# Expense Tracker MCP Server

FastMCP server for tracking expenses with four tools and one category resource.

## Run for Cloud / HTTP

Use the FastMCP config:

```powershell
fastmcp run
```

Or run the Python entrypoint directly:

```powershell
python main.py
```

Both serve MCP over HTTP at:

```text
http://localhost:8000/mcp/
```

If you run `fastmcp run main.py` without `--transport http`, FastMCP defaults to stdio. For an explicit HTTP command:

```powershell
fastmcp run main.py --transport http --host 0.0.0.0 --port 8000 --path /mcp/
```

Opening `/mcp/` directly in a browser may show `406 Not Acceptable`; that is expected because MCP clients must send streamable HTTP headers.

## SQLite Storage

The server stores expenses in SQLite at:

```text
/tmp/expenses.db
```

Override this with `EXPENSES_DB_PATH` when deploying with a persistent volume:

```powershell
$env:EXPENSES_DB_PATH="/path/to/persistent/expenses.db"
```
