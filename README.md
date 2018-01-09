# rainbow6-siege-danmu-request
rainbow6-siege-danmu-request 是一个识别特定格式的直播弹幕
来点播干员的程序。

## 使用方法 Usage
在 ``config.ini`` 中配置直播地址``roomId``和识别关键词``keyword``，
识别的格式为`[关检测][进攻/防守] [探员名]`。

在 CMD 或 PowerShell 中运行 ``python run.py``。

窗口中将会显示点播干员的队列的前三个，按照点播人数和时间排序。

按下 Attacker 或 Defender 按钮来弹出最靠前的一个干员。

## FAQ
Q: 可以用中文名来点播干员吗？

A: 可以。支持的干员名称可以在 ``operator_queue.py`` 中的
 ``Attacker.OP_NAME_DICT`` 和 ``Defender.OP_NAME_DICT`` 
 来查询和修改。

Q: 支持什么直播平台？

A: 目前只测试了 Bilibili 平台下可用。见注。

## 备注 Comment
本程序使用了 [littlecodersh](https://github.com/littlecodersh) 
的弹幕 API 库 [danmu](https://github.com/littlecodersh/danmu). 
由于直播平台的 HTML 改变，该库中部分直播平台无法使用，因此本程序使用了
修改过的本地 danmu 库来支持 Bilibili 的弹幕。
在 danmu 修改后将删除本地库。

其他直播平台的支持取决于 danmu 的情况。
