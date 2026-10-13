# fhir-ortho-toolkit

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

骨科植入物唯一标识（UDI）的 HL7 FHIR R4 轮廓参考实现：Device（含 UDI carrier）、Patient、Procedure（THA/TKA）、Observation 的资源构造器与示例。定位为互操作参考实现，面向 HL7 社区征询。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增轮廓：在 `BUILDERS` 注册表加一个资源构造器即可。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- 资源构造器：Device(UDI) / Patient / Procedure(THA,TKA) / Observation 返回规范 FHIR R4 dict
- 示例输出：CLI `--resource Device --example` 打印可校验的 JSON
- UDI carrier 建模：DI/PI 拆分 + carrierHRF/carrierAIDC
- 零依赖 + 规范仓姿态（CC0，便于 HL7 社区直接采用）

**上游投稿目标**：HL7 community / chat.fhir.org

## 内容说明

本仓是互操作参考实现（非产品）：把骨科 UDI 如何映射到 FHIR 讲清楚，供 HL7 社区 chat.fhir.org 征询与 IG PR；以个人专家身份参与标准轨道。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/fhir_ortho.py --resource Device --example
python scripts/fhir_ortho.py --resource Procedure --example
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/fhir-ortho-toolkit.git && cd fhir-ortho-toolkit
python scripts/fhir_ortho.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/fhir-ortho-toolkit/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [omop-ortho-toolkit](https://github.com/stevenzhao07/omop-ortho-toolkit)
- [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)

## 许可

CC0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
