# SOC Home Lab

Purple-team style home lab portfolio for **SOC analyst** skill-building: emulate ATT&CK techniques on an owned Windows VM, **detect** with host sensors, investigate, write cases, then level into **contain / block**.

> All activity is authorized testing on my own VirtualBox lab (`SOC-LAB1`). No production systems. No unauthorized access.

## Lab host

| Item | Detail |
|------|--------|
| Hypervisor | Oracle VirtualBox on Windows lab PC (Blair) |
| Guest | Windows 11 Enterprise Evaluation — `SOC-LAB1` |
| Sensors | Sysmon (modular config), PowerShell Script Block Logging (**4104**), Process Creation (**4688** + cmdline) |
| Emulation | [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) (scoped tests only) |

## Labs

| # | Folder | Technique | Focus | Status |
|---|--------|-----------|--------|--------|
| 01 | [01-t1059-001-powershell](./01-t1059-001-powershell/) | T1059.001 PowerShell | Detect + investigate + CASE | **Complete (detect)** |
| 02 | [02-t1547-001-persistence](./02-t1547-001-persistence/) | T1547.001 Registry Run Keys | Persist + **contain** | Planned |

## Lab 01 highlights

- Emulated **only** Atomic `T1059.001` test **#17**
- Confirmed **4104** scriptblock telemetry at execution time
- Documented escalate / contain / block playbook (stretch — detect lab first)
- Visuals: tooling stack + Detect vs Block
- Evidence screenshots in [screenshots/](./01-t1059-001-powershell/screenshots/), including a false-positive triage example

See [CASE.md](./01-t1059-001-powershell/CASE.md).

## Diagrams (Lab 01)

| Diagram | File |
|---------|------|
| Sensor vs simulator stack | [soc-lab1-tooling-stack.png](./01-t1059-001-powershell/diagrams/soc-lab1-tooling-stack.png) |
| Detect vs Block | [detect-vs-block.png](./01-t1059-001-powershell/diagrams/detect-vs-block.png) |

## Threat context: why these labs, in this order

Labs are chosen by working backwards from what attackers want. Most intrusions are financially motivated, and ransomware crews often buy access from Initial Access Brokers, so the cheapest place to stop them is the first few days after login.

| Slide | File |
|-------|------|
| Who's who in the attack economy (CIS, DPRK, IAB, infostealers) | [attacker-terms-map.png](./threat-context/attacker-terms-map.png) |
| How access gets sold: the criminal supply chain | [iab-forum-supply-chain.png](./threat-context/iab-forum-supply-chain.png) |
| From bought access to payday: hospital scenario | [iab-to-payday-hospital.png](./threat-context/iab-to-payday-hospital.png) |
| Ransomware kill-path vs. hospital, detect + contain per step | [healthcare-ransomware-kill-path.png](./threat-context/healthcare-ransomware-kill-path.png) |

Sources: Mandiant M-Trends, Microsoft Digital Defense Report, public reporting on the 2024 Change Healthcare incident. The forum listing on the supply-chain slide is illustrative, not real.

## What this shows employers

- MITRE mapping and scoped emulation (not “run all atomics”)
- Host-based detection literacy (Sysmon / 4104 / 4688)
- Investigation writeups that separate **detect** from **block**
- Progression toward containment (Lab 02+)

## Disclaimer

Educational portfolio only. Techniques are run exclusively inside an isolated lab VM I own and control.
