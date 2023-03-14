# from TextAnalysisTools.text_analysis_tools import DbscanClustering

# import TextAnalysisTools
# print(TextAnalysisTools)
from text_analysis_tools import DbscanClustering
from text_analysis_tools import TopicKeywords
import json

def dbscan_cluster(data_path,
                   eps=0.05, min_samples=3, fig=False):
    """
    基于DBSCAN进行文本聚类
    :param data_path: 文本路径，每行一条
    :param eps: DBSCA中半径参数
    :param min_samples: DBSCAN中半径eps内最小样本数目
    :param fig: 是否对降维后的样本进行画图显示，默认False
    :return: {'cluster_0': [0, 1, 2, 3, 4], 'cluster_1': [5, 6, 7, 8, 9]}   0,1,2....为文本的行号
    """
    pass
    dbscan = DbscanClustering()
    result = dbscan.dbscan(corpus_path=data_path, eps=eps, min_samples=min_samples, fig=fig)
    print("dbscan result: {}\n".format(result))
    return result
    
def tosjson_theme():
    txt_path = './resource/test.txt'
    result = dbscan_cluster(data_path = txt_path)
    
    with open(txt_path, "r", encoding="utf-8") as f:
        data = f.readlines()

    # 转换为 JSON 格式
    json_data = []
    for k, v in result.items():
        json_cluster = {}
        json_cluster["clusterId"] = int(k.split("_")[1])
        text = [data[i].strip() for i in v]
        topic_keywords = TopicKeywords(train_data=text, n_components=1,
                                   n_top_words=3, max_iter=15)
        json_cluster["theme"] = ' '.join(list(topic_keywords.analysis().values())[0])
        json_cluster["num"] = len(v)
        json_cluster["text"] = text
        
        
        json_data.append(json_cluster)

    # 输出为 JSON 文件
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
        print(json_data)
    
    
def clusterTheme():
    pass
    
    
if __name__ == '__main__':
    tosjson_theme()
    

    
    
    
    