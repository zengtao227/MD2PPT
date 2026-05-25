#!/usr/bin/env bash
set -euo pipefail

timeout_seconds="${1:-120}"

osascript - "$timeout_seconds" <<'APPLESCRIPT'
on run argv
  set timeoutSeconds to item 1 of argv as integer
  set startedAt to (current date)

  repeat while ((current date) - startedAt) < timeoutSeconds
    tell application "System Events"
      if exists process "Microsoft PowerPoint" then
        tell process "Microsoft PowerPoint"
          try
            set frontmost to true
          end try

          try
            repeat with w in windows
              set windowName to name of w
              if windowName contains "Grant File Access" then
                my clickFirstExistingButton(w, {"Select", "Select...", "Choose", "OK"})
              end if
              if windowName contains "Please select the folder" then
                my clickFirstExistingButton(w, {"Grant Access", "Open", "Choose", "OK"})
              end if
            end repeat
          end try

          try
            if exists sheet 1 of window 1 then
              my clickFirstExistingButton(sheet 1 of window 1, {"Grant Access", "Open", "Choose", "OK"})
            end if
          end try
        end tell
      end if
    end tell
    delay 0.25
  end repeat
end run

on clickFirstExistingButton(containerRef, buttonNames)
  tell application "System Events"
    repeat with buttonName in buttonNames
      try
        if exists button (buttonName as text) of containerRef then
          click button (buttonName as text) of containerRef
          return true
        end if
      end try
    end repeat
  end tell
  return false
end clickFirstExistingButton
APPLESCRIPT
