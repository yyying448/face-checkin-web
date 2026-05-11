# 🎓 全班人脸识别签到系统 (Web 版)

这是一个专为班级场景设计的全栈式人脸识别签到系统。项目不仅实现了本地识别，还通过内网穿透技术支持多名学生同时通过手机浏览器进行远程刷脸签到，并实现了全局数据同步与持久化存储。

### 🚀 功能特点
* **跨设备访问**：利用 Cloudflare 隧道技术，无需安装 App，进入网址即可通过手机摄像头签到。
* **快速识别**：利用 YOLOv11 进行人脸检测，识别精度高。
* **网页化部署**：基于 Streamlit 开发，无需安装环境，点开网址即可签到。
* **实时统计**：自动统计已到人数与未到人数，侧边栏实时显示“已签到”与“未签到”名单.

### 🛠️ 技术栈
*前端展示: Streamlit (Python 快速 Web 框架)
*人脸检测: YOLOv11 (Ultralytics)
*人脸比对: face_recognition (基于 dlib 的深度学习模型)
*网络穿透: Cloudflare Tunnel (cloudflared)
*环境管理: Conda + uv

🚀 快速开始
1. 环境准备
建议使用 Python 3.10 环境：
conda create -n face_checkin python=3.10
conda activate face_checkin
2. 安装依赖
# 建议先安装 opencv 和 dlib 的预编译版本
conda install -c conda-forge opencv dlib
# 安装其余依赖
pip install streamlit ultralytics face_recognition pandas
3. 运行程序
在项目根目录下启动 Streamlit：
streamlit run web_attendance.py
4. 开启远程访问（可选）
如果需要同学通过手机签到，请另开终端运行：
cloudflared tunnel --url http://localhost:8501
分享终端输出的 https://xxxx.trycloudflare.com 链接即可。

### 📂 项目结构说明
web_attendance.py: Web 端主程序逻辑。

yolo11n-face.pt: 预训练的人脸检测模型。

face_db/: 存放已知学生人脸特征的数据库（.pkl 文件）。

requirements.txt: 项目依赖清单。

## 📸 项目效果展示
### 1. 系统主界面
支持实时开启摄像头。
![网页主界面](https://github.com/user-attachments/assets/b5eeda43-cba3-4328-b92b-895c652bb097)

1.1手机界面
<img width="1206" height="1961" alt="78f952d3c01fed3e51b2a09004150593" src="https://github.com/user-attachments/assets/1a3d2ed9-210d-4faf-be20-8e00f3863c1d" />


### 2. 实时识别与侧边栏统计
侧边栏会实时更新当前已签到的人数和名单。
<img width="608" height="1522" alt="af4d2174159eaeeddbc77325d77dc199" src="https://github.com/user-attachments/assets/e6228c50-d0cb-41e7-8913-24e8971df690" />

2.2手机界面同上类似

### 3. 最终识别结果
系统准确识别出人脸，并自动在签到记录中添加姓名、日期和精确时间。
![识别结果展示](https://github.com/user-attachments/assets/8d16a7d0-2860-4ea2-8918-98b8040f1cdb)

### 其他项目说明
由于Cloudflare 的隧道连接很不稳定，所以打开速度会很慢，需要等待，以及苹果手机有安全策略，可能会出现小bug；其次，因为每位同学的照片数量角度有限，所以难免出现识别错误的情况，可以通过调节人脸识别的距离阈值来进行矫正（不过也不一定完美解决）。

