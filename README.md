# CVE Sentinel

[![CI](https://github.com/cawa102/SecEngineer/actions/workflows/ci.yml/badge.svg)](https://github.com/cawa102/SecEngineer/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CVE auto-detection and remediation proposal system for Claude Code. Automatically scans your project dependencies for known vulnerabilities and suggests fixes.

## Features

- **Multi-source CVE Detection**: Fetches vulnerability data from NVD API 2.0 and Google OSV
- **Multi-language Support**: Analyzes dependencies across 7+ languages
- **Three Analysis Levels**: From manifest-only to full source code import scanning
- **Smart Matching**: CPE-based vulnerability matching with version range checking
- **Remediation Proposals**: Suggests fix versions and upgrade commands
- **Claude Code Integration**: Runs as a session hook for automatic scanning

## Supported Languages

| Language | Package Managers | Manifest Files | Lock Files |
|----------|-----------------|----------------|------------|
| JavaScript/TypeScript | npm, yarn, pnpm | package.json | package-lock.json, yarn.lock, pnpm-lock.yaml |
| Python | pip, poetry, pipenv | requirements.txt, pyproject.toml, Pipfile | poetry.lock, Pipfile.lock |
| Go | go mod | go.mod | go.sum |
| Java | Maven, Gradle | pom.xml, build.gradle | - |
| Ruby | Bundler | Gemfile | Gemfile.lock |
| Rust | Cargo | Cargo.toml | Cargo.lock |
| PHP | Composer | composer.json | composer.lock |

## Installation

```bash
pip install cve-sentinel
```

Or install from source:

```bash
git clone https://github.com/cawa102/SecEngineer.git
cd SecEngineer
pip install -e .
```

## Quick Start

```bash
# Scan current directory
cve-sentinel

# Scan specific path
cve-sentinel --path /path/to/project

# Scan with specific analysis level
cve-sentinel --level 3
```

## Configuration

Create `.cve-sentinel.yaml` in your project root:

```yaml
# Target directory to scan
target_path: ./

# Paths to exclude from scanning
exclude:
  - node_modules/
  - vendor/
  - .venv/

# Analysis level (1-3)
# 1: Direct dependencies from manifest files only
# 2: Include transitive dependencies from lock files
# 3: Full source code import scanning
analysis_level: 3

# Enable automatic scanning on Claude Code session start
auto_scan_on_startup: true

# Cache expiration in hours
cache_ttl_hours: 24
```

## Analysis Levels

| Level | Description | Speed | Coverage |
|-------|-------------|-------|----------|
| **1** | Manifest files only (package.json, requirements.txt, etc.) | Fast | Direct dependencies |
| **2** | + Lock files (package-lock.json, poetry.lock, etc.) | Medium | All dependencies |
| **3** | + Source code import scanning | Thorough | Includes file:line locations |

## NVD API Key

For best results, obtain an NVD API key from [nvd.nist.gov](https://nvd.nist.gov/developers/request-an-api-key) and set it as an environment variable:

```bash
export NVD_API_KEY=your-api-key-here
```

Without an API key, requests are rate-limited to 5 requests per 30 seconds.

## Claude Code Integration

CVE Sentinel can run automatically when you start a Claude Code session. Add the session hook to your Claude Code settings to enable automatic vulnerability scanning.

## Output

CVE Sentinel generates results in `.cve-sentinel/results.json`:

```json
{
  "scan_time": "2025-01-21T00:00:00Z",
  "vulnerabilities": [
    {
      "cve_id": "CVE-2024-XXXXX",
      "package": "example-package",
      "installed_version": "1.0.0",
      "severity": "HIGH",
      "description": "...",
      "fix_version": "1.0.1",
      "remediation": "npm update example-package"
    }
  ]
}
```

## Development

```bash
# Clone repository
git clone https://github.com/cawa102/SecEngineer.git
cd SecEngineer

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy cve_sentinel
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
