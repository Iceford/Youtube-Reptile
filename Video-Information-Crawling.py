import os  # 导入Python内置的os模块
import csv  # 导入Python内置的csv模块
from googleapiclient.discovery import build
# 从googleapiclient包中的discovery模块导入build函数,用于访问Google API服务


api_key = ""  # YouTube API密钥
# 使用Google API构建一个访问YouTube视频服务的客户端对象
youtube = build("youtube", "v3", developerKey=api_key)


"""
函数功能:获取指定YouTube频道的所有视频信息
传入参数:接受一个参数channel_id作为要获取视频的频道ID
返回值:返回一个包含所有视频信息的列表videos
"""
def get_channel_videos(channel_id):
    # 定义了空列表video_ids用于保存视频id和变量next_page_token用于存储下一页数据的令牌
    video_ids = []
    next_page_token = None
    # 循环获取下一页视频信息
    while True:
        # 使用googleapiclient.discovery模块的search().list()方法来向YouTube API发送请求
        request = youtube.search().list(
            part="id",  # 要获取的视频的基本信息(如标题、描述和发布时间等)
            channelId=channel_id,  # 要查询的频道ID
            maxResults=50,  # 每页最多返回的视频数
            pageToken=next_page_token,  # 要获取的下一页数据的令牌
            type="video",  # 要查询的资源类型（这里为video，即视频）
        )
        # 执行查询请求并将结果保存到response变量
        response = request.execute()
        # 将YouTube API响应中的视频ID提取出来并添加到现有的视频ID列表中
        video_ids.extend([item["id"]["videoId"] for item in response["items"]])
        # 获取YouTube API响应中的下一页令牌（next page token）的值
        next_page_token = response.get("nextPageToken")
        # 当没有下一页数据时，退出循环
        if next_page_token is None:
            break
    videos = []  # 创建空列表videos用于存储视频详细信息
    for video_id in video_ids:  # 遍历之前提取出的视频id列表
        request = youtube.videos().list(  # 获取特定视频的详细信息
            part="snippet,contentDetails,player,statistics,status", id=video_id)
        response = request.execute()  # 响应包含请求的视频详细信息
        # 通过extend()方法将response中的视频信息添加到videos列表中
        videos.extend(response["items"])
        # 判断是否还有下一页数据，如果有则更新next_page_token变量，并继续循环获取下一页数据
        next_page_token = response.get("nextPageToken")
    # 返回所有视频信息的列表videos
    return videos


"""
函数功能:将指定的YouTube视频信息保存到CSV文件
传入参数:videos表示要保存的视频信息列表,csv_name表示要保存到的CSV文件名
返回值:无
"""
def save_to_csv(videos, csv_name):
    # 使用Python内置的open()方法打开指定文件
    with open(csv_name, mode="w", newline="", encoding="utf-8") as file:
        # 创建一个csv.writer对象来写入CSV格式数据
        writer = csv.writer(file)
        # 使用writerow()方法写入表头行
        writer.writerow(["id", "title", "publishedAt", "duration", "definition", "caption", "licensedContent",
                        "viewCount", "likeCount", "commentCount", "description", "embeddable", "player"])
        # 写入每个视频对应的行
        for video in videos:
            # 视频的详细信息如下
            writer.writerow([
                video["id"],  # YouTube用于唯一标识视频的ID
                video["snippet"]["title"],  # 视频标题
                video["snippet"]["publishedAt"],  # 发布日期和时间
                video["contentDetails"]["duration"],  # 视频时长
                video["contentDetails"]["definition"],  # 清晰度
                video["contentDetails"]["caption"],  # 是否有字幕
                video["contentDetails"]["licensedContent"],  # 是否受版权保护
                video["statistics"].get("viewCount", "N/A"),  # 观看次数
                video["statistics"].get("likeCount", "N/A"),  # 点赞次数
                video["statistics"].get("commentCount", "N/A"),  # 评论次数
                video["snippet"]["description"],  # 视频描述
                video["status"]["embeddable"],  # 视频是否可以嵌入到网页中以播放
                video["player"],  # 视频的嵌入代码，可将其插入到网页中以播放视频
            ])


def run():
    # YouTube频道名称
    channel_name = "李子柒 Liziqi"
    # YouTube频道ID
    channel_id = "UCoC47do520os_4DBMEFGg4A"
    # 获取指定YouTube频道的所有视频信息
    videos = get_channel_videos(channel_id)
    # 将指定的YouTube视频信息保存到csv文件
    save_to_csv(videos, channel_name+".csv")
    # 输出保存文件信息的结果
    print(f"视频信息已保存到 {channel_name}.csv")


# 运行程序
if __name__ == "__main__":
    run()
