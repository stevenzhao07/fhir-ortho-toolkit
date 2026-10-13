# AGENTS.md · fhir-ortho-toolkit

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
骨科植入物唯一标识（UDI）的 HL7 FHIR R4 轮廓参考实现：Device（含 UDI carrier）、Patient、Procedure（THA/TKA）、Observation 的资源构造器与示例。定位为规范（spec）仓，投 HL7 社区。

## 运行
```bash
python scripts/fhir_ortho.py --demo
python scripts/fhir_ortho.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增轮廓：在 `BUILDERS` 注册表加一个资源构造器即可。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
