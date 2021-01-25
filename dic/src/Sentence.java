import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Sentence {
    String string;

    public static final int KEYS = 2;//关键词的个数
    Word[] words = new Word[KEYS];
    int cnt = 0;

    int polarity = 0;

    public HashMap<String, Integer> segs = new HashMap<>();//句中各词与出现次数
    public HashMap<String, Double> tf_idf;//句中各词及其TF-IDF系数

    public Sentence(String s){
        this.string = s;
    }

    /**
     * 将一句话分为几个关键词，默认分成2个关键词
     * @return 关键词的个数
     */
    public int toWords() {
        for (Term t:HanLP.segment(string)){
            segs.merge(t.word, 1, Integer::sum);
        }

        //利用TF-IDF来提取关键词
        tf_idf = TFIDFUtil.TFIDF(this);
        List<String> keywordList = extraKeys();

        //通过HanLP提取关键词
//        List<String> keywordList = HanLP.extractKeyword(string, KEYS);

        for (String s:keywordList){
            Word w = Dictionary.get(s);
            if (w==null) {
                //记录下来该词语出现的次数，最后对它们打标签
                Dictionary.newWords.merge(s, 1, Integer::sum);

                //【已弃用】即刻对该条消息打标签
//                Comment.tag(s);
            }
            if (w!=null)
                words[cnt++] = w;
        }
        return keywordList.size();
    }

    /**
     * 对这句话中的关键词进行加权，得出这句话的极性
     */
    public void calculate(){
        for (Word w:words){
            this.polarity += w.strength * w.polarity;
        }
    }

    private List<String> extraKeys(){
        ArrayList<String> list = new ArrayList<>();
        for (int i = 0; i < KEYS; i++) {
            list.add(extraKey());
        }
        return list;
    }

    /**
     * 取出一个关键词
     * @return 关键词
     */
    private String extraKey(){
        double max = 0;
        String key = "";
        for (String str:tf_idf.keySet()){
            double ti = tf_idf.get(str);
            if (max < ti){
                max = ti;
                key = str;
            }
        }
        tf_idf.remove(key);
        return key;
    }
}
