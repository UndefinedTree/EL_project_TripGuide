# 项目路径说明（我们自己看的readme）

UI界面在UI_ALL文件夹中

API获取在api文件夹中

图标gif在icongif文件夹中

程序运行依赖的第三方库有：dashcope,pillow,openai,python-dotenv。已在requirement.txt中列出。可以自行分别安装，也可打开文件路径后运行-m pip install -r requirement.txt（不同环境指令可能有些许差别）一次性全部安装。安装可能遇到虚拟环境的问题。“win是不是需要虚拟环境我不太清楚呀。明天下床再测一测win了”。安装过程可能遇到很多奇奇怪怪的问题，比如图标非常大多半是安装pillow失败了，很多很多，遇到了再说吧。

另外，请尤其注意travel_hamster_utils.py和icongif文件夹的相对位置。因为前者加载图标的路径搜索依赖此相对位置关系。

好像还有一些需要说说的，但一时半会儿想不起来啦。托某人的福，今天又开始头疼了哈哈哈。孩子要睡了，世界晚安！