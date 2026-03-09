---
name: reverse-multi-track
description: Execute multi-track reverse workflows across anti-analysis bypass, protocol and crypto recovery, CTF solving, and web reverse engineering. Use when the user asks for anti-debug bypass, API or traffic reconstruction, crypto key tracing, CTF flag extraction, JavaScript deobfuscation, or browser-runtime evidence collection.
---

# Reverse Multi Track

## Quick Invoke Template

Copy and fill this template when invoking the skill:

```text
Use reverse-multi-track for this task:
target: <file path or URL>
objective: <what to achieve>
constraints: <time/tool/safety limits>
output: <Example.js|Example.py + Reverse_Report_CN.md>
```

### Fast Presets

```text
[A] Anti-analysis bypass
Use reverse-multi-track:
target: <sample.exe|sample.dll|sample.so>
objective: bypass anti-debug/anti-Frida and recover critical execution path
constraints: no destructive patch, keep process stable, <time budget>
output: Example.js + Reverse_Report_CN.md
```

```text
[B] Protocol and crypto recovery
Use reverse-multi-track:
target: <app binary|apk|service endpoint>
objective: reconstruct signing/encryption pipeline and replay valid request
constraints: no production abuse, controlled traffic only, <time budget>
output: Example.py + Reverse_Report_CN.md
```

```text
[C] CTF solving
Use reverse-multi-track:
target: <challenge file or URL>
objective: obtain valid flag with reproducible solver
constraints: patch allowed yes/no, internet allowed yes/no
output: Example.py + Reverse_Report_CN.md
```

```text
[D] Web reverse
Use reverse-multi-track:
target: <https://example.com/app>
objective: recover API contract and token/signature generation chain
constraints: read-only account, non-destructive requests only
output: Example.js + Reverse_Report_CN.md
```

## 中文快速调用模板

复制后按需填空：

```text
请使用 reverse-multi-track 处理该任务：
target: <文件路径或URL>
objective: <要达成的目标>
constraints: <时间/工具/安全限制>
output: <Example.js|Example.py + Reverse_Report_CN.md>
```

### 中文快捷预设

```text
[A] 反分析绕过
请使用 reverse-multi-track：
target: <sample.exe|sample.dll|sample.so>
objective: 绕过 anti-debug/anti-Frida，恢复关键执行路径
constraints: 不做破坏性patch，保持进程稳定，<时间预算>
output: Example.js + Reverse_Report_CN.md
```

```text
[B] 协议与加密还原
请使用 reverse-multi-track：
target: <app binary|apk|service endpoint>
objective: 还原签名/加密链路并重放有效请求
constraints: 不触发生产滥用，仅限受控流量，<时间预算>
output: Example.py + Reverse_Report_CN.md
```

```text
[C] CTF 解题
请使用 reverse-multi-track：
target: <challenge file or URL>
objective: 获取可验证 flag，并提供可复现实验脚本
constraints: 是否允许 patch（是/否），是否允许联网（是/否）
output: Example.py + Reverse_Report_CN.md
```

```text
[D] Web 逆向
请使用 reverse-multi-track：
target: <https://example.com/app>
objective: 还原 API 协议与 token/signature 生成链
constraints: 只读账号，禁止破坏性请求
output: Example.js + Reverse_Report_CN.md
```

## Purpose

Provide a compact, execution-first playbook that routes tasks into four tracks:
- Anti-analysis bypass
- Protocol and crypto recovery
- CTF solving
- Web reverse and runtime tracing

Always produce reproducible evidence and runnable scripts.

## Intake Checklist

Collect these fields before action:

| Field | Required values |
|---|---|
| `target` | file path or URL; binary/web/challenge type |
| `objective` | bypass / decrypt / reconstruct protocol / get flag / map API |
| `constraints` | time budget, no-crash/no-patch limits, allowed tooling |
| `output` | report format + script language (`js` or `py`) |

If any field is missing, ask once, then continue with the safest default.

## Track Router

Choose the first matching route:

1. **Anti-analysis bypass**: anti-debug, anti-Frida, anti-VM, anti-tamper
2. **Protocol and crypto**: request signing, key schedule, encode/decode chain, custom cipher
3. **CTF solving**: crackme/rev/web challenge with explicit flag goal
4. **Web reverse**: API call chain, token lineage, JS packer/deobfuscation, runtime hook

For hybrid cases, run primary route first and mark secondary route as follow-up.

## Shared Execution Rules

- Start with low-risk triage: strings/imports/symbols/network map.
- Every key claim must have an anchor: function, class, endpoint, offset, or packet sample.
- Mark confidence:
  - `HIGH`: static + runtime agreement
  - `MEDIUM`: single strong source
  - `LOW`: inferred without runtime evidence
- Never leave long-running commands unbounded; always set timeout.
- End with mandatory artifacts:
  - `Example.js` or `Example.py`
  - `Reverse_Report_CN.md`

## Track A: Anti-Analysis Bypass

### Goal
Restore visibility and controllable execution under instrumentation.

### Steps
1. Detect protections (anti-debug API checks, timing checks, integrity checks).
2. Classify bypass layer:
   - environment-level (VM/debugger artifacts)
   - API-level (IsDebuggerPresent, NtQueryInformationProcess, ptrace)
   - logic-level (custom checks, checksum guards)
3. Apply minimal bypass first, then verify behavior delta.
4. Re-run critical path with hooks enabled.

### Minimum Evidence
- At least one protected check location and one bypass proof.
- Before/after behavior snapshot.

## Track B: Protocol and Crypto Recovery

### Goal
Reconstruct request/response semantics and cryptographic transformations.

### Steps
1. Map I/O boundaries (HTTP/WebSocket/native IPC).
2. Identify transform pipeline:
   - canonicalization
   - serialization
   - encryption/signature
   - transport encoding
3. Hook entry and post-transform boundaries.
4. Build replay script that reproduces a valid request.

### Minimum Evidence
- Field mapping table (plaintext -> transformed).
- Key/nonce source hypothesis with verification note.
- One successful replay example.

## Track C: CTF Solving

### Goal
Reach valid flag or solver output quickly and reproducibly.

### Steps
1. Extract challenge metadata (flag regex, known hints, binary/web type).
2. Perform fast triage for likely win path.
3. Decide lane:
   - symbolic/math solving
   - patch-and-run
   - dynamic trace
   - protocol replay
4. Generate solver script with deterministic steps.

### Minimum Evidence
- Exact flag derivation path (or exploit chain).
- One-command reproduction procedure.

## Track D: Web Reverse

### Goal
Recover client-side logic and backend interaction contracts.

### Steps
1. Capture runtime traffic and token lineage.
2. Locate request builder, signer, and obfuscation boundary in JS.
3. Trace key functions with runtime hooks.
4. Rebuild minimal client that reproduces target endpoint behavior.

### Minimum Evidence
- Endpoint table (method, path, auth, critical params).
- Signature/timestamp generation chain.
- Replay script with request sample.

## Output Contract

Deliver in this structure:

```markdown
# FACTS
- Confirmed findings with anchors

# INFERENCES
- Best-effort reasoning with basis

# UNKNOWNS
- Gaps and blockers

# NEXT ACTIONS
- Short, prioritized list
```

Also provide:
- `Example.js` or `Example.py`: runnable and commented only where logic is non-obvious.
- `Reverse_Report_CN.md`: Chinese report with evidence anchors and confidence labels.

## Quality Gate

Before final response, verify:
- At least one runnable script is produced.
- Every major claim has an anchor.
- Confidence labels are present.
- Unknowns are explicit.
- Reproduction steps are concise and complete.
