# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CVE Sentinel - A Claude Code plugin that automatically detects CVE vulnerabilities in project dependencies and proposes remediation actions.

### Core Functionality
- **CVE Detection**: Fetches vulnerability data from NVD API 2.0 and Google OSV
- **Dependency Analysis**: Parses package manifests and lock files across multiple languages
- **Vulnerability Matching**: Correlates detected packages with known CVEs using CPE matching
- **Remediation Proposals**: Suggests fix versions and upgrade commands

### Plugin Architecture
- Runs as a Claude Code Hook (SessionStart trigger)
- Uses background processing with status/result JSON files for async communication
- CLAUDE.md instructions guide Claude to monitor `.cve-sentinel/status.json` and report results

## Technology Stack

- **Implementation**: Python
- **Data Sources**: NVD API 2.0 (requires API key), Google OSV
- **CVE Fetch Strategy**: Package-specific queries (not bulk download)
- **Cache**: Per-project (`.cve-sentinel/cache/`)

## Supported Package Managers

| Language | Package Managers | Manifest Files | Lock Files |
|----------|-----------------|----------------|------------|
| JavaScript/TypeScript | npm, yarn, pnpm | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| Python | pip, poetry, pipenv | requirements.txt, pyproject.toml, Pipfile | poetry.lock, Pipfile.lock |
| Go | go mod | go.mod | go.sum |
| Java | Maven, Gradle | pom.xml, build.gradle | - |
| Ruby | Bundler | Gemfile | Gemfile.lock |
| Rust | Cargo | Cargo.toml | Cargo.lock |
| PHP | Composer | composer.json | composer.lock |

## Analysis Levels

- **Level 1**: Direct dependencies from manifest files
- **Level 2**: Transitive dependencies from lock files
- **Level 3**: Import statement scanning in source code (reports file:line locations)

## Key File Structure

```
.cve-sentinel/
├── status.json      # Scan state (scanning|completed|error)
├── results.json     # Scan results with vulnerabilities
└── cache/           # CVE data cache

.cve-sentinel.yaml   # Project configuration
```

## Configuration

Configuration via `.cve-sentinel.yaml`:
- `target_path`: Scan target directory
- `exclude`: Paths to exclude
- `analysis_level`: 1-3
- `auto_scan_on_startup`: Enable/disable automatic scanning
- `cache_ttl_hours`: Cache expiration

## NVD API Key

Required for optimal performance. Store in environment variable:
```bash
export NVD_API_KEY=your-api-key-here
```

## Development

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy cve_sentinel
```
