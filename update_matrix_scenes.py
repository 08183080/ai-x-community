import os
import urllib.request
import time

# ==============================================================================
# 用户使用指南 (USER GUIDE):
# 由于版权限制，我不能直接为您下载电影原片截图。
# 请您在网上找到您心仪的《黑客帝国》剧照/截图的链接（右键复制图片地址），
# 填入下方对应的引号中。
# 填好后运行此脚本，即可自动替换网页中的图片。
# ==============================================================================

# 请在这里填入图片链接 (Direct Image URLs)
image_links = {
    # 场景1：尼奥觉醒 / 电脑屏幕 "Wake up, Neo"
    "scene_1.jpg": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg", 
    
    # 场景2：白兔纹身 / 追随白兔
    "scene_2.jpg": "", 

    # 场景3：母体城市 / 绿色代码雨覆盖的城市
    "scene_3.jpg": "",

    # 场景4：红蓝药丸
    "scene_4.jpg": "",

    # 场景5：墨菲斯和尼奥 / 镜子 / 门
    "scene_5.jpg": "",

    # 场景6：光头小孩 / 弯曲勺子 "There is no spoon"
    "scene_6.jpg": "",

    # 场景7：道场训练 / 剪影 "I know Kung Fu"
    "scene_7.jpg": "",

    # 场景8：大厅枪战 / 很多枪
    "scene_8.jpg": "",

    # 场景9：尼奥飞行 / 结尾
    "scene_9.jpg": ""
}

# 目标文件夹
save_dir = r"d:\AI+X web\images\matrix\scenes"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

print(">>> 开始更新黑客帝国剧照...")
print(f">>> 目标文件夹: {save_dir}")

headers = {'User-Agent': 'Mozilla/5.0'}

for filename, url in image_links.items():
    if not url:
        print(f"Skipping {filename}: URL is empty (Please edit the script to add URL)")
        continue
        
    file_path = os.path.join(save_dir, filename)
    try:
        print(f"Downloading {filename} from {url[:30]}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"√ Success: {filename}")
    except Exception as e:
        print(f"X Failed {filename}: {e}")

print("\n>>> 更新完成！请刷新 matrix.html 查看效果。")
