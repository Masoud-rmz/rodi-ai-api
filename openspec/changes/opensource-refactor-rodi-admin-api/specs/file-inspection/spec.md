## MODIFIED Requirements

### Requirement: File inspection is an isolated feature module
`safe_read_text_file` and handlers for `/read`, `/ls`, `/find` SHALL live in `rodi_admin/features/file_inspection.py`.

#### Scenario: /read returns file content
- **WHEN** `GET /read?path=/etc/hostname` is received and file exists
- **THEN** response contains `{"success": true, "content": "...", "size": N, "encoding": "utf-8"}`

#### Scenario: /read truncates large files
- **WHEN** file size exceeds `MAX_READ_BYTES`
- **THEN** response contains `{"truncated": true, "max_bytes": 262144}`

#### Scenario: /read on missing file returns 404
- **WHEN** `GET /read?path=/nonexistent` is received
- **THEN** response status is `404` with `{"success": false, "error": "file not found"}`

#### Scenario: /ls lists directory contents
- **WHEN** `GET /ls?path=/home` is received
- **THEN** response contains stdout of `ls -la /home`

#### Scenario: /find searches by name pattern
- **WHEN** `GET /find?path=/etc&name=*.conf&depth=2` is received
- **THEN** response contains matching file paths from `find` command output
