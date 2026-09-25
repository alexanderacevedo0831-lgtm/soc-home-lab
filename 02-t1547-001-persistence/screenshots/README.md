# Screenshots (Lab 02 evidence)

VM clock is UTC+2, so `TimeCreated` and taskbar times read about 4:11 to 4:12 AM 9/25/2026. The case file uses Sysmon `UtcTime` (02:11 UTC).

| File | What it shows |
|------|---------------|
| `01-atomic-run-reg-key.png` | Atomic T1547.001-1 "Reg Key Run" details (GUID `e55be3fd-...`, executor command_prompt, ElevationRequired False, REG ADD attack command and REG DELETE cleanup), then `$start = Get-Date; Invoke-AtomicTest T1547.001 -TestNumbers 1` completing with "The operation completed successfully." and exit code 0 |
| `02-sysmon13-setvalue-and-sysmon1.png` | Sysmon 13 SetValue at 02:11:44.997 UTC writing `...\Run\Atomic Red Team` = `C:\Path\AtomicRedTeam.exe`, above the Sysmon 1 process create for `reg.exe` at 02:11:44.966. Both carry ProcessGuid `{aa4fc3ef-d860-6ab5-7d02-000000000700}` and PID 7428. Event 1's RuleName reads T1012 Query Registry, a config mislabel. |
| `03-parent-chain-and-runkey-triage.png` | Rest of the Sysmon 1 record: SHA256, parent `cmd.exe` (PID 3600) with the full `REG ADD` command line. Below it, the HKCU Run key with the legitimate OneDrive and Edge entries next to `Atomic Red Team` → `C:\Path\AtomicRedTeam.exe` |
| `04-containment-and-sweep.png` | Containment commands: payload check (`Test-Path` returns False, no matching process), `Remove-ItemProperty` of the Atomic value, and a sweep of HKCU RunOnce, HKLM Run/RunOnce and the Startup folder. Only the benign HKLM Run entries SecurityHealth and VBoxTray remain. The top line is the end of the `reg export` evidence step ("The operation completed successfully.") |
| `05-post-logon-verification.png` | After log off and log on, a fresh PowerShell `Get-ItemProperty` on HKCU Run shows only OneDrive and Edge. The persistence is gone. |

Not pictured: the Sysmon 12/13 event for the value's removal. It was confirmed on the VM but not screenshotted.

These are evidence attachments for [CASE.md](../CASE.md).
