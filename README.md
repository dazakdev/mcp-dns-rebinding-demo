# mcp-dns-rebinding-demo

Example code showing how a random website you open can read an MCP server running
on your own `127.0.0.1`, using DNS rebinding. It's here to read, not to run. All
data is fake.

## The pieces

- `normal_mcp.py` — a plain FastMCP server (the victim), no auth, on `127.0.0.1:4040`.
- `attacker_dns.py` — DNS for a demo zone: answers the attacker's IP, then flips to `127.0.0.1`.
- `attacker_web.py` — serves the page, then opens the flip window.
- `attack.html` — the page: a same-origin MCP handshake that reads the victim.
- `phase.py` — the shared flip flag.

## How it works

The page loads from the attacker's IP. Serving it flips the name to `127.0.0.1`,
so the page's same-origin `fetch` to `…/mcp` now hits your local MCP, and being
same-origin it gets to read the response. Chrome and Firefox block
public→loopback (Local Network Access); Safari doesn't yet.

## The fix

Reject any request whose `Host` isn't loopback:

```python
if request.headers.get("host", "").split(":")[0] not in ("127.0.0.1", "localhost", "[::1]"):
    return forbidden()
```
