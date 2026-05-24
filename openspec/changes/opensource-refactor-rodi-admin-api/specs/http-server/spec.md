## MODIFIED Requirements

### Requirement: HTTP server and routing are in an isolated feature module
`AdminHandler` (with all `do_GET`, `do_POST`, `do_OPTIONS` methods) and the `ThreadingHTTPServer` setup SHALL live in `rodi_admin/features/http_server.py`. Handler methods SHALL delegate business logic to the appropriate feature modules rather than implementing it inline.

#### Scenario: All endpoints respond correctly after refactor
- **WHEN** any documented endpoint is called after refactor
- **THEN** response is identical to the response from the original `api_admin.py`

#### Scenario: CORS headers are present on all responses
- **WHEN** any GET or POST request is made
- **THEN** response includes `Access-Control-Allow-Origin: *`

#### Scenario: OPTIONS preflight is handled
- **WHEN** `OPTIONS /run` is received
- **THEN** response status is `200` with CORS headers

#### Scenario: Unknown path returns 404 JSON
- **WHEN** `GET /nonexistent` is received
- **THEN** response is `404` with `{"error": "Path not found"}`
