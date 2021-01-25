import com.alibaba.fastjson.JSONObject;

import java.util.HashMap;

public class TFIDFUtil {
    public static Sentence[] ss;
    public static int cnt = 0;

    /**
     * 初始化评论总数，以便计算IDF
     * @param j 评论总数
     */
    public static void init(JSONObject j){
        ss = new Sentence[j.size()+1];

        String str;
        do {
            str = j.getString(cnt + "");
            ss[cnt++] = new Sentence(str);
        }while (str!=null);
    }

    /**
     * 计算该句中每个分词的TF-IDF
     * @param s 句子
     * @return 一个散列表，记录了每个词语及其对应的TF-IDF
     */
    public static HashMap<String, Double> TFIDF(Sentence s){
        HashMap<String, Double> mapTf = TF(s);
        HashMap<String, Double> mapIdf = IDF(s);
        for (String str:mapTf.keySet()){
            mapIdf.put(str, mapTf.get(str)*mapIdf.get(str));
        }
        return mapIdf;
    }

    /**
     * 计算该句中每个分词的TF
     * @param s 句子
     * @return 一个散列表，记录了每个词语及其对应的TF
     */
    private static HashMap<String, Double> TF(Sentence s){
        HashMap<String, Double> map = new HashMap<>();
        int total = 0;
        for (String str:s.segs.keySet()) {
            total += s.segs.get(str);
        }
        for (String str:s.segs.keySet()) {
            map.put(str, (double) s.segs.get(str)/total);
        }
        return map;
    }

    /**
     * 计算该句中每个分词的IDF
     * @param s 句子
     * @return 一个散列表，记录了每个词语及其对应的IDF
     */
    private static HashMap<String, Double> IDF(Sentence s){
        HashMap<String, Double> map = new HashMap<>();
        for (String str:s.segs.keySet()){
            int total = 0;
            for (Sentence sent:ss){
                total += isInSentence(str, sent);
            }
            map.put(str, Math.log((double) ss.length/total));
        }
        return map;
    }

    /**
     * 词语是否在句子中，在返回1，不在返回0
     * @param str 词
     * @param s 句
     * @return 1 or 0
     */
    private static int isInSentence(String str, Sentence s){
        return s.segs.containsKey(str) ? 1 : 0;
    }

}
