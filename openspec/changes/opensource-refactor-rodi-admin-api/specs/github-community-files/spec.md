## ADDED Requirements

### Requirement: Standard GitHub OSS files present
The repository SHALL contain all required files for a standard open-source GitHub project: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`.

#### Scenario: LICENSE file exists with MIT license
- **WHEN** repository is published
- **THEN** `LICENSE` file exists containing MIT license text with correct copyright holder

#### Scenario: README has all required sections
- **WHEN** README.md is rendered on GitHub
- **THEN** it contains: badges (version, license, python version), one-line description, features list, requirements, installation steps, usage examples, API reference table, and license section

#### Scenario: SECURITY.md documents reporting process
- **WHEN** a security researcher finds a vulnerability
- **THEN** `SECURITY.md` provides a clear contact method and states the tool is for LAN/private use only

### Requirement: GitHub issue and PR templates
The repository SHALL have `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, and `.github/PULL_REQUEST_TEMPLATE.md`.

#### Scenario: Bug report template has required fields
- **WHEN** user opens a new issue on GitHub
- **THEN** they see a template with: Python version, OS version, steps to reproduce, expected vs actual behavior

#### Scenario: PR template has checklist
- **WHEN** contributor opens a pull request
- **THEN** they see a checklist including: tested on Ubuntu, no new external dependencies, docstrings added

### Requirement: CI workflow runs on push
The `.github/workflows/ci.yml` SHALL run on every push and pull request to `main`, install the package, and run a basic import smoke test.

#### Scenario: CI passes on clean code
- **WHEN** a push is made to `main` with valid code
- **THEN** GitHub Actions workflow completes successfully on `ubuntu-latest`
