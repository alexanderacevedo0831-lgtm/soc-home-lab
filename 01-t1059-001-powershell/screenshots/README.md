# Screenshots (Lab 01 evidence)

| File | What it shows |
|------|---------------|
| `01-atomic-run-and-4104-hunt-terminal.png` | Atomic T1059.001-17 completes, then Get-WinEvent hunt returns 4104 script blocks at 2026-09-19 16:26:52 |
| `02-event-viewer-4104-scriptblocks.png` | PowerShell/Operational log, burst of 4104 "Creating Scriptblock text" events at the same time |
| `noise-triage-sysmon11-prefetch.png` | False-positive triage: Sysmon 11 carried a T1574.010 rule tag, but it was svchost.exe (SYSTEM) writing a Prefetch file on 09-21, unrelated to the test. An ATT&CK tag is a hint, not a verdict. |

These are evidence attachments for [CASE.md](../CASE.md).
