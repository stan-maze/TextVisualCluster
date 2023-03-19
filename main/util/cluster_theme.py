
from text_analysis_tools import DbscanClustering
from text_analysis_tools import TopicKeywords

import json
import os

class ClusterTool:
    def __init__(self):
        pass

    def dbscan_cluster(self, data_path = '../resouce/test.xlsx',
                    eps=0.05, min_samples=3, fig=False):
        dbscan = DbscanClustering()
        result = dbscan.dbscan(corpus_path=data_path, eps=eps, min_samples=min_samples, fig=fig)
        return result
        
    def excuteCluster(self, txt_path,
                      eps=0.05, min_samples=3, fig=False):
        print(txt_path)
        result = self.dbscan_cluster(data_path = txt_path, eps=eps, min_samples=min_samples, fig=fig)
        
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
        json_file_path = os.path.splitext(txt_path)[0] + '.json'
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
            print(f'聚类成功，结果保存到 {json_file_path}')

        return json_file_path

    
    
    
    