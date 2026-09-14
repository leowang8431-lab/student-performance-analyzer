# 从这里开始：Student Performance Analyzer v0.1

今天先在 Windows 上运行这份第一版程序。代码先用函数拆分；OOP 重构、
真实数据和 GitHub 协作放在后续阶段。这是 AI 辅助的学习起点，不代表你
已经独立完成整个简历项目。

## 1. 解压并打开文件夹

完整解压 ZIP，不要在压缩包里直接运行。你之前偏好把开发项目放在 F 盘；
本机有 F 盘时可以使用 `F:\Projects\student-performance-analyzer`。
没有 F 盘就使用本机有写入权限的其他普通文件夹。

解压工具可能多包一层同名文件夹。进入**直接包含 main.py、requirements.txt
和 README.md 的那一层**。在 VS Code 通过“文件 / File → 打开文件夹 /
Open Folder”打开，再通过“终端 / Terminal → 新建终端 / New Terminal”
打开 PowerShell。先不要点 C++ 的运行按钮，不用重装编译器。

## 2. 检查环境

两行分开执行：

```powershell
py --version
```

```powershell
git --version
```

Python 应输出版本号，本项目目标为 Python 3.11+。如果找不到 `py`，再执行：

```powershell
python --version
```

打开商店、没有输出或两个命令都不能运行时，先解决 Python 安装/命令识别
问题，不要继续安装依赖。Git 暂时不可用不会阻止本地运行 Python，上传前
再处理即可。安装并不意味着必须重装 VS Code 或 C++ 环境。

## 3. 创建项目自己的 Python 环境

在包含 requirements.txt 的项目目录执行：

```powershell
py -m venv .venv
```

成功通常只会多出 `.venv` 文件夹，不一定有长篇输出。如果上一步只有
`python` 能用，把本步改为 `python -m venv .venv`；两条不用都运行。
虚拟环境默认与其他项目的 Python 包隔离，不要上传 `.venv`。

## 4. 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

出现 ERROR 或网络超时就停在这里检查。requirements.txt 中的兼容版本范围
不代表每个版本组合均已测试，实际测试记录见 docs/TEST_RESULTS.txt。
这里直接调用虚拟环境的 Python，不需要激活脚本、管理员权限或更改执行策略。
安装需要网络；分析程序不调用付费 API，也不上传数据。

## 5. 第一次运行

```powershell
.\.venv\Scripts\python.exe main.py
```

成功时会出现 `Valid records: 24`、`Report saved:` 和 `Chart saved:`。
输出位于 `results/report.md` 和 `results/study_hours.png`。前者可在 VS Code
打开后按 Ctrl+Shift+V 预览，后者直接双击查看。横轴为每周学习时数，纵轴为
考试成绩。再次运行更新生成文件，不更改原始 CSV。

## 6. 运行测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

末尾出现 `OK` 才表示你这次运行的测试通过。包内附带的是另一套测试环境的
结果，不能直接当成你的电脑已经测试通过。

## 今天学会这些词

| English | 中文 | 在代码里找什么 |
| :--- | :--- | :--- |
| DataFrame | 二维数据表 | load_data() |
| Validation | 输入校验 | validate_data() |
| Mean / Median | 均值 / 中位数 | mean() / median() |
| Sample variance | 样本方差 | var(ddof=1) |
| Standard deviation | 标准差 | std(ddof=1) |
| Correlation | 相关性 | correlations() |
| Unit test | 单元测试 | tests/test_analyzer.py |

样本方差使用 n−1 作分母。相关性不等于因果关系。之前规划里的 0.72 是示意，
不是本项目的结果。现在的输出来自附带模拟数据的真实计算，但仍不是现实
学生群体的研究结论。60 分及格也是程序示例规则，不是你学校的评分政策。

不要上传同学真实成绩、姓名、学号或联系方式，不要放入 API key。不要为了
让图好看而悄悄删除记录。下一步亲手修改的任务见 docs/LEARNING_TASKS_zh.md。
本包不会自动创建仓库或操作你的 GitHub 账号。

## 官方资料

- Python 虚拟环境：https://docs.python.org/3/library/venv.html
- pandas 样本标准差：https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html
- pandas 相关系数：https://pandas.pydata.org/docs/reference/api/pandas.Series.corr.html
