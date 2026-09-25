# Lab 02: Registry Run Key Persistence (T1547.001)

**Status:** Complete (detect + contain + verify)

Emulated Atomic `T1547.001` test #1 on SOC-LAB1, detected the Run key write with Sysmon 1 + 13 (correlated by ProcessGuid), then contained it manually and verified after a fresh logon.

| Item | Link |
|------|------|
| Case writeup | [CASE.md](./CASE.md) |
| Evidence screenshots | [screenshots/](./screenshots/) |
| Diagrams | [persistence-lifecycle.png](./diagrams/persistence-lifecycle.png), [processguid-correlation.png](./diagrams/processguid-correlation.png) |
| Diagram source | [src/](./src/) |
