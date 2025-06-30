jq -c '.results[] |
  {
    source: "semgrep",
    type: "diagnostic",
    check_name: .check_id,
    severity: (
      if .extra.severity == "CRITICAL" or .extra.severity == "ERROR" then "ERROR"
      elif .extra.severity == "WARNING" then "WARNING"
      else "INFO" end
    ),
    message: (
      (if .extra.severity == "CRITICAL" then "🚨 [CRITICAL]"
       elif .extra.severity == "ERROR" then "🔴 [HIGH]"
       elif .extra.severity == "WARNING" then "⚠️ [MEDIUM]"
       else "💡 [LOW]"
      end)
      + " " + .extra.message
      + "\n(ID: " + .check_id + ")"
      + (if .extra.fix.sed then "\n🔧 Auto-fix available" else "" end)
      + (if (.extra.metadata.references | length) > 0 then "\n📚 Docs: " + .extra.metadata.references[0] else "" end)
      + "\nIf you believe this is a false positive or acceptable risk, add `# nosemgrep` or `// nosemgrep` to skip this finding."
    ),
    location: {
      path: .path,
      range: {
        start: { line: .start.line },
        end: { line: (.end.line // .start.line) }
      }
    }
  }
' "$INPUT_FILE" > "$OUTPUT_FILE"
