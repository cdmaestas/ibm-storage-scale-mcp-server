"""IBM Storage Scale Operations MCP Server.

Operations management tools for tracking and managing long-running asynchronous operations.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.operations import (
    list_operations_api,
    get_operation_api,
    cancel_operation_api,
    wait_for_operation_api,
)

# Create the operations MCP server
mcp = FastMCP(
    "operations",
    instructions="Operations tracking and management for long-running tasks",
)


@mcp.tool()
async def list_operations(
    ctx: Context,
    filter: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all operations.

    Retrieves a list of operations, optionally filtered by status or other criteria.

    Args:
        filter: Filter expression (e.g., 'status=running', 'status=completed')
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of operations
    """
    await ctx.info("Tool called: list_operations")
    await ctx.debug(f"Listing operations with filter: {filter}")

    try:
        result = await list_operations_api(filter=filter, domain=domain)
        await ctx.info("Successfully retrieved operations list")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list operations: {str(e)}")
        raise


@mcp.tool()
async def get_operation(
    ctx: Context,
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific operation.

    Retrieves detailed information about a specific operation including its
    status, progress, and results.

    Args:
        operation_id: Operation ID
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation details
    """
    await ctx.info(f"Tool called: get_operation for ID: {operation_id}")
    await ctx.debug(f"Retrieving operation details for: {operation_id}")

    try:
        result = await get_operation_api(operation_id=operation_id, domain=domain)
        await ctx.info(f"Successfully retrieved operation: {operation_id}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get operation {operation_id}: {str(e)}")
        raise


@mcp.tool()
async def cancel_operation(
    ctx: Context,
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Cancel a running operation.

    Attempts to cancel a running operation. Not all operations can be cancelled.

    Args:
        operation_id: Operation ID to cancel
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cancellation status
    """
    await ctx.info(f"Tool called: cancel_operation for ID: {operation_id}")
    await ctx.debug(f"Attempting to cancel operation: {operation_id}")

    try:
        result = await cancel_operation_api(operation_id=operation_id, domain=domain)
        await ctx.info(f"Successfully cancelled operation: {operation_id}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to cancel operation {operation_id}: {str(e)}")
        raise


@mcp.tool()
async def wait_for_operation(
    ctx: Context,
    operation_id: str,
    timeout: Optional[int] = None,
    domain: Optional[str] = None,
) -> Any:
    """Wait for an operation to complete.

    Polls an operation until it completes or times out.

    Args:
        operation_id: Operation ID to wait for
        timeout: Maximum time to wait in seconds (optional)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing final operation status
    """
    await ctx.info(f"Tool called: wait_for_operation for ID: {operation_id}")
    await ctx.debug(f"Waiting for operation: {operation_id} (timeout: {timeout}s)")

    try:
        result = await wait_for_operation_api(
            operation_id=operation_id, timeout=timeout, domain=domain
        )
        await ctx.info(f"Operation completed: {operation_id}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to wait for operation {operation_id}: {str(e)}")
        raise
