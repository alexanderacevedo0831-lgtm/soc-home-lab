# CASE-001 — Suspicious PowerShell Execution (T1059.001)

| Field | Value |
|-------|-------|
| **Case ID** | CASE-001 |
| **Lab** | SOC-LAB1 (VirtualBox / Windows 11 Enterprise Eval) |
| **Date** | 2026-09-19 |
| **Analyst** | Alexander Acevedo |
| **Severity** | Medium (controlled lab emulation) |
| **Status** | Closed — Detected & Documented |
| **MITRE ATT&CK** | [T1059.001](https://attack.mitre.org/techniques/T1059/001/) — Command and Scripting Interpreter: PowerShell |
| **Emulation** | Atomic Red Team — `T1059.001` Test **#17** only |

---

## 1. Executive summary

On the lab endpoint **SOC-LAB1**, a controlled Atomic Red Team test (`T1059.001-17` — PowerShell Command Execution) was executed to simulate an adversary using PowerShell for command execution. Host sensors (**Sysmon**, **PowerShell Script Block Logging / Event ID 4104**, **Security process creation / Event ID 4688**) recorded the activity. No automated containment was applied in this lab; the objective was **detect → investigate → document**, and to define how a SOC would **escalate / contain / block** next.

**Bottom line:** Initial access-style PowerShell execution was **visible in telemetry**. This is a detect lab, not a block lab.

---

## 2. Environment & sensor stack

| Component | Role |
|-----------|------|
| VirtualBox VM `SOC-LAB1` | Isolated Windows 11 Eval lab (host: Blair) |
| Sysmon + modular config | Process / network / file telemetry |
| Event ID **4104** | PowerShell Script Block Logging (script *content*) |
| Event ID **4688** + cmdline | Process creation auditing |
| Atomic Red Team | Emulation runner (`Invoke-AtomicTest`) |
| Snapshot `clean-desktop` | Rollback baseline before tooling / tests |

**Important:** Sensors **log**; they do not by themselves **block**. Blocking would require Defender ASR, AppLocker/WDAC, EDR isolate, etc. (see §7).

---

## 3. What the attack means

**T1059.001** is one of the most common living-off-the-land techniques. After phishing, exploit, or stolen creds, attackers often use **PowerShell** already on the box to:

- download payloads
- enumerate the host/domain
- disable weak controls
- stage persistence or lateral movement

**What it affects**

- **Confidentiality:** scripts can read files, tokens, browser data
- **Integrity:** can change configs, drop files, alter registry
- **Availability:** less common here, but destructive scripts are possible
- **SOC workload:** noisy if undetected; high-value if you catch script *content* (4104) + parent/child process chain (Sysmon / 4688)

**Interview one-liner:** *"PowerShell isn't malware — abuse of a trusted interpreter is. I correlate 4104 script text with Sysmon process ancestry to tell admin work from suspicious execution."*

---

## 4. Activity performed (emulation)

```text
Import-Module ...Invoke-AtomicRedTeam.psd1
Invoke-AtomicTest T1059.001 -TestNumbers 17 -GetPrereqs
Invoke-AtomicTest T1059.001 -TestNumbers 17
```

Observed runner output (success):

- `T1059.001-17 PowerShell Command Execution` — prereqs defined / ran / **done**

Scope control: **only test #17** (no credential-dumping or unrelated atomics).

---

## 5. Evidence & hunt results

### 5.1 PowerShell Script Block Logging (4104)

**Log:** `Microsoft-Windows-PowerShell/Operational`

**Observed:** Multiple `4104` events at **2026-09-19 ~16:26:51–16:26:52** (lab local time), including multi-part scriptblocks (`1 of N` … `N of N`).

**Why it matters:** 4104 is where you see **what the script said**, not only that `powershell.exe` started.

**Hunt (example):**

```powershell
Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" |
  Where-Object {
    $_.Id -eq 4104 -and
    $_.TimeCreated -ge (Get-Date "2026-09-19 16:26:00") -and
    $_.TimeCreated -le (Get-Date "2026-09-19 16:27:30")
  } |
  Select-Object -First 1 -ExpandProperty Message
```

**GUI path:** Event Viewer → Applications and Services Logs → Microsoft → Windows → **PowerShell** → **Operational**

### 5.2 Process creation (4688) / Sysmon (ID 1)

**Expected artifacts:** `powershell.exe` (and related) process create events with command line near the same timestamp; Sysmon Event ID **1** for process create.

**Hunt (example):**

```powershell
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" |
  Where-Object {
    $_.Id -eq 1 -and
    $_.TimeCreated -ge (Get-Date "2026-09-19 16:26:00") -and
    $_.TimeCreated -le (Get-Date "2026-09-19 16:28:00") -and
    $_.Message -match "powershell"
  } |
  Select-Object -First 3 -ExpandProperty Message
```

**GUI path:** Event Viewer → … → **Sysmon** → **Operational**

### 5.3 Detection logic (SOC-style)

| Signal | Good for |
|--------|----------|
| 4104 + suspicious keywords / encoded command / IEX / download cradles | Script *intent* |
| Sysmon ID 1: odd parent (Office, `wscript`, `msiexec`) → `powershell.exe` | Execution chain |
| 4688 cmdline include | Quick triage when Sysmon absent |

---

## 6. Investigation narrative (how to say it)

1. Alert / hunt window around Atomic run time.
2. Confirm **4104** scriptblocks — identify technique class (PowerShell execution).
3. Pivot to **Sysmon ID 1 / 4688** — parent process, user context, cmdline.
4. Classify: **lab emulation / authorized test** vs true positive.
5. If real: escalate per §7; if lab: close with notes + snapshot hygiene.

---

## 7. Escalate / contain / block (response playbook — Lab 1 stretch goal)

Lab 1 did **not** auto-block. In a real SOC, after confirming malicious PowerShell:

### Escalate
- Open incident; page IR if host is production / crown-jewel / lateral movement suspected
- Capture: hostname, user, PID, cmdline, scriptblock hash/text, network connects

### Contain (host)
- EDR **isolate** network (preferred) or disable NIC on lab host for practice
- Kill suspicious PID tree (`Stop-Process` / EDR kill) **after** evidence capture
- Disable local account / reset creds if theft suspected

### Block / harden (prevent next time)
- **Defender ASR:** e.g. block Office child processes, constrain risky script behavior where compatible
- **WDAC / AppLocker:** allow signed/admin scripts only on high-value hosts
- **CLM** (Constrained Language Mode) for standard users
- Reduce privileged interactive use of PowerShell; prefer JEA / limited endpoints
- Tune detections: alert on `powershell -enc`, `IEX (New-Object Net.WebClient)`, odd parents

**Lab 2 will practice containment** (not only logging).

---

## 8. False positives & analyst judgment

PowerShell is used by IT, Intune, software installers, and legit automation. Reduce noise by:

- Parent/child baselining
- Signed script paths vs user-writable paths
- Time-of-day / user role context
- Allowlists for known management tooling

---

## 9. Lessons learned

1. **Detect ≠ block** — 4104/Sysmon/4688 prove visibility.
2. **Scriptblock logging** is high value for T1059.001 investigations.
3. Scope Atomic tests (**#17 only**) keeps the lab interview-safe and focused.
4. Portfolio value is the **writeup + reasoning**, not reinventing Atomic from scratch.

---

## 10. Artifacts checklist (attach screenshots when exporting portfolio)

- [ ] Atomic success lines for T1059.001-17
- [ ] Event Viewer 4104 detail (full Message)
- [ ] Sysmon ID 1 or 4688 with cmdline
- [ ] This CASE.md

---

## 11. Next lab (level-up)

**Lab 2 (planned):** After initial PowerShell execution, adversaries often **persist**. Lab 2 will emulate a **Registry Run key** persistence technique (MITRE **T1547.001**), detect it with Sysmon registry events, then practice **containment**: remove the Run key, kill related processes, optional network isolate, and verify the persistence is gone. Goal: move from "I found it" to "I stopped the blast radius."
