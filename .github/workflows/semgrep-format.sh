#!/bin/bash

jq -r '
  .results[]
  | "\(.path):\(.start.line):\(.start.col // 1): \(
      if .extra.severity == \"CRITICAL\" then \"error\"
      elif .extra.severity == \"ERROR\" then \"error\"
      elif .extra.severity == \"WARNING\" then \"warning\"
      else \"info\"
    end
  ): \(
      if .extra.severity == \"CRITICAL\" then \"🚨 [CRITICAL]\"
      elif .extra.severity == \"ERROR\" then \"🔴 [HIGH]\"
      elif .extra.severity == \"WARNING\" then \"⚠️ [MEDIUM]\"
      else \"💡 [LOW]\"
    end
  ) \(
    if .extra.metadata.source? != null then
      \"<[\(.check_id)](\(.extra.metadata.source))>\"
    else
      \"<[\(.check_id)](https://semgrep.dev/r/\(.check_id))>\"
    end
  ) \(
    (.extra.message | gsub(\"\n\"; \" \"))
    + (
        if (.extra.metadata.references | length) > 0 then
          \"\n📚 Docs: \" + (.extra.metadata.references | join(\", \"))
        else
          \"\"
        end
      )
  )"
'
