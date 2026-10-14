#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fhir_ortho.py — 骨科植入物 UDI 的 HL7 FHIR R4 轮廓构造器
=========================================================
输出规范 FHIR R4 资源：Device(含 UDI carrier) / Patient /
Procedure(THA,TKA) / Observation。规范仓（CC0），投 HL7 社区。
零依赖（仅 Python 3.8+ 标准库）。
"""
from __future__ import annotations
import sys
import argparse
import json

BUILDERS = {}


def builder(name):
    def deco(fn):
        BUILDERS[name] = fn
        return fn
    return deco


@builder("Device")
def device_example() -> dict:
    # UDI carrier 的 system URI 已按 FHIR 规范核实（2026-10-12）：
    #  - issuer：R4/R5 规范定义 http://hl7.org/fhir/NamingSystem/gs1-di（GS1 发码机构）
    #  - jurisdiction：R4 规范文本仅示例 fda-udi；R5 起定义 us-fda-udi / eu-ec-udi；
    #    **NMPA 无规范 URI**，故本示例用保留示例域自声明命名空间，不占 hl7.org。
    #  - 这些 URI 是命名空间标识符约定，并非可解析的 NamingSystem 资源（THO 未发布）。
    # Device.type 不硬写 SNOMED 码：原 304120007 经核实为髋假体相关概念（ccdakit
    # 示例标注 "Left Total Hip Prosthesis"），与本膝假体示例 display 不符，已移除；
    # 已核实的膝关节置换手术概念（77465005 / 609588000）放在 Procedure 资源上。
    return {
        "resourceType": "Device",
        "id": "ortho-implant-001",
        "type": {"text": "全膝关节置换植入物"},
        "udiCarrier": [
            {
            "deviceIdentifier": "09876543210987",
            "issuer": "http://hl7.org/fhir/NamingSystem/gs1-di",
            "jurisdiction": "http://example.org/fhir/NamingSystem/nmpa-udi",
            "carrierHRF": "(01)09876543210987(11)260101",
                "carrierAIDC": "eyJE...",
                "entryType": "unknown"
            }
        ],
        "status": "active"
    }


@builder("Patient")
def patient_example() -> dict:
    return {
        "resourceType": "Patient",
        "id": "patient-001",
        "gender": "female",
        "birthDate": "1962-05-14"
    }


@builder("Procedure")
def procedure_example() -> dict:
    # SNOMED 609588000 = "Prosthetic total arthroplasty of knee joint (procedure)"
    # （SNOMED 官方 Editorial Guide，2026-10-12 核实）；77465005 = "Total knee replacement"
    # （OHDSI/Epic 表型实践）为同义常用码。勿再使用未经核实的 SNOMED 数字。
    return {
        "resourceType": "Procedure",
        "id": "proc-tka-001",
        "status": "completed",
        "code": {"coding": [{"system": "http://www.ama-assn.org/go/cpt", "code": "27447",
                             "display": "Total knee arthroplasty"},
                            {"system": "http://snomed.info/sct", "code": "609588000",
                             "display": "Prosthetic total arthroplasty of knee joint (procedure)"}],
                 "text": "全膝关节置换术 (TKA)"},
        "subject": {"reference": "Patient/patient-001"},
        "usedReference": [{"reference": "Device/ortho-implant-001"}]
    }


@builder("Observation")
def observation_example() -> dict:
    # LOINC 100207-0 = "Post-op total score [Knee Society Score]"（满分 100，各分项之和，
    # 与 demo 的 92 一致）。已一手核实 loinc.org/100207-0（2026-10-12）。
    # 纠错记录：83612-6 是**无效校验位** LOINC 码（官网拒识并指向 83612-2=外科护士记录），
    # 与 UDI/KSS 均无关；UDI 的正确 LOINC 为 74711-3 "Unique device identifier"。
    return {
        "resourceType": "Observation",
        "id": "obs-kss-001",
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org", "code": "100207-0",
                             "display": "Knee Society Score (post-op total score)"}],
                 "text": "Knee Society Score"},
        "subject": {"reference": "Patient/patient-001"},
        "valueInteger": 92
    }


def _demo() -> int:
    print(json.dumps(device_example(), ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="骨科 FHIR 轮廓构造器")
    ap.add_argument("--demo", action="store_true", help="输出 Device 示例资源")
    ap.add_argument("--selftest", action="store_true", help="跑内置自测（断言 + 负对照 + xfail）")
    ap.add_argument("--resource", choices=list(BUILDERS.keys()),
                    help="Device/Patient/Procedure/Observation（--demo 时默认 Device）")
    ap.add_argument("--example", action="store_true", help="输出示例资源 JSON")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()
    if args.demo:
        return _demo()
    if args.example:
        res = BUILDERS[args.resource or "Device"]()
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    if args.resource:
        res = BUILDERS[args.resource]()
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    ap.print_help()
    return 2


# ==================== 内置自测（--selftest） ====================
# 由 conformance 补丁于 2026-10-14 生成（生成器 v2）。
# 特性：端到端 CLI 调用 + 内容断言 + 负对照 + xfail（已知缺陷显式标注，不掩盖）。
_SELFTEST_CASES = [(['--demo'], 0, [], [], None), (['--resource', 'Patient'], 0, ['resourceType'], [], None), (['--example'], 0, [], [], '已声明但未实现：--example 在 help 中存在，main() 无对应分支，实际 rc=2')]


def _selftest() -> int:
    import os as _os
    import subprocess as _sp
    _here = _os.path.dirname(_os.path.abspath(__file__))
    # 仓库根：脚本位于 <repo>/scripts/ 时取上一级；否则取脚本所在目录
    _root = _os.path.dirname(_here) if _os.path.basename(_here) == "scripts" else _here
    _script = _os.path.abspath(__file__)
    _fail, _xfail, _n = [], [], 0
    for _case in _SELFTEST_CASES:
        _args, _rc, _must, _mustnot = _case[0], _case[1], _case[2], _case[3]
        _reason = _case[4] if len(_case) > 4 else None
        _n += 1
        _p = _sp.run([sys.executable, _script] + _args, capture_output=True, cwd=_root)
        _out = _p.stdout.decode("utf-8", "replace")
        _bad = []
        if _p.returncode != _rc:
            _bad.append(f"rc={_p.returncode} 期望 {_rc}")
        for _m in _must:
            if _m not in _out:
                _bad.append(f"输出缺少 {_m!r}")
        for _m in _mustnot:
            if _m in _out:
                _bad.append(f"输出含禁止内容 {_m!r}")
        if _rc == 0 and not _out.strip():
            _bad.append("rc=0 但输出为空（假绿）")
        if _bad:
            if _reason:
                _xfail.append(f"xfail args={_args}：{'；'.join(_bad)} ← 已知缺陷：{_reason}")
            else:
                _fail.append(f"args={_args}：{'；'.join(_bad)}")
    # 通用负对照：未知参数必须非零
    _n += 1
    _p = _sp.run([sys.executable, _script, "--__nonexistent_flag__"], capture_output=True, cwd=_root)
    if _p.returncode == 0:
        _fail.append("负对照失败：未知参数竟返回 0")
    for _x in _xfail:
        print("[selftest][xfail] " + _x)
    if _fail:
        print(f"[selftest] FAILED {len(_fail)}/{_n}")
        for _f in _fail:
            print("  - " + _f)
        return 1
    print(f"[selftest] PASS {_n - len(_xfail)}/{_n}（含负对照；xfail {len(_xfail)} 项为已知缺陷）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
