# Lab 3: OS Credential Dumping, LSASS Memory (T1003.001)

**Security+ SY0-701 domains reinforced:** Domain 2 (Threats, Vulnerabilities & Mitigations), Domain 4 (Security Operations)

Status: planned. Full spec lives in the curriculum review (LAB3-SPEC.md); CASE-003 will be written here after the run.


---

## Hunt Note (to complete)

Fill in after the lab run, specific to T1003.001 on SOC-LAB1.

1. **Baseline:** What normally opens handles to `lsass.exe` on this host (Defender, `svchost`, `wininit`, etc.) and with what GrantedAccess, so an unusual source process stands out.
2. **Attacker goal:** Why an adversary dumps LSASS memory (what credentials/hashes/tickets they gain).
3. **Blast radius:** What accounts and systems those credentials can reach if the dump succeeds.
4. **Next ATT&CK step:** What typically follows (for example lateral movement with stolen credentials).
5. **What automation/AI triage might miss:** Where an alert pipeline or AI triage could produce a false negative/positive here (for example a Defender block treated as "resolved", or Sysmon 10 not configured for LSASS), and what a human should check.
