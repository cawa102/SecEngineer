<p align="center">
  <img src="assets/icon.png" alt="CVE Sentinel" width="180" height="180">
</p>

<h1 align="center">CVE Sentinel</h1>

<p align="center">
  <strong>Your AI-Powered Vulnerability Detector</strong>
</p>

<p align="center">
  Automatically detect vulnerabilities in your dependencies before they become threats.
</p>

<p align="center">
  <a href="https://github.com/cawa102/cveSentinel/actions/workflows/ci.yml">
    <img src="https://github.com/cawa102/cveSentinel/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
</p>

---

## Demo

<p align="center">
  <img src="assets/cveSentinel.gif" alt="CVE Sentinel Demo" width="800">
</p>

https://github.com/user-attachments/assets/25634a88-8ed0-4da4-9b11-4e924ad87adf

---

## Why CVE Sentinel?

Every day, new vulnerabilities are discovered in popular packages. **CVE Sentinel** integrates seamlessly with Claude Code to automatically scan your project dependencies and alert you to security risks - before you ship vulnerable code.

### Key Features

- **Automatic Scanning** - Runs silently in the background when you start Claude Code
- **Multi-Source Intelligence** - Combines data from NVD and Google OSV for comprehensive coverage
- **7+ Languages Supported** - JavaScript, Python, Go, Java, Ruby, Rust, PHP and more
- **Smart Analysis** - Three levels from quick manifest scans to deep source code analysis
- **Actionable Fixes** - Get specific upgrade commands, not just vulnerability reports

---

## Quick Start

### Installation

```bash
# Install from GitHub
pip install git+https://github.com/cawa102/cveSentinel.git

# Or clone and install locally
git clone https://github.com/cawa102/cveSentinel.git
cd cveSentinel
pip install .
```

### Scan Your Project

```bash
# Scan current directory
cve-sentinel scan

# Scan a specific directory
cve-sentinel scan /path/to/project

# Scan with options
cve-sentinel scan /path/to/project --level 2 --exclude node_modules --exclude .venv
```

No configuration file required - just run and scan!

### Auto-scan with Claude Code (Optional)

```bash
cve-sentinel init
```

This sets up a **SessionStart Hook** - CVE Sentinel will automatically scan your project every time you launch Claude Code.

---

## NVD API Key (Recommended)

For faster scanning, get a free API key from [NVD](https://nvd.nist.gov/developers/request-an-api-key):

```bash
export NVD_API_KEY=your-api-key-here
```

Without an API key, requests are rate-limited to 5 per 30 seconds.


---

## How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Your Project   │────▶│  CVE Sentinel   │────▶│  Security Report│
│                 │     │                 │     │                 │
│ package.json    │     │ ┌─────────────┐ │     │ 3 Critical      │
│ requirements.txt│     │ │ NVD API 2.0 │ │     │ 5 High          │
│ go.mod          │     │ └─────────────┘ │     │ 2 Medium        │
│ Cargo.toml      │     │ ┌─────────────┐ │     │                 │
│ ...             │     │ │ Google OSV  │ │     │ + Fix Commands  │
│                 │     │ └─────────────┘ │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Supported Languages (Default)

| Language | Package Managers | Files Analyzed |
|:--------:|:-----------------|:---------------|
| **JavaScript** | npm, yarn, pnpm | `package.json`, `package-lock.json`, `yarn.lock` |
| **Python** | pip, poetry, pipenv | `requirements.txt`, `pyproject.toml`, `Pipfile` |
| **Go** | go mod | `go.mod`, `go.sum` |
| **Java** | Maven, Gradle | `pom.xml`, `build.gradle` |
| **Ruby** | Bundler | `Gemfile`, `Gemfile.lock` |
| **Rust** | Cargo | `Cargo.toml`, `Cargo.lock` |
| **PHP** | Composer | `composer.json`, `composer.lock` |

---

## Analysis Levels

Choose the depth of analysis that fits your needs:

| Level | What It Scans | Best For |
|:-----:|:--------------|:---------|
| **1** | Manifest files only | Quick CI checks |
| **2** | + Lock files (transitive deps) | Regular development (default) |
| **3** | + Source code imports | Pre-release audits |

```bash
# Quick scan - manifest files only (Level 1)
cve-sentinel scan --level 1

# Standard scan - includes lock files (Level 2, default)
cve-sentinel scan

# Deep scan - includes source code analysis (Level 3)
cve-sentinel scan --level 3

# Scan specific directory with level
cve-sentinel scan /path/to/project --level 3
```

---

## Usage

```bash
cve-sentinel scan [PATH] [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `PATH` | Target directory to scan (default: current directory) |
| `--level`, `-l` | Analysis level: 1, 2, or 3 (default: 2) |
| `--exclude`, `-e` | Paths to exclude (can be specified multiple times) |
| `--verbose`, `-v` | Enable verbose output |
| `--fail-on` | Exit with error if vulnerabilities at or above this severity (default: HIGH) |

### Examples

```bash
# Basic scan
cve-sentinel scan

# Scan with exclusions
cve-sentinel scan --exclude node_modules --exclude dist

# CI/CD usage - fail on critical vulnerabilities only
cve-sentinel scan --fail-on CRITICAL

# Verbose deep scan
cve-sentinel scan /path/to/project --level 3 --verbose
```

---

## Configuration (Optional)

For persistent settings, create `.cve-sentinel.yaml` in your project root:

```yaml
# Scan settings
analysis_level: 2

# Exclude paths (e.g., test fixtures)
exclude:
  - node_modules/
  - vendor/
  - .venv/

# Cache settings
cache_ttl_hours: 24

# Auto-scan on Claude Code startup
auto_scan_on_startup: true
```

CLI options override configuration file settings.

---

## Custom File Patterns

Your unique projects sometimes use non-standard file names for their dependencies. CVE Sentinel lets you specify additional file patterns to scan:

```yaml
# .cve-sentinel.yaml
custom_patterns:
  python:
    manifests:
      - "deps/*.txt"
      - "requirements-*.txt"
    locks:
      - "custom.lock"
  javascript:
    manifests:
      - "dependencies.json"
```

### Supported Ecosystems

| Config Key | Aliases | Default Files |
|:-----------|:--------|:--------------|
| `javascript` | `npm` | `package.json`, `package-lock.json`, `yarn.lock` |
| `python` | `pypi` | `requirements.txt`, `pyproject.toml`, `Pipfile` |
| `go` | - | `go.mod`, `go.sum` |
| `java` | `maven`, `gradle` | `pom.xml`, `build.gradle` |
| `ruby` | `rubygems` | `Gemfile`, `Gemfile.lock` |
| `rust` | `crates.io` | `Cargo.toml`, `Cargo.lock` |
| `php` | `packagist` | `composer.json`, `composer.lock` |

Custom patterns **extend** the defaults - your standard files are always scanned.

---

## Claude Code Integration

CVE Sentinel is designed to work seamlessly with [Claude Code](https://claude.ai/code). After running `cve-sentinel init`, it will:

1. Automatically scan your project when you start a Claude Code session
2. Report vulnerabilities directly in your conversation
3. Suggest fixes that Claude can help you implement

---

## Sample Output

```json
{
  "scan_time": "2025-01-21T00:00:00Z",
  "summary": {
    "critical": 1,
    "high": 3,
    "medium": 5,
    "low": 2
  },
  "vulnerabilities": [
    {
      "cve_id": "CVE-2024-XXXXX",
      "package": "lodash",
      "installed_version": "4.17.20",
      "severity": "CRITICAL",
      "description": "Prototype pollution vulnerability...",
      "fix_version": "4.17.21",
      "remediation": "npm update lodash"
    }
  ]
}
```

---

## Development

```bash
# Clone and install
git clone https://github.com/cawa102/cveSentinel.git
cd cveSentinel
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

---

## Contributing

Contributions are welcome! Whether it's:
- Adding support for new languages
- Improving vulnerability detection
- Enhancing the user experience

Please feel free to submit a Pull Request.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with security in mind. Powered by Claude Code.</sub>
</p>
