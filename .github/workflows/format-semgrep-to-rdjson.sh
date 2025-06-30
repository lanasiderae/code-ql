#!/bin/bash
set -eo pipefail

INPUT_FILE="${1:-semgrep-results.json}"
OUTPUT_FILE="${2:-semgrep-rdjson.json}"

jq -c '.results[] | {
  "source": "semgrep",
  "type": "diagnostic",
  "check_name": .check_id,
  "severity": (
    if .extra.severity == "CRITICAL" or .extra.severity == "ERROR" then "ERROR"
    elif .extra.severity == "WARNING" then "WARNING"
    else "INFO" end
  ),
  "message": .extra.message,
  "location": {
    "path": .path,
    "range": {
      "start": { "line": .start.line },
      "end": { "line": (.end.line // .start.line) }
    }
  }
}

' "$INPUT_FILE" > "$OUTPUT_FILE"

' "$INPUT_FILE" > "$OUTPUT_FILE"
