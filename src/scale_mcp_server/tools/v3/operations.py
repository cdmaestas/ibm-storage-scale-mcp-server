"""IBM Storage Scale Operations MCP Server.

Tools for tracking and managing long-running operations (LRO).
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.operations import (
    list_operations_api,
    get_operation_api,
    get_operation_output_api,
    cancel_operation_api,
    delete_operation_api,
)

# Create the operations MCP server
mcp = FastMCP("operations", instructions="Long-running operation (LRO) management")


@mcp.tool()
async def list_operations(
    ctx: Context,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List information about all long-running operations (LROs).

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_operations")
    try:
        return await list_operations_api(
            page_size=page_size, page_token=page_token, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to list operations: {str(e)}")
        raise


@mcp.tool()
async def get_operation(
    ctx: Context,
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """List details of an existing LRO.

    Args:
        operation_id: Operation ID of the LRO
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_operation with operation_id={operation_id}")
    try:
        return await get_operation_api(operation_id=operation_id, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get operation {operation_id}: {str(e)}")
        raise


@mcp.tool()
async def get_operation_output(
    ctx: Context,
    operation_id: str,
    byte_offset: Optional[int] = None,
    domain: Optional[str] = None,
) -> Any:
    """Display message output from an LRO.

    Args:
        operation_id: Operation ID of the LRO
        byte_offset: Offset in bytes to start reading the console output
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_operation_output with operation_id={operation_id}")
    try:
        return await get_operation_output_api(
            operation_id=operation_id, byte_offset=byte_offset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get output for operation {operation_id}: {str(e)}")
        raise


@mcp.tool()
async def cancel_operation(
    ctx: Context,
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Cancel an LRO.

    Args:
        operation_id: Operation ID of the LRO to cancel
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: cancel_operation with operation_id={operation_id}")
    try:
        return await cancel_operation_api(operation_id=operation_id, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to cancel operation {operation_id}: {str(e)}")
        raise


@mcp.tool()
async def delete_operation(
    ctx: Context,
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete an existing LRO record.

    Args:
        operation_id: Operation ID of the LRO to delete
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_operation with operation_id={operation_id}")
    try:
        return await delete_operation_api(operation_id=operation_id, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to delete operation {operation_id}: {str(e)}")
        raise
