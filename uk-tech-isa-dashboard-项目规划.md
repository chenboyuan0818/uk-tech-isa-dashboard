# 英国科技股 ISA 组合分析仪表盘 — 项目规划

> 项目代号:`uk-tech-isa-dashboard`
> 预计周期:2–3 周
> 目标:完成一个可公开访问的交互式仪表盘,覆盖数据获取、清洗、分析、可视化与部署全流程,作为数据分析作品集项目。
>
> **免责声明:本项目仅供教育与学习用途,不构成任何投资建议。**

---

## 项目总览

| 阶段 | 内容 | 预计时间 | 产出 |
|------|------|----------|------|
| 一 | 环境搭建 | 半天 | GitHub 仓库 + 项目骨架 |
| 二 | 数据获取 | 2–3 天 | `fetch_data.py` + 缓存数据 |
| 三 | 核心分析指标 | 3–5 天 | `analysis.py` + 验证 notebook |
| 四 | Streamlit 仪表盘 | 3–5 天 | `app.py` 四大板块 |
| 五 | 部署上线 | 1 天 | 公开访问链接 |
| 六 | 打磨 README | 1 天 | 作品集级别的项目主页 |

---

## 阶段一:环境搭建(半天)

### 任务清单

- [ ] 在 GitHub 上新建仓库 `uk-tech-isa-dashboard`
- [ ] 本地创建虚拟环境
- [ ] 安装核心依赖
- [ ] 建立项目结构并完成首次 push

### 安装命令

```bash
python -m venv venv
source venv/bin/activate        # Windows 用 venv\Scripts\activate
pip install yfinance pandas numpy matplotlib plotly streamlit
pip freeze > requirements.txt
```

### 项目结构

```
uk-tech-isa-dashboard/
├── data/              # 缓存下来的数据(CSV)
├── src/
│   ├── fetch_data.py  # 取数模块
│   ├── analysis.py    # 指标计算模块
│   └── app.py         # Streamlit 主程序
├── notebooks/         # 探索性分析用的 notebook
├── requirements.txt
└── README.md
```

**习惯养成:小步提交。每完成一个小功能就 commit 一次,写清楚 commit message。**

---

## 阶段二:数据获取(2–3 天)

### 任务清单

- [ ] 选定 5–8 只关注的股票
- [ ] 编写 `fetch_data.py`,用 `yf.download()` 拉取 2–3 年日线数据
- [ ] 数据存为 CSV 放入 `data/` 目录
- [ ] 处理缺失值与异常值
- [ ] 处理英美股票的时区与交易日差异
- [ ] 标注币种(GBP / USD)

### 股票代码提示

伦敦上市股票在 yfinance 中需要加 `.L` 后缀:

| 股票 | 代码 | 市场 | 币种 |
|------|------|------|------|
| Sage Group | `SGE.L` | 伦敦 | GBp(便士) |
| Ocado | `OCDO.L` | 伦敦 | GBp(便士) |
| Auto Trader | `AUTO.L` | 伦敦 | GBp(便士) |
| ARM Holdings | `ARM` | 纳斯达克 | USD |
| Apple | `AAPL` | 纳斯达克 | USD |
| Microsoft | `MSFT` | 纳斯达克 | USD |
| NVIDIA | `NVDA` | 纳斯达克 | USD |

**注意:伦敦股票报价单位是便士(GBp),不是英镑(GBP),做跨市场比较时要统一单位。**

### 工程要点

- yfinance 是非官方接口,偶尔失效或限流,必须加异常处理(try/except)
- 实现本地缓存:已下载的数据优先从 CSV 读取,避免重复请求
- 英美市场交易日不同(节假日不一样),合并数据时注意对齐方式

---

## 阶段三:核心分析指标(3–5 天)

### 任务清单

在 `analysis.py` 中实现以下函数,先在 notebook 里验证正确性,再整理成模块:

- [ ] **日收益率与累计收益率** — `pct_change()` 与累乘
- [ ] **移动平均线** — 20 日、50 日、200 日
- [ ] **年化波动率** — 日收益率标准差 × √252
- [ ] **最大回撤** — 从历史高点的最大跌幅
- [ ] **相关性矩阵** — 检查持仓是否同涨同跌
- [ ] **组合层面指标** — 按设定权重计算组合整体收益与波动

### 验证方法

每个指标先在 `notebooks/` 中的 notebook 里计算并画图,与财经网站(如 Yahoo Finance 页面)上的数字粗略对照,确认逻辑正确后再封装成函数。

---

## 阶段四:Streamlit 仪表盘(3–5 天)

### 任务清单

`app.py` 建议四个板块:

- [ ] **侧边栏** — 选股票、选日期范围、输入各股票权重
- [ ] **板块一:组合总览** — 累计收益曲线、关键指标卡片(总收益、波动率、最大回撤)
- [ ] **板块二:个股页** — 价格 + 均线图、收益分布直方图
- [ ] **板块三:风险页** — 相关性热力图、回撤曲线
- [ ] **板块四:数据表** — 原始数据展示,支持下载 CSV

### 技术要点

- 图表统一用 **Plotly**,交互体验优于 matplotlib
- 用 `st.cache_data` 缓存数据加载,避免每次交互都重新取数
- 权重输入要做校验(总和为 100%)
- 本地调试命令:`streamlit run src/app.py`

---

## 阶段五:部署上线(1 天)

### 任务清单

- [ ] 确认 `requirements.txt` 完整
- [ ] 注册 Streamlit Community Cloud(免费)
- [ ] 连接 GitHub 仓库,选择 `src/app.py` 作为入口
- [ ] 部署并获得公开链接
- [ ] 测试线上版本各功能正常

部署后的公开链接可以直接放进简历和 LinkedIn。

---

## 阶段六:打磨 README(1 天)

### README 应包含

- [ ] 项目动机(一两段,说明为什么做这个项目)
- [ ] 线上 Demo 链接
- [ ] 仪表盘截图(2–3 张)
- [ ] 技术栈说明(Python、Pandas、yfinance、Plotly、Streamlit)
- [ ] 本地运行步骤
- [ ] 项目收获(学到了什么)
- [ ] 免责声明(仅供教育用途,不构成投资建议)

---

## 隐私与安全提醒

1. **不要**把真实持仓金额、账户信息写进公开仓库,权重用假设值即可
2. **不要**在代码中硬编码任何 API key 或个人信息
3. 免责声明要放在 README 和仪表盘页面显眼位置

---

## 后续可扩展方向(第一版完成后)

- 加入基准对比(如 FTSE 100 或 NASDAQ 100 指数)
- 加入汇率换算,统一以 GBP 展示组合价值
- 加入夏普比率等风险调整后收益指标
- 用 GitHub Actions 定时更新数据
