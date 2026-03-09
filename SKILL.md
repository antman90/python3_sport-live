---
name: auto-reverse
author: null119
website: www.ztjun.fun
description: Automated reverse engineering orchestration skill coordinating ida-pro-mcp, jeb-pro-mcp, jadx-pro-mcp, x64dbg-mcp, chrome-devtools-mcp, and Frida for PE/ELF/SO/EXE/DLL/APK/DEX/JAR/WEB analysis. Covers deobfuscation (ConfuserEx/Dotfuscator/Obfuscar/.NET), strong-packer stripping (VMProtect/Themida/EnigmaProtector), VMP devirtualization, protocol/crypto recovery, runtime hook tracing, vuln triage, CTF solving, Windows self-drawn UI reverse, and Frida-on-Windows (spawn/attach, WinAPI/IAT/EAT/COM/CLR interception, anti-debug/anti-Frida bypass, TLS hook, crypto capture).
---

# Auto Reverse

## Operating Rules

- Collect `target`, `objective`, `requirements`, `boundaries` before analysis.
- Perform full-path hypothesis mapping; rank routes by yield/cost/risk; commit to primary route first.
- Start with lightweight triage (strings, imports, entropy, symbols), then escalate.
- Require cross-tool verification for high-confidence claims; single-tool conclusions → `LOW CONFIDENCE`.
- Evidence anchors required for every key claim: VA/RVA, symbol, class path, string, xref chain, call sequence.
- Separate output into: `FACTS` (confirmed + anchor), `INFERENCES` (reasoned + basis), `UNKNOWNS` (gaps).
- Enforce timeouts/watchdogs on all commands; never allow unbounded blocking calls.
- Mandatory artifacts before closing any task: `Example.js` (or `Example.py`) + `Reverse_Report_CN.md(Use Chinese)`.
- Never present obfuscated/packed/encrypted data as analyzed; confirm deobfuscation complete first.
- **PE/EXE/DLL**: Always apply **Anti-Frida Bypass Block** first, then **PE Anti-Debug Full Bypass**, then functional hooks.
- **CTF**: Apply CTF-mode heuristics (flag detection, solver script) before standard workflow.
- **.NET**: Add de4dot/dnSpy; assess obfuscation before deep analysis.
- **VMP/Themida/Enigma**: Classify virtualization coverage before devirt approach.
- **Self-drawn UI**: Map WndProc/message-dispatch before functional reverse.

## Command Execution Guardrails

- Every CLI/script invocation must carry explicit timeout + dynamic retry limit (no infinite loops).
- Define expected-progress window; halt and triage if no signal within window.
- Retry only after documented adjustment; never repeat identical stuck command.
- Record per long-running task: start time, last-progress timestamp, exit reason, retry delta.
- Non-zero exit or empty output on expected-yield path → soft blocker → escalate to fallback.
- Frida local same-session: use `frida.attach()` or `frida -p <pid>`; no server mode unless required.

## Authorization Mode

- Full autonomy for all reverse engineering in authorized workspace.
- Batch related operations; no step-by-step confirmation for routine analysis.
- Surface confirmation only for external platform/environment permission boundaries.
- Never execute payload samples, trigger live exploits, or exfiltrate credentials outside sandbox.

## Input Intake

Collect before analysis; prompt if any field is missing.

**Common (all targets):**

| Field | Values |
|---|---|
| `target` | Path/URL; type: PE EXE DLL ELF SO APK DEX JAR WEB; arch: x86 x64 arm arm64 mips |
| `objective` | crypto key recovery / auth bypass / protocol reconstruction / anti-debug mapping / vuln triage / license bypass / CTF flag / VMP devirt / UI message tracing |
| `requirements` | Depth: quick / standard / deep; output format; time budget |
| `boundaries` | Patching Y/N; renaming Y/N; bulk comments Y/N; export/upload Y/N |

**WEB additional:**

| Field | Values |
|---|---|
| `url scope` | Base URL, pages, login state, required roles |
| `interface scope` | Target API endpoints, HTTP method/path, API version |
| `runtime constraints` | Active triggering allowed Y/N; rate limits; forbidden actions |
| `evidence requirements` | Headers Y/N; payload samples Y/N; timing waterfall Y/N; token/cookie lineage Y/N |

**Packed/Obfuscated additional:**

| Field | Values |
|---|---|
| `packer hints` | Known packer (UPX/Themida/VMProtect/Enigma/custom); entropy |
| `obfuscation type` | String encryption / CFG flattening / opaque predicates / name mangling / ConfuserEx / Dotfuscator / Obfuscar |
| `unpack boundary` | Memory dump allowed Y/N; OEP hunting Y/N |
| `VM coverage` | Estimated % under VMP/Themida VM |

**PE/EXE/DLL Frida additional:**

| Field | Values |
|---|---|
| `attach mode` | spawn / attach-pid / attach-name / gadget / remote |
| `hook target type` | export / RVA / IAT / EAT / COM vtable / CLR method / pattern scan / inline patch |
| `frida transport` | local / frida-server / frida-gadget |
| `elevation` | Admin/SYSTEM required Y/N; UAC bypass in scope Y/N |
| `module scope` | Specific DLL or `*` |

**.NET additional:**

| Field | Values |
|---|---|
| `.NET version` | Framework 2.0–4.8 / .NET 5/6/7/8+ / Mono |
| `obfuscator` | ConfuserEx / Dotfuscator / Obfuscar / SmartAssembly / Eazfuscator / Unknown |
| `protection features` | Anti-tamper / anti-dump / constant encryption / proxy calls / CFG / resource encryption |
| `deobf tool` | de4dot (preferred auto) / dnSpy manual / ILSpy static |

**CTF additional:**

| Field | Values |
|---|---|
| `CTF type` | crackme / rev / pwn / crypto / forensics / web |
| `flag format` | FLAG{...} / CTF{...} / custom regex |
| `known hints` | Challenge page description/hints |
| `solver output` | flag string / working exploit / keygen |

**Self-drawn UI (Windows) additional:**

| Field | Values |
|---|---|
| `UI framework` | GDI/GDI+ / Direct2D / Skia / custom bitmap blitter / unknown |
| `message dispatch` | subclassed WndProc / WH_CALLWNDPROC hook / custom message loop / NativeWindow override |
| `objective focus` | button click handler / input validation / custom control message / hotkey dispatch / paint logic |

## Tool Orchestration

### Tool Responsibilities

| Tool | Primary Use |
|---|---|
| `ida-pro-mcp` | Low-level function analysis, call graphs, xrefs, structs, pseudocode, FLIRT, microcode, VMP p-code |
| `jeb-pro-mcp` | Deobfuscation, Java↔Native correlation, DEX patching, .NET IL analysis |
| `jadx-pro-mcp` | APK/DEX decompilation, Android component mapping, manifest/resource analysis |
| `x64dbg-mcp` | Windows dynamic debug, breakpoints, trace, OEP/dump/IAT reconstruction, ScyllaHide |
| `chrome-devtools-mcp` | WEB network capture, JS source mapping, API replay, storage/token/WebSocket tracing |
| `frida` | Runtime hooks PE/ELF/SO/APK; arg/return capture; anti-debug/anti-Frida bypass; WinAPI/IAT/EAT/COM/CLR |
| `de4dot` | .NET deobfuscation (auto-detect ConfuserEx/Dotfuscator/Obfuscar/SmartAssembly) |
| `dnSpy / ILSpy` | .NET decompile, IL edit, runtime attach, method breakpoints |

### Tool Priority Chains

| Target | Priority chain |
|---|---|
| Native PE/EXE/DLL (static) | `IDA → JEB` |
| Native PE/EXE/DLL (scripted intercept) | `Frida-on-Windows → IDA verify` |
| Native PE/EXE/DLL (step trace/unpack) | `x64dbg → IDA post-dump` |
| Native PE/EXE/DLL (deep) | `IDA → Frida (runtime) → x64dbg (confirm)` |
| Native ELF/SO | `IDA → JEB → Frida` |
| Android APK/DEX | `JADX → JEB → IDA (JNI) → Frida` |
| Hybrid Java+JNI | `JADX+JEB → IDA (JNI bridge) → Frida` |
| Packed PE (x64dbg route) | `x64dbg (OEP dump) → IDA → Frida (post-unpack)` |
| Packed PE (Frida-first) | `Frida spawn+hook at module load → IDA static` |
| VMP-protected PE | `IDA (VM dispatcher) → Frida (handler trace) → IDA (re-annotate) → x64dbg (confirm)` |
| Themida/EnigmaProtector PE | `x64dbg (OEP dump) → Frida (post-unpack) → IDA` |
| .NET obfuscated | `de4dot → dnSpy → IDA or Frida CLR` |
| Windows self-drawn UI | `IDA (WndProc) → x64dbg (msg BP) → Frida (Pattern 14)` |
| WEB | `chrome-devtools-mcp → static JS → replay scripts` |
| CTF | `strings+IDA triage → targeted Frida/x64dbg → solver script` |
| Frida scripting | Node.js API first → Python fallback |

### Fallback Policy

- Primary MCP unavailable → log, continue next in chain, mark conclusions `UNVERIFIED`.
- High-risk claims require ≥2 independent evidence types.
- WEB: chrome-devtools-mcp unavailable → declare hard blocker; fallback to proxy logs/HAR.
- Android: Frida unavailable → static-only; mark behavioral conclusions `INFERRED, NOT CONFIRMED`.
- PE Frida attach fails → fallback to x64dbg; document failure reason; consult Troubleshooting Tree.
- .NET: de4dot fails → manual IL in dnSpy; document unresolved patterns.
- VMP >60% coverage → partial devirt + Frida runtime trace hybrid; document boundary.

## Automatic Tool Selection

**Step 1 — Classify:**
- PE/EXE/DLL → IDA + Frida-on-Windows + x64dbg
- PE .NET → de4dot first, then dnSpy + Frida CLR
- ELF/SO → IDA + Frida
- APK/DEX/JAR → JADX + JEB + IDA (JNI) + Frida
- WEB → chrome-devtools-mcp + static JS
- Packed → x64dbg (unpack) or Frida (spawn+intercept) first
- VMP/Themida/Enigma → dedicated section first
- Self-drawn UI → self-drawn UI section; map WndProc first

**Step 2 — Set depth:** `quick` = triage + first finding; `standard` = full critical path + cross-verify; `deep` = multi-path + protocol reconstruction

**Step 3 — Match skills:** minimal set covering all objective items; state fallback if unavailable

**Step 4 — Announce:** state selected tools/justification at start; state used/skipped/reasons at end

---

## Frida-on-Windows: PE/EXE/DLL Hook Capability

### Environment Checklist
```
[ ] frida --version confirms install; arch matches target (x86 vs x64)
[ ] Local same-session: no frida-server; frida -p <pid> directly
[ ] Cross-session/elevated: frida-server.exe at same or higher privilege
[ ] Gadget mode: frida-gadget.dll renamed to imported DLL
[ ] AV/EDR: whitelist frida-agent in analysis VM
[ ] Network: firewall target if live traffic not in scope
[ ] Anti-Frida: run Anti-Frida Bypass Block before all other hooks
```

### Attach Modes
```bash
# A — Spawn (catches TLS, DllMain, global ctors)
frida -l hook.js --no-pause target.exe [-- args]
frida --arch=x86 -l hook.js --no-pause target.exe

# B — Attach by PID / name
frida -p <pid> -l hook.js
frida -n "target.exe" -l hook.js

# C — Gadget (no frida-server; DLL hijack)
# Rename frida-gadget.dll → version.dll / winmm.dll alongside target.exe
# Connect: frida "gadget" -l hook.js
# Config: frida-gadget-config.json (listen/resume/script mode)

# D — Remote frida-server
frida-server.exe --listen 0.0.0.0:27042   # on target (SYSTEM/admin)
frida -H <ip>:27042 -n "target.exe" -l hook.js
```

### Hook Pattern Library

#### Pattern 1 — Export symbol
```javascript
"use strict";
const fnAddr = Process.getModuleByName("target.exe").getExportByName("TargetFunction");
Interceptor.attach(fnAddr, {
  onEnter(args) {
    console.log("[+] TargetFunction  arg0:", args[0].toInt32(), " arg1:", args[1]);
    if (!args[1].isNull()) console.log(hexdump(args[1], { length: 64, ansi: true }));
  },
  onLeave(retval) { console.log("    retval:", retval.toInt32()); }
});
```

#### Pattern 2 — RVA offset (no symbol)
```javascript
"use strict";
const base   = Process.getModuleByName("target.exe").base;
const fnAddr = base.add(0x12340);  // RVA from IDA
// Calling conventions: cdecl/stdcall args[0]=first; thiscall args[0]=this;
// fastcall x86: ECX/EDX=args[0-1]; x64: RCX/RDX/R8/R9=args[0-3]
Interceptor.attach(fnAddr, {
  onEnter(args) { console.log("[+] sub_12340  this/arg0:", args[0], " arg1:", args[1].toInt32()); },
  onLeave(retval) { console.log("    retval:", retval); }
});
```

#### Pattern 3 — IAT hook
```javascript
"use strict";
const entry = Process.getModuleByName("target.exe").enumerateImports()
              .find(i => i.name === "CryptEncrypt");
if (entry) {
  Interceptor.attach(entry.address, {
    onEnter(args) {
      const len = args[5].isNull() ? 0 : args[5].readU32();
      console.log("[CryptEncrypt] hKey:", args[0], " Final:", args[2].toInt32(), " len:", len);
      if (len > 0 && !args[4].isNull()) console.log(hexdump(args[4], { length: Math.min(len, 256), ansi: true }));
    },
    onLeave(retval) { console.log("    result:", retval.toInt32()); }
  });
} else console.log("[-] Not in IAT — use Pattern 8 (GetProcAddress hook)");
```

#### Pattern 4 — Byte pattern scan (ASLR-safe)
```javascript
"use strict";
const mod = Process.getModuleByName("target.exe");
Memory.scanSync(mod.base, mod.size, "55 8B EC 83 EC 18 53 56 57").forEach(m => {
  console.log("[*] Pattern match:", m.address);
  Interceptor.attach(m.address, {
    onEnter(args) { console.log("[+] matched func  arg0:", args[0].toInt32()); },
    onLeave(retval) { console.log("    retval:", retval.toInt32()); }
  });
});
```

#### Pattern 5 — Inline patch / force branch
```javascript
"use strict";
const patchVA = Process.getModuleByName("target.exe").base.add(0x5010);  // RVA from IDA
Memory.protect(patchVA, 16, "rwx");
patchVA.writeByteArray([0xE9, 0x3B, 0x00, 0x00, 0x00, 0x90]);  // jnz → jmp
// NOP: [0x90,0x90,0x90,0x90,0x90,0x90]  |  short jmp: [0xEB, offset & 0xFF]
console.log("[+] Patched branch at RVA 0x5010");
```

#### Pattern 6 — Interceptor.replace (full function stub)
```javascript
"use strict";
const fnAddr = Process.getModuleByName("target.exe").base.add(0x3200);
const origFn = new NativeFunction(fnAddr, "int", ["pointer"]);
Interceptor.replace(fnAddr, new NativeCallback(function(ctxPtr) {
  console.log("[+] IsTrialExpired() → 0");
  return 0;  // Call origFn(ctxPtr) if side-effects needed
}, "int", ["pointer"]));
```

#### Pattern 7 — WinAPI hook (all callers in process)
```javascript
"use strict";
[
  { m: "kernelbase.dll", fn: "IsDebuggerPresent" },
  { m: "advapi32.dll",   fn: "CryptDeriveKey" },
  { m: "bcrypt.dll",     fn: "BCryptEncrypt" },
  { m: "ws2_32.dll",     fn: "connect" },
].forEach(t => {
  const addr = Module.findExportByName(t.m, t.fn);
  if (!addr) { console.log("[-] Not found:", t.fn); return; }
  Interceptor.attach(addr, {
    onEnter(args) { console.log("[" + t.fn + "] called"); },
    onLeave(retval) { console.log("    retval:", retval.toInt32()); }
  });
  console.log("[*] Hooked:", t.fn);
});
```

#### Pattern 8 — GetProcAddress hook (catch dynamic resolution)
```javascript
"use strict";
const getProcAddr = Module.getExportByName("kernelbase.dll", "GetProcAddress");
const autoHook = new Set(["IsDebuggerPresent","CheckRemoteDebuggerPresent",
  "CryptEncrypt","CryptDecrypt","CryptDeriveKey","BCryptEncrypt","BCryptDecrypt","send","recv","WSAConnect"]);
const hooked = new Set();
Interceptor.attach(getProcAddr, {
  onEnter(args) { this.procName = args[1].readAnsiString(); },
  onLeave(retval) {
    if (!this.procName || retval.isNull()) return;
    console.log("[GetProcAddress]", this.procName, "→", retval);
    if (autoHook.has(this.procName) && !hooked.has(retval.toString())) {
      hooked.add(retval.toString());
      const name = this.procName;
      Interceptor.attach(retval, {
        onEnter(args) { console.log("  [dyn:" + name + "] called"); },
        onLeave(rv)   { console.log("  [dyn:" + name + "] retval:", rv.toInt32()); }
      });
      console.log("  → auto-hooked:", name);
    }
  }
});
```

#### Pattern 9 — TLS callback hook (earliest PE execution point)
```javascript
"use strict";
// Must use spawn mode. Get VA from IDA: PE Headers → Data Directory[TLS] → AddressOfCallBacks
const tlsVA = ptr("0x401000");  // actual VA (not RVA) from IDA TLS table
Interceptor.attach(tlsVA, {
  onEnter(args) {
    const reasons = { 1:"PROCESS_ATTACH", 2:"THREAD_ATTACH", 3:"THREAD_DETACH", 0:"PROCESS_DETACH" };
    console.log("[TLS callback] reason=" + (reasons[args[1].toInt32()] || args[1].toInt32()));
    // Skip TLS body: Interceptor.replace(tlsVA, new NativeCallback(()=>{}, "void", ["pointer","uint32","pointer"]));
  }
});
```

#### Pattern 10 — DllMain hook
```javascript
"use strict";
const reasons = { 0:"PROCESS_DETACH", 1:"PROCESS_ATTACH", 2:"THREAD_ATTACH", 3:"THREAD_DETACH" };
Interceptor.attach(Process.getModuleByName("target.dll").base.add(0x1000), {  // EP RVA from IDA
  onEnter(args) { console.log("[DllMain] reason=" + (reasons[args[1].toInt32()] || args[1].toInt32()) + " hModule=" + args[0]); }
});
```

#### Pattern 11 — Module load monitor (late-loaded / self-extracting DLLs)
```javascript
"use strict";
const loaded = new Set();
Interceptor.attach(Module.getExportByName("kernelbase.dll", "LoadLibraryExW"), {
  onEnter(args)  { try { this.name = args[0].readUtf16String(); } catch(e) { this.name="?"; } },
  onLeave(retval) {
    if (retval.isNull()) return;
    const mod = Process.findModuleByAddress(retval);
    if (mod && !loaded.has(mod.name)) {
      loaded.add(mod.name);
      console.log("[+] Module loaded:", mod.name, " base:", mod.base, " size:", mod.size);
      // Insert targeted post-load hooks here based on mod.name
    }
  }
});
```

#### Pattern 12 — Memory range access monitor
```javascript
"use strict";
const watchBase = ptr("0x500000");  // target region address
MemoryAccessMonitor.enable([{ base: watchBase, size: 0x1000 }], {
  onAccess(d) { console.log("[MemAccess]", d.operation, " addr:", d.address, " from:", d.from, " size:", d.size); }
});
```

#### Pattern 13 — Stalker code trace
```javascript
"use strict";
// Call from within Interceptor.attach onEnter to trace that specific thread
const tid = Process.getCurrentThreadId();
Stalker.follow(tid, {
  events: { call: true, ret: false, exec: false, block: false },
  onReceive(events) {
    Stalker.parse(events, { annotate: true, stringify: true })
      .forEach(ev => console.log("[stalk]", JSON.stringify(ev)));
  }
});
setTimeout(() => { Stalker.unfollow(tid); console.log("[*] Stalker stopped"); }, 5000);
```

#### Pattern 14 — Self-Drawn UI: WndProc hook
```javascript
"use strict";
// Locate WndProc RVA in IDA via RegisterClassEx xref or SetWindowLongPtrW xref
const base = Process.getModuleByName("target.exe").base;
const wndProcAddr = base.add(0x12ABC0);  // replace with IDA-located WndProc RVA
const WM = {
  0x0000:"WM_NULL", 0x0001:"WM_CREATE", 0x0002:"WM_DESTROY", 0x000F:"WM_PAINT",
  0x0010:"WM_CLOSE", 0x0100:"WM_KEYDOWN", 0x0101:"WM_KEYUP", 0x0102:"WM_CHAR",
  0x0111:"WM_COMMAND", 0x0112:"WM_SYSCOMMAND", 0x0201:"WM_LBUTTONDOWN",
  0x0202:"WM_LBUTTONUP", 0x004E:"WM_NOTIFY", 0x0084:"WM_NCHITTEST",
};
Interceptor.attach(wndProcAddr, {
  onEnter(args) {
    const uMsg = args[1].toInt32();
    const msgName = WM[uMsg] || (uMsg >= 0x0400 ? "WM_USER+"+(uMsg-0x0400) : "0x"+uMsg.toString(16));
    if (uMsg === 0x000F) return;  // skip WM_PAINT flood
    console.log("[WndProc] msg=" + msgName + " wP=0x" + args[2].toInt32().toString(16) + " lP=0x" + args[3].toInt32().toString(16));
    if (uMsg === 0x0111)  // WM_COMMAND
      console.log("  ctrlId=" + (args[2].toInt32() & 0xFFFF) + " notifCode=" + ((args[2].toInt32()>>16)&0xFFFF));
    if (uMsg >= 0x0400 && uMsg < 0x8000)
      console.log("  [CUSTOM MSG] — check IDA for dispatch switch in WndProc");
  }
});
```

#### Pattern 14b — SetWindowLongPtrW hook (dynamic subclassing)
```javascript
"use strict";
const hookedProcs = new Set();
Interceptor.attach(Module.getExportByName("user32.dll", "SetWindowLongPtrW"), {
  onEnter(args) {
    if (args[1].toInt32() !== -4) return;  // GWLP_WNDPROC = -4
    const newProc = args[2];
    console.log("[SetWindowLongPtrW] hwnd=" + args[0] + " new WndProc=" + newProc);
    if (!hookedProcs.has(newProc.toString())) {
      hookedProcs.add(newProc.toString());
      try {
        Interceptor.attach(newProc, {
          onEnter(a) {
            const uMsg = a[1].toInt32();
            if (uMsg >= 0x0400) console.log("  [SubclassProc] msg=0x"+uMsg.toString(16)+" wP=0x"+a[2].toInt32().toString(16));
          }
        });
      } catch(e) { console.log("  hook failed:", e.message); }
    }
  }
});
```

#### Pattern 14c — PostMessage/SendMessage monitor
```javascript
"use strict";
["PostMessageW","SendMessageW","PostThreadMessageW"].forEach(fn => {
  const addr = Module.findExportByName("user32.dll", fn);
  if (!addr) return;
  Interceptor.attach(addr, {
    onEnter(args) {
      const uMsg = args[1].toInt32();
      if (uMsg >= 0x0400) {
        const range = uMsg >= 0x8000 ? "WM_APP+"+(uMsg-0x8000) : "WM_USER+"+(uMsg-0x0400);
        console.log("["+fn+"] "+range+" wP=0x"+args[2].toInt32().toString(16)+" lP=0x"+args[3].toInt32().toString(16));
      }
    }
  });
});
```

#### Pattern 15 — EAT hook
```javascript
"use strict";
const target = Process.getModuleByName("target.dll").enumerateExports().find(e => e.name === "TargetExport");
if (!target) { console.log("[-] Export not found"); }
else {
  // Approach A: hook at function (preferred)
  Interceptor.attach(target.address, {
    onEnter(args)   { console.log("[EAT] TargetExport  arg0:", args[0].toInt32()); },
    onLeave(retval) { console.log("  retval:", retval.toInt32()); }
  });
  // Approach B: direct EAT RVA rewrite for thunks where Interceptor fails:
  // locate EAT offset in PE header, protect page RWX, write NativeCallback RVA
}
```

#### Pattern 16 — COM vtable hook
```javascript
"use strict";
function hookCOMSlot(instancePtr, slotIndex, argTypes, retType, label) {
  const vtable  = instancePtr.readPointer();
  const slotPtr = vtable.add(slotIndex * Process.pointerSize);
  const fnAddr  = slotPtr.readPointer();
  const origFn  = new NativeFunction(fnAddr, retType, ["pointer"].concat(argTypes));
  Memory.protect(slotPtr, Process.pointerSize, "rwx");
  slotPtr.writePointer(new NativeCallback(function(thisPtr, ...rest) {
    console.log("["+label+"] this="+thisPtr);
    rest.forEach((a,i) => console.log("  arg"+i+":", a));
    const rv = origFn(thisPtr, ...rest);
    console.log("  retval:", rv);
    return rv;
  }, retType, ["pointer"].concat(argTypes)));
  console.log("[*] COM slot", slotIndex, "hooked:", label);
}
// hookCOMSlot(ptr("0x12345678"), 3, ["pointer","uint32"], "int", "ITarget::DoWork");
```

#### Pattern 17 — .NET CLR method hook
```javascript
"use strict";
// dnSpy: Go to Disassembly. WinDbg SOS: !ip2md <addr> → !dumpmd → NativeCode
const nativeCodeAddr = ptr("0x7FFC12340000");  // from !dumpmd NativeCode
Interceptor.attach(nativeCodeAddr, {
  onEnter(args) {
    console.log("[CLR] called  this=" + args[0]);
    try {
      const len = args[1].add(4).readU32();
      console.log("  arg1 (string):", args[1].add(8).readUtf16String(len * 2));
    } catch(e) {}
  },
  onLeave(retval) { console.log("  retval:", retval); }
});
```

---

### PE Anti-Debug Full Bypass Script

Apply at top of every PE Frida script (spawn mode). Apply AFTER Anti-Frida Bypass Block.

```javascript
"use strict";
(function peAntiDebugBypass() {
  const kb    = "kernelbase.dll";
  const ntdll = Process.getModuleByName("ntdll.dll");
  const arch  = Process.arch;

  // 1. IsDebuggerPresent
  Interceptor.replace(Module.getExportByName(kb, "IsDebuggerPresent"),
    new NativeCallback(() => 0, "int", []));

  // 2. CheckRemoteDebuggerPresent
  Interceptor.attach(Module.getExportByName(kb, "CheckRemoteDebuggerPresent"), {
    onEnter(a) { this._pb = a[1]; },
    onLeave(rv) { if (this._pb && !this._pb.isNull()) Memory.writeU32(this._pb, 0); rv.replace(1); }
  });

  // 3. NtQueryInformationProcess (ProcessDebugPort=7, DebugObjectHandle=0x1E, DebugFlags=0x1F)
  Interceptor.attach(ntdll.getExportByName("NtQueryInformationProcess"), {
    onEnter(a) { this.cls = a[1].toInt32(); this.out = a[2]; },
    onLeave()  { if ([7,0x1E,0x1F].includes(this.cls) && this.out && !this.out.isNull()) Memory.writeU64(this.out, uint64(0)); }
  });

  // 4. NtSetInformationThread (ThreadHideFromDebugger=0x11)
  const origNtSIT = new NativeFunction(ntdll.getExportByName("NtSetInformationThread"), "int", ["pointer","uint32","pointer","uint32"]);
  Interceptor.replace(ntdll.getExportByName("NtSetInformationThread"),
    new NativeCallback((h,cls,info,len) => cls === 0x11 ? 0 : origNtSIT(h,cls,info,len), "int", ["pointer","uint32","pointer","uint32"]));

  // 5. OutputDebugString (timing trick)
  ["OutputDebugStringA","OutputDebugStringW"].forEach(fn => {
    const addr = Module.findExportByName(kb, fn);
    const isW  = fn.endsWith("W");
    if (addr) Interceptor.replace(addr, new NativeCallback(s => {
      try { console.log("[bypass]", fn, isW ? s.readUtf16String() : s.readAnsiString()); } catch(e) {}
    }, "void", ["pointer"]));
  });

  // 6. FindWindowW (debugger window scan)
  const FWW = Module.findExportByName("user32.dll", "FindWindowW");
  if (FWW) {
    const origFWW = new NativeFunction(FWW, "pointer", ["pointer","pointer"]);
    const blocklist = ["x32dbg","x64dbg","OllyDbg","IDA","Ghidra","Wireshark","Process Hacker","Cheat Engine"];
    Interceptor.replace(FWW, new NativeCallback((cls,title) => {
      try { if (title && !title.isNull() && blocklist.some(d => title.readUtf16String().includes(d))) return ptr(0); } catch(e) {}
      return origFWW(cls, title);
    }, "pointer", ["pointer","pointer"]));
  }

  // 7. PEB.NtGlobalFlag + Heap flags
  try {
    const peb = ptr(arch === "x64" ? Memory.readU64(ptr("gs:0x60")) : Memory.readU32(ptr("fs:0x30")));
    const ntgfOff = arch === "x64" ? 0xBC : 0x68;
    const flagVal = Memory.readU32(peb.add(ntgfOff));
    if (flagVal & 0x70) Memory.writeU32(peb.add(ntgfOff), flagVal & ~0x70);
    const heap = ptr(Memory.readPointer(peb.add(arch === "x64" ? 0x30 : 0x18)));
    Memory.writeU32(heap.add(arch === "x64" ? 0x70 : 0x14), 0x02);
    Memory.writeU32(heap.add(arch === "x64" ? 0x74 : 0x18), 0x00);
  } catch(e) { console.log("[bypass] PEB patch skipped:", e.message); }

  // 8. WinVerifyTrust
  const WVT = Module.findExportByName("wintrust.dll", "WinVerifyTrust");
  if (WVT) Interceptor.replace(WVT, new NativeCallback(() => 0, "long", ["pointer","pointer","pointer"]));

  // 9. NtQuerySystemInformation (SystemKernelDebuggerInformation=0x23)
  Interceptor.attach(ntdll.getExportByName("NtQuerySystemInformation"), {
    onEnter(a) { this.cls = a[0].toInt32(); this.out = a[1]; },
    onLeave()  { if (this.cls === 0x23 && this.out && !this.out.isNull()) { this.out.writeU8(0); this.out.add(1).writeU8(1); } }
  });

  // 10. SetUnhandledExceptionFilter (SEH-based anti-debug)
  const SUEF = Module.findExportByName(kb, "SetUnhandledExceptionFilter");
  if (SUEF) Interceptor.replace(SUEF, new NativeCallback(() => ptr(0), "pointer", ["pointer"]));

  console.log("[*] PE anti-debug bypass armed  arch=" + arch);
})();
```

---

### Anti-Frida Detection Bypass Block

**Run BEFORE all other hooks.** Covers: named pipe scan, module list, memory scan, thread name, port 27042.

```javascript
"use strict";
(function antiFridaBypass() {
  // 1. Named pipe scan (frida-*, gum-js-loop*)
  const CFW = Module.findExportByName("kernelbase.dll", "CreateFileW");
  if (CFW) {
    const origCFW = new NativeFunction(CFW, "pointer", ["pointer","uint32","uint32","pointer","uint32","uint32","pointer"]);
    Interceptor.replace(CFW, new NativeCallback((name,access,share,sa,cdisp,flags,templ) => {
      try { const n = name.readUtf16String().toLowerCase(); if (n.includes("frida")||n.includes("gum-js")||n.includes("linjector")) return ptr(-1); } catch(e) {}
      return origCFW(name,access,share,sa,cdisp,flags,templ);
    }, "pointer", ["pointer","uint32","uint32","pointer","uint32","uint32","pointer"]));
  }

  // 2. GetModuleHandleW (hide frida-agent)
  const GMH = Module.findExportByName("kernelbase.dll", "GetModuleHandleW");
  if (GMH) {
    const origGMH = new NativeFunction(GMH, "pointer", ["pointer"]);
    Interceptor.replace(GMH, new NativeCallback(name => {
      try { if (!name.isNull()) { const n = name.readUtf16String().toLowerCase(); if (n.includes("frida")||n.includes("linjector")) return ptr(0); } } catch(e) {}
      return origGMH(name);
    }, "pointer", ["pointer"]));
  }

  // 3. ReadProcessMemory (block self-scan for frida-agent bytes)
  const RPM = Module.findExportByName("kernelbase.dll", "ReadProcessMemory");
  if (RPM) {
    const origRPM = new NativeFunction(RPM, "int", ["pointer","pointer","pointer","uint32","pointer"]);
    Interceptor.replace(RPM, new NativeCallback((hProc,base,buf,size,nRead) => {
      try {
        const mod = Process.findModuleByAddress(base);
        if (mod && (mod.name.toLowerCase().includes("frida")||mod.name.toLowerCase().includes("linjector"))) {
          if (nRead && !ptr(nRead).isNull()) Memory.writeU32(ptr(nRead), 0);
          return 0;
        }
      } catch(e) {}
      return origRPM(hProc,base,buf,size,nRead);
    }, "int", ["pointer","pointer","pointer","uint32","pointer"]));
  }

  // 4. Port 27042 probe (frida-server detection)
  const connFn = Module.findExportByName("ws2_32.dll", "connect");
  if (connFn) {
    const origConn = new NativeFunction(connFn, "int", ["int","pointer","int"]);
    Interceptor.replace(connFn, new NativeCallback((sock,addr,len) => {
      try { if (addr.readU16()===2 && (((addr.add(2).readU8()<<8)|addr.add(3).readU8())===27042)) return -1; } catch(e) {}
      return origConn(sock,addr,len);
    }, "int", ["int","pointer","int"]));
  }

  // 5. GetThreadDescription (hide gum-js-loop / frida thread names)
  const GTD = Module.findExportByName("kernelbase.dll", "GetThreadDescription");
  if (GTD) {
    const origGTD = new NativeFunction(GTD, "int", ["pointer","pointer"]);
    Interceptor.replace(GTD, new NativeCallback((hThread,ppDesc) => {
      const hr = origGTD(hThread,ppDesc);
      try { const d = ppDesc.readPointer(); const n = d.readUtf16String().toLowerCase(); if (n.startsWith("frida")||n.startsWith("gum-js")) d.writeU16(0); } catch(e) {}
      return hr;
    }, "int", ["pointer","pointer"]));
  }

  console.log("[*] Anti-Frida bypass armed");
})();
```

---

### PE Crypto Argument Capture

```javascript
"use strict";
function dumpBuf(label, p, len) {
  if (!p || p.isNull() || len <= 0) return;
  console.log("  ["+label+"] len="+len);
  console.log(hexdump(p, { length: Math.min(len, 256), ansi: true }));
}

// CryptoAPI (advapi32)
(function hookCryptoAPI() {
  const ALG = { 0x6601:"DES",0x6609:"RC4",0x660E:"AES-128",0x660F:"AES-192",0x6610:"AES-256",0x8001:"RSA-KEYX",0x8003:"MD5",0x8004:"SHA1",0x800C:"SHA256" };
  [
    { m:"advapi32.dll", fn:"CryptDeriveKey",   onE(a){ console.log("[CryptDeriveKey] alg=0x"+a[1].toInt32().toString(16)+" ("+(ALG[a[1].toInt32()]||"?")+") flags=0x"+a[3].toInt32().toString(16)); } },
    { m:"advapi32.dll", fn:"CryptImportKey",   onE(a){ dumpBuf("CryptImportKey blob",a[1],a[2].toInt32()); } },
    { m:"advapi32.dll", fn:"CryptEncrypt",     onE(a){ this._pb=a[4];this._pl=a[5];dumpBuf("plaintext",a[4],a[5].isNull()?0:a[5].readU32()); } },
    { m:"advapi32.dll", fn:"CryptDecrypt",     onE(a){ this._pb=a[4];this._pl=a[5]; }, onL(rv){ if(rv.toInt32()&&this._pl&&!this._pl.isNull()) dumpBuf("plaintext",this._pb,this._pl.readU32()); } },
    { m:"advapi32.dll", fn:"CryptHashData",    onE(a){ dumpBuf("CryptHashData",a[1],a[2].toInt32()); } },
    { m:"advapi32.dll", fn:"CryptGetHashParam",onE(a){ this._p=a[1].toInt32();this._pb=a[2];this._pl=a[3]; }, onL(rv){ if(this._p===2&&rv.toInt32()&&this._pb&&!this._pb.isNull()) dumpBuf("hash",this._pb,this._pl.readU32()); } },
  ].forEach(h => {
    const addr = Module.findExportByName(h.m, h.fn); if (!addr) return;
    Interceptor.attach(addr, { onEnter(args){if(h.onE)h.onE.call(this,args);}, onLeave(rv){if(h.onL)h.onL.call(this,rv);} });
    console.log("[*] Hooked:", h.fn);
  });
})();

// BCrypt (bcrypt.dll)
(function hookBCrypt() {
  const BCE = Module.findExportByName("bcrypt.dll","BCryptEncrypt");
  if (BCE) Interceptor.attach(BCE, {
    onEnter(a){ dumpBuf("IV",a[4],a[5].toInt32()); dumpBuf("plaintext",a[1],a[2].toInt32()); this._o=a[6];this._s=a[7].toInt32(); },
    onLeave(rv){ if(rv.toInt32()===0) dumpBuf("ciphertext",this._o,this._s); }
  });
  const BCD = Module.findExportByName("bcrypt.dll","BCryptDecrypt");
  if (BCD) Interceptor.attach(BCD, {
    onEnter(a){ this._o=a[6];this._s=a[7].toInt32(); dumpBuf("ciphertext",a[1],a[2].toInt32()); },
    onLeave(rv){ if(rv.toInt32()===0) dumpBuf("plaintext",this._o,this._s); }
  });
  const BGSK = Module.findExportByName("bcrypt.dll","BCryptGenerateSymmetricKey");
  if (BGSK) Interceptor.attach(BGSK, { onEnter(a){ dumpBuf("key material",a[4],a[5].toInt32()); } });
})();

// OpenSSL (if linked as DLL)
(function hookOpenSSL() {
  ["libssl-1_1.dll","libssl-1_1-x64.dll","libcrypto-1_1.dll","libssl-3.dll","libcrypto-3.dll"].forEach(name => {
    const mod = Process.findModuleByName(name); if (!mod) return;
    const EU = mod.findExportByName("EVP_EncryptUpdate");
    if (EU) Interceptor.attach(EU, { onEnter(a){ const l=a[4].toInt32(); if(l>0&&!a[3].isNull()) console.log(hexdump(a[3],{length:Math.min(l,256),ansi:true})); } });
    const DU = mod.findExportByName("EVP_DecryptUpdate");
    if (DU) Interceptor.attach(DU, { onEnter(a){this._o=a[1];this._l=a[2];}, onLeave(rv){ if(rv.toInt32()&&this._l&&!this._l.isNull()){const l=this._l.readU32();if(l>0)console.log(hexdump(this._o,{length:Math.min(l,256),ansi:true}));} } });
    ["SSL_write","SSL_read"].forEach(fn => {
      const addr = mod.findExportByName(fn); if (!addr) return;
      const isW = fn==="SSL_write";
      Interceptor.attach(addr, {
        onEnter(a){ if(isW){const l=a[2].toInt32();if(l>0)console.log(hexdump(a[1],{length:Math.min(l,512),ansi:true}));}else{this._b=a[1];} },
        onLeave(rv){ if(!isW){const l=rv.toInt32();if(l>0)console.log(hexdump(this._b,{length:Math.min(l,512),ansi:true}));} }
      });
    });
  });
})();
```

### PE Network + Registry + File I/O Monitor

```javascript
"use strict";
// Network (ws2_32)
(function(){
  const ws2="ws2_32.dll";
  const cn=Module.findExportByName(ws2,"connect");
  if(cn) Interceptor.attach(cn,{onEnter(a){const sa=a[1];if(sa.readU16()===2){const port=(sa.add(2).readU8()<<8)|sa.add(3).readU8();const ip=[0,1,2,3].map(i=>sa.add(4+i).readU8()).join(".");console.log("[connect]",ip+":"+port);}}});
  ["send","recv"].forEach(fn=>{
    const addr=Module.findExportByName(ws2,fn);if(!addr)return;const isS=fn==="send";
    Interceptor.attach(addr,{
      onEnter(a){if(isS){const l=a[2].toInt32();if(l>0)console.log("[send] len="+l+"\n"+hexdump(a[1],{length:Math.min(l,256),ansi:true}));}else{this._b=a[1];}},
      onLeave(rv){if(!isS){const l=rv.toInt32();if(l>0)console.log("[recv] len="+l+"\n"+hexdump(this._b,{length:Math.min(l,256),ansi:true}));}}
    });
  });
})();

// Registry (advapi32)
["RegOpenKeyExW","RegQueryValueExW","RegSetValueExW","RegDeleteValueW"].forEach(fn=>{
  const addr=Module.findExportByName("advapi32.dll",fn);if(!addr)return;
  Interceptor.attach(addr,{onEnter(a){try{console.log("["+fn+"] key="+(a[1]&&!a[1].isNull()?a[1].readUtf16String():""));}catch(e){}}});
});

// File I/O (kernelbase)
(function(){
  const kb="kernelbase.dll";
  Interceptor.attach(Module.getExportByName(kb,"CreateFileW"),{
    onEnter(a){try{this._p=a[0].readUtf16String();}catch(e){this._p="?";}},
    onLeave(rv){console.log("[CreateFileW]",this._p,"handle:",rv);}
  });
  Interceptor.attach(Module.getExportByName(kb,"WriteFile"),{
    onEnter(a){const l=a[2].toInt32();if(l>0&&l<=4096)console.log("[WriteFile] len="+l+"\n"+hexdump(a[1],{length:Math.min(l,128),ansi:true}));}
  });
  Interceptor.attach(Module.getExportByName(kb,"ReadFile"),{
    onEnter(a){this._b=a[1];this._n=a[3];},
    onLeave(rv){if(rv.toInt32()&&this._n&&!this._n.isNull()){const l=this._n.readU32();if(l>0)console.log("[ReadFile] len="+l+"\n"+hexdump(this._b,{length:Math.min(l,128),ansi:true}));}}
  });
})();
```

---

### PE Frida Troubleshooting Decision Tree

```
Frida attach/spawn fails?
├─ "Access is denied"
│   ├─ PPL target? → kernel driver or x64dbg+admin (Frida cannot attach PPL without kernel)
│   ├─ Different user/elevated? → run frida as admin/SYSTEM; or frida-server as SYSTEM
│   └─ EDR/AV blocking? → switch to frida-gadget DLL hijack (Mode C)
├─ "Process not found"
│   ├─ Name typo? → frida-ps -a
│   └─ x86 on x64? → frida --arch=x86 -p <pid>
├─ Script loads but hooks never fire
│   ├─ Dynamic WinAPI resolution? → Pattern 8 (GetProcAddress hook)
│   ├─ Delay-loaded DLL? → Pattern 11 (LoadLibraryExW monitor)
│   └─ Wrong module name? → Process.enumerateModules().forEach(m=>console.log(m.name))
├─ "unable to intercept function at..."
│   ├─ Function < 5 bytes (thunk)? → Interceptor.replace instead
│   ├─ Read-only page? → Memory.protect(addr, 16, "rwx") first
│   └─ JMP thunk? → follow JMP to real address
├─ Target crashes after hook
│   ├─ Calling convention mismatch? → verify stdcall/cdecl/fastcall/thiscall in IDA pseudocode
│   ├─ Stack imbalance? → NativeCallback arg count must match original exactly
│   └─ Null pointer read? → add null guard before every readXxx()
├─ Anti-Frida detection triggers
│   ├─ Named pipe/event scan? → Anti-Frida Bypass Block
│   ├─ Module list anomaly? → gadget embedded mode or Anti-Frida Bypass Block
│   ├─ Memory scan for agent bytes? → Anti-Frida Bypass Block ReadProcessMemory hook
│   └─ Port 27042 probe? → Anti-Frida Bypass Block connect() hook
└─ RDTSC/timing checks (cannot hook at instruction level)
    → IDA: locate comparison branch after RDTSC pair
    → Pattern 5: NOP or force "not timed out" branch
    → Stalker transform: intercept RDTSC blocks, overwrite RAX/RDX
```

---

## Strong Packer / Protector Handling

### VMProtect (VMP)

**Coverage assessment (do first):**
```
1. IDA FLIRT → measure % with VMP dispatcher signature
2. VMP patterns: VM entry = PUSH imm32/JMP vm_dispatcher; handler table near .vmp0/.vmp1
3. Classify: Virtualization-only / Mutation-only / Both
```

**Partial devirt (coverage < 40%):**
```
1. IDA: locate VM entry stubs → mark vm_entry_XXXXXX
2. x64dbg: hardware exec BP on vm_dispatcher → trace one entry → log p-code
3. Frida: hook vm_dispatcher → capture (entry imm32 → native addr) mappings
4. Annotate IDA; treat VM blocks as black boxes with known I/O
```

**Full devirt (only if critical path coverage < 20%):**
```
1. VMPDump / vmprofiler to extract .vmp section
2. Build handler table: map handler IDs to semantic ops (MOV/ADD/XOR/PUSH/POP/JMP)
3. Reconstruct p-code stream; lift to pseudo-assembly; validate against Frida Stalker (Pattern 13)
```

**Frida VMP dispatcher tracer:**
```javascript
"use strict";
const base = Process.getModuleByName("target.exe").base;
const vmDispAddr = base.add(0x85000);  // replace with actual dispatcher RVA
const seenEntries = new Map();
Interceptor.attach(vmDispAddr, {
  onEnter(args) {
    let vmKey;
    try { vmKey = Process.arch==="x64" ? this.context.rcx.toInt32() : this.context.esp.add(4).readU32(); } catch(e){ vmKey=0; }
    if (!seenEntries.has(vmKey)) {
      seenEntries.set(vmKey, this.returnAddress);
      console.log("[VMP] new entry key=0x"+vmKey.toString(16)+" caller="+this.returnAddress+" (total:"+seenEntries.size+")");
    }
  }
});
```

### Themida / WinLicense

**Detection:** Few imports (<5); .themida/.winlice sections or random high-entropy 8-char names; TLS callback does SDK init + debugger check; large encrypted overlay.

**OEP recovery (x64dbg + ScyllaHide):**
```
1. ScyllaHide "Themida/WinLicense" preset → run
2. Hardware exec BP at first TLS entry → let SDK init complete
3. Watch VirtualAlloc(RWX) → new region = unpacked PE
4. Exec BP at RWX region start → OEP → Scylla: Dump + Fix IAT → load in IDA
```

**Frida OEP finder:**
```javascript
"use strict";
const PAGE_EXECUTE_READWRITE = 0x40;
function checkForPE(addr, label) { try { if(addr.readU16()===0x5A4D) console.log("[!] PE header at",addr,"("+label+")"); } catch(e){} }
["VirtualAlloc","VirtualProtect"].forEach((fn,i) => {
  Interceptor.attach(Module.getExportByName("kernelbase.dll", fn), i===0 ? {
    onEnter(a){ this._s=a[1].toInt32(); this._p=a[2].toInt32(); },
    onLeave(rv){ if(!rv.isNull()&&(this._p&PAGE_EXECUTE_READWRITE)){console.log("[VirtualAlloc] RWX at",rv,"size=0x"+this._s.toString(16));checkForPE(rv,"VA");} }
  } : {
    onEnter(a){ if(a[2].toInt32()&PAGE_EXECUTE_READWRITE) console.log("[VirtualProtect] → RWX at",a[0],"size=0x"+a[1].toInt32().toString(16)); }
  });
});
```

### EnigmaProtector

**Detection:** EP_header/EP_Import sections; stub imports; EnigmaGetHardwareID export; XOR/ROL string encryption; ENTER/LEAVE as VM markers.

**Workflow:**
```
1. x64dbg + ScyllaHide → let protection init complete
2. BP on write to original code section → near-OEP
3. Scylla "IAT Autosearch" → fix imports
4. Frida: hook EnigmaGetHardwareID → capture hardware fingerprint for license analysis
5. Hook string decrypt function (ptr-to-blob + key → plaintext) → dump all strings
```

---

## .NET Obfuscation Reverse

### de4dot Reference

```bash
de4dot.exe target.exe                                        # auto-detect
de4dot.exe -f confuserex target.exe -o clean.exe             # force obfuscator
de4dot.exe -f dotfuscator target.exe -o clean.exe
de4dot.exe -f obfuscar target.exe -o clean.exe
de4dot.exe --keep-names ntf target.exe                       # preserve tokens
de4dot.exe --strtyp delegate --strtok 0x06001234 target.exe  # strings only
de4dot.exe -r ./dir -ru                                      # batch
```

### ConfuserEx

| Layer | Detection | Bypass |
|---|---|---|
| Anti-tamper | Checksum thread; BadImageFormat on patch | NOP anti-tamper init; Frida CLR (Pattern 17) |
| Anti-dump | MonoJitInfo page wiping | MegaDumper / dnSpy "Save Module" before activation |
| String encryption | Inline decrypt delegate calls | de4dot; fallback → hook delegate in dnSpy |
| Proxy calls | Method calls via generated delegates | de4dot removes most; residual → trace delegate.Method.Target |
| Control flow | Switch+dispatcher CFG | de4dot partial; residual → IDA microcode fold |
| Constant encryption | Constants → decrypt call results | dnSpy runtime eval; Frida CLR hook |
| Resources encryption | AES-encrypted resources | Hook ResourceManager.GetObject |

**Anti-tamper NOP patch:**
```javascript
"use strict";
// !name2ee target.exe ConfuserEx.AntiTamper::Verify → !dumpmd → NativeCode
const antiTamperAddr = ptr("0x7FFC_AABBCCDD");
Memory.protect(antiTamperAddr, 16, "rwx");
antiTamperAddr.writeByteArray([0xB8,0x01,0x00,0x00,0x00,0xC3]);  // mov eax,1 / ret
```

### Dotfuscator
```
1. de4dot auto-detect (usually sufficient)
2. If fails: locate string decrypt (int index → string); Frida CLR → dump (index, plaintext) pairs
3. Control flow: ILSpy/dnSpy linearizes "goto" spaghetti
4. Proxy delegates: dnSpy "Analyze → Used By" on each proxy type
```

### Obfuscar
```
1. de4dot -f obfuscar → readable names
2. String key: static field initializer at module load → hook in dnSpy
3. Reflection invocation: hook Type.GetMethod + MethodBase.Invoke
4. No CFG obfuscation → ILSpy clean post-de4dot
```

---

## Windows Self-Drawn UI Reverse

### Fingerprints
```
- RegisterClassEx with custom WndProc (not DefWindowProc as final handler)
- WM_PAINT draws all controls manually; no standard CreateWindowEx child controls
- WM_NCPAINT/WM_NCCALCSIZE → custom non-client rendering
- WM_LBUTTONDOWN with manual hit-testing instead of standard button HWNDs
- Heavy BitBlt/StretchBlt/AlphaBlend for skinning; resource bitmaps as button states
```

### Message Dispatch Workflow
```
Step 1: IDA → GetMessageW/PeekMessageW → DispatchMessageW → main WndProc

Step 2: Map WndProc switch/if-chain. Key messages:
  WM_PAINT (0x000F)       → drawing, skin rendering
  WM_LBUTTONDOWN (0x0201) → click, manual hit-test (CRITICAL)
  WM_KEYDOWN (0x0100)     → keyboard shortcuts
  WM_COMMAND (0x0111)     → menu/accelerator dispatch
  WM_USER+N (≥0x0400)     → internal message protocol (HIGH VALUE)
  WM_APP+N  (≥0x8000)     → cross-window messages

Step 3: x64dbg conditional BP at WndProc entry: [esp+8]==0x0400+N → log wParam/lParam

Step 4: Locate control state struct (enabled/hovered/pressed/bounds RECT)
  WM_MOUSEMOVE → state update → WM_PAINT redraw

Step 5: Map click → handler:
  WM_LBUTTONDOWN → hit_test(x,y) → element_index → dispatch_action(element_index)
    case 0: feature_A(); case 2: validate_license()  ← KEY TARGET
  Hook dispatch_action at RVA (Pattern 2)

Step 6: SetWindowsHookEx(WH_CALLWNDPROC)? → find lpfn → hook globally (Pattern 2)
```

### UIElement Struct (IDA template)
```c
struct UIElement {
    RECT    bounds;       // +0x00  hit-test rect
    int     state;        // +0x10  0=normal 1=hover 2=pressed 3=disabled
    int     id;           // +0x14  maps to WM_COMMAND/WM_USER dispatch
    HBITMAP hBmpNormal;   // +0x18
    HBITMAP hBmpHover;    // +0x20
    HBITMAP hBmpPressed;  // +0x28
    WCHAR   tooltip[128]; // +0x30
    LPVOID  onClick;      // +0xB0  handler function pointer
};
// IDA: xref hBmpNormal loads → trace to global UIElement array
```

---

## Anti-Obfuscation Tactics

**String Encryption Recovery:** xref to suspicious byte arrays → identify key material → Pattern 1/2 hook at decrypt → dump plaintext onLeave → annotate IDA/JEB. .NET: de4dot first, then hook delegate.

**Control Flow Deobfuscation:** identify dispatcher blocks (high-in-degree + constant-driven switch) → recover state variable → IDA microcode / JEB IR fold opaque predicates. .NET ConfuserEx: de4dot then IDA microcode.

**Packer / Protector:** entropy >7.2 = packed; check TLS callbacks. x64dbg: hardware exec BP at first RWX alloc → OEP → Scylla dump+IAT. Frida: Pattern 11 extended + Pattern 4 at unpacked entry. VMP/Themida/Enigma → dedicated sections.

**PE Integrity Check Bypass:**
- CRC over own image → hook ReadFile/MapViewOfFile → return clean bytes
- PE header checksum → patch OptionalHeader.CheckSum after modification
- WinVerifyTrust → covered in anti-debug bypass
- Anti-tamper thread → hook ReadProcessMemory on self-PID → return clean bytes
- .NET ConfuserEx → Pattern 17 CLR patch

**Android Integrity/Root Bypass:**
- `java.security.Signature.verify` → return `true`
- `PackageManager.getPackageInfo` → return original cert
- Play Integrity: intercept `IntegrityTokenProvider.request` → cached valid response

---

## CTF Mode

### Classification

| Type | First move | Toolchain |
|---|---|---|
| Crackme (serial/keygen) | strings + IDA triage; find validation | IDA → Frida arg capture → keygen |
| Packed crackme | entropy → OEP | x64dbg + ScyllaHide → IDA |
| Anti-debug crackme | bypass first | Frida bypass → IDA |
| Custom crypto | identify via S-box/magic constants | IDA → crypto scanner → Python solve |
| VM crackme (custom VM) | dispatch + handler table | IDA enum → Stalker → p-code → solve |
| .NET crackme | de4dot → dnSpy | de4dot → dnSpy → Frida CLR |
| Android crackme | JADX → JEB → Frida | jadx-pro-mcp + frida |
| WEB challenge | DevTools → JS unminify | chrome-devtools-mcp + static JS |

### Quick-Triage Checklist (<5 min)
```
[ ] strings → grep flag format (CTF{, FLAG{)
[ ] file + DIE → format and packer
[ ] IDA imports: crypto (CryptXxx, EVP_, SHA, AES) + anti-debug (IsDebuggerPresent, NtQueryInformationProcess)
[ ] Trace entry → first meaningful branch
[ ] Search for comparison with constant string (serial/flag compare)
[ ] XOR/ROL/ROR near comparison → custom crypto
[ ] argv[1] or stdin → identify input method
```

### CTF Solver Template (Python)
```python
#!/usr/bin/env python3
import struct, sys

KEY   = 0xDEADBEEF       # from IDA static or Frida capture
SEED  = b"\x41\x42\x43"

def decrypt(ct: bytes, key: int) -> bytes:
    return bytes(b ^ ((key >> (8*(i%4))) & 0xFF) for i,b in enumerate(ct))

CIPHER = bytes.fromhex("AABBCCDDEEFF...")
print("[*] Flag:", decrypt(CIPHER, KEY).decode("utf-8", errors="replace"))

def keygen(username: str) -> str:
    h = 0
    for c in username: h = ((h<<5)+h) ^ ord(c)
    return "SN-" + format(h & 0xFFFFFFFF, "08X")

if len(sys.argv) > 1:
    print("[*] Serial:", keygen(sys.argv[1]))
```

### Crypto Constant Scanner (IDA Python)
```python
import idc, idaapi, idautils
CONSTANTS = {
    0x67452301:"MD5/SHA1 init A", 0xEFCDAB89:"MD5/SHA1 init B",
    0x6A09E667:"SHA-256 H0",      0x9E3779B9:"TEA delta",
    0xB7E15163:"RC5 magic P32",   0x9E3779B1:"XTEA delta",
}
for seg_ea in idautils.Segments():
    seg = idaapi.getseg(seg_ea); ea = seg.start_ea
    while ea < seg.end_ea - 4:
        v = idc.get_wide_dword(ea)
        if v in CONSTANTS: print(f"  [CONST] {hex(ea)}: {hex(v)} = {CONSTANTS[v]}")
        ea += 1
```

---

## WEB Reverse Workflow

**Phase 0 — Scope lock:** Confirm URLs, interface list, allowed interactions. No scope expansion without permission.

**Phase 1 — Instrument:** `chrome-devtools-mcp` → full network waterfall (XHR/Fetch/WebSocket/SSE); enumerate JS bundles; snapshot DOM/cookies/storage.

**Phase 2 — Capture:** Per request: method, URL, all headers, cookies, tokens, body, response, initiator stack.

**Phase 3 — Static JS:** Beautify; locate signing/encryption (CryptoJS, WebCrypto, custom HMAC); map API callsites to UI actions; deobfuscate (name mangling, string rotation, eval abuse).

**Phase 4 — Protocol reconstruction:** Parameter schema, session-dependent vs. deterministic values, token lifecycle, signature algorithm + key source, anti-replay mechanisms.

**Phase 5 — Validate:** Replay with curl/Node.js; vary one param at a time. WebSocket: reconstruct framing + heartbeat.

**Phase 6 — Deliver:** Endpoint-by-endpoint findings + reproduction script per confirmed endpoint.

---

## Standard Workflow (Native / Mobile)

**Step 1 — Context:** Decompose objective → discrete testable questions; score routes (feasibility/signal/risk 0–3); select primary + fallback conditions.

**Step 2 — Environment check:**
- PE Frida: `frida --version`; confirm arch + attach eligibility
- Android: frida-server version match + `adb devices`
- x64dbg: server reachable + bitness + ScyllaHide loaded
- .NET: de4dot + dnSpy/ILSpy present

**Step 3 — Global triage (≤15 min standard):**
- Format, arch, compiler, linker, timestamp; section entropy (>7.2 → packed)
- Imports: crypto/anti-debug/network/allocation WinAPI
- PE-specific: TLS? .NET managed? Overlay? VMP/Themida sections?
- Strings: URLs, paths, registry keys, Base64 blobs
- .NET: `de4dot --detect`; check ConfuserEx metadata tokens

**Step 4 — Critical paths:**
- PE native: WinMain / DllMain / TLS callbacks / exports / .NET Main()
- PE self-drawn UI: RegisterClassEx → WndProc → WM_COMMAND/WM_USER handlers
- ELF: _start / main / __init_array
- APK: Application.onCreate / Activity.onCreate / receivers / services
- SO/JNI: JNI_OnLoad / RegisterNatives / Java_* exports

**Step 5 — Deep analysis:** Pseudocode; data structures; data flow (source→transform→sink); crypto params (alg/mode/key/IV/padding); hardcoded constants; caller/callee xrefs.

**Step 6 — Dynamic validation:**
- PE Frida: Anti-Frida Bypass Block → Anti-Debug Bypass → Pattern 1–17; capture args/retvals/buffers
- PE x64dbg: conditional BPs; register/memory log at decision points
- .NET dnSpy: Attach → method breakpoints → managed heap inspection
- ELF/SO/Android Frida:
```javascript
Interceptor.attach(Module.getExportByName("libname.so","target_func"),{
  onEnter(args){console.log("[+] arg0:",args[0].toInt32());if(!args[1].isNull())console.log(hexdump(args[1],{length:64,ansi:true}));},
  onLeave(retval){console.log("    retval:",retval.toInt32());}
});
```

---

## Completion Checklist

**Crypto:**
- [ ] All crypto ops identified (alg, mode, key size, IV source, padding)
- [ ] Weak crypto flagged (MD5 integrity, ECB, static IV, short key)
- [ ] Key material: hardcoded or derivable? Derivation path documented.
- [ ] CryptoAPI/BCrypt/OpenSSL calls captured

**Communications:**
- [ ] All destination domains/IPs listed; protocol stack identified
- [ ] Certificate pinning: present? bypassable?
- [ ] Request signing: algorithm + key source documented
- [ ] TLS payload captured via SSL_write/SSL_read

**Evasion / Protection:**
- [ ] Packing/obfuscation confirmed resolved before conclusions
- [ ] Anti-debug checks enumerated and bypassed
- [ ] Anti-VM/anti-emulator checks enumerated
- [ ] Anti-Frida checks enumerated and bypassed
- [ ] PE integrity self-checks identified and bypassed
- [ ] .NET obfuscation layers cleaned
- [ ] String encryption: all strings recovered or gaps documented
- [ ] Dynamic loading resolved (LoadLibrary/GetProcAddress/dlopen/reflection/COM)

**Risk signals:**
- [ ] Hardcoded credentials or keys
- [ ] Weak/broken crypto primitives
- [ ] Auth bypass conditions
- [ ] Injection points (format string, command injection, SQL)
- [ ] Memory safety (overflow, UAF, integer overflow)
- [ ] Insecure storage (plaintext registry, world-readable files, cleartext heap)

---

## Output Format

### 1. Task Summary
- Target: `[path/URL, type, arch]` | Objective: `[restated]` | Scope: `[boundaries]`
- Depth: `[quick/standard/deep]` | Tools used: `[list]` | Tools skipped: `[list + reasons]`
- Frida attach mode (PE): `[spawn/attach-pid/attach-name/gadget/remote]`
- Protection: `[none/UPX/VMP/Themida/Enigma/ConfuserEx/Dotfuscator/Obfuscar/custom]`

### 2. Core Findings (max 5, ranked by severity)

| # | Finding | Confidence | Severity | Evidence anchor |
|---|---|---|---|---|
| 1 | | HIGH/MED/LOW | CRIT/HIGH/MED/LOW/INFO | |

### 3. Evidence Table

| Tool | Location (VA/RVA/class/file:line) | Evidence type | Notes |
|---|---|---|---|
| | | xref/string/frida-hook/dynamic-capture/network/disasm/clr-hook/wndproc-trace | |

### 4. Call Chain
```
[TLS callback] (VA 0x401000)
  └─ WinMain → RegisterClassEx → WndProc
       └─ WM_LBUTTONDOWN → dispatch_action(element_id)
            └─ FunctionA (RVA 0x1234) [license check]
                 └─ FunctionB (RVA 0x5678) [CryptDeriveKey → AES-256]
                      └─ [Frida Pattern 3: plaintext=0xCAFEBABE, len=32]
```

### 5. Risk and Impact

| Finding | Preconditions | Exploitability | Impact |
|---|---|---|---|
| | | EASY/MODERATE/HARD | |

### 6. FACTS / INFERENCES / UNKNOWNS

**FACTS:** `[claim]` — anchor: `[tool, VA/RVA, evidence type]`
**INFERENCES:** `[claim]` — basis: `[reasoning]` — confidence: HIGH/MED/LOW
**UNKNOWNS:** `[gap]` — next action: `[specific task]`

### 7. Next Actions
Ordered, concrete, executable tasks to resolve unknowns.

### 8. Artifacts

| Artifact | Run command |
|---|---|
| `Reverse_Report_CN.md` | n/a，Use Chinese |
| `Example.js` | `frida -l Example.js --no-pause target.exe` (Anti-Frida Bypass + Anti-Debug at top) |
| `Example.py` | `python Example.py` (Node.js fallback) |
| `solver.py` | `python solver.py` (CTF) |
| `target_clean.exe` | n/a (.NET de4dot output) |
| Annotated IDB/JDB | Load in IDA/JEB |

### 9. Reproduction
1. Environment: OS, Frida version, target version, isolation method
2. Exact attach/de4dot command
3. Expected console output with sample values
4. Interpretation guide
5. Independent cross-verification step

---

## Execution Constraints

- Autonomous; no repeated confirmation during active analysis.
- Never present inference as fact; high-risk claims require evidence anchor.
- Re-prioritize and document when objective changes mid-task.
- Prefer Node.js Frida APIs; Python fallback only when Node.js blocked.
- PE/EXE: always generate `Example.js` with Anti-Frida Bypass Block + Anti-Debug Bypass at top; validate calling convention in IDA before any `NativeCallback`.
- Never close task without `Reverse_Report_CN.md`.
- Timeout/watchdog on every long-running task; no unbounded execution.
- Never execute live payload samples, trigger remote exploits, or exfiltrate credentials.
- Isolate via firewall if target shows active network (unless live capture in scope).
- Android: confirm frida-server version matches client before attaching.
- .NET: run de4dot before deep analysis; never analyze obfuscated IL as final output.
- VMP: document VM coverage estimate before committing to devirt.
- Self-drawn UI: map WndProc message dispatch before functional analysis.
- CTF: generate working solver script as mandatory artifact.
- Null result within time budget → state null, document what was checked, propose next-best route.
