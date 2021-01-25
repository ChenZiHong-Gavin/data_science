import com.hankcs.hanlp.HanLP;

import java.util.HashMap;
import java.util.List;

public class Sentence {
    String string;
    public static final int KEYS = 2;
    Word[] words = new Word[KEYS];
    int cnt = 0;
    int polarity = 0;

    public static HashMap<String, Integer> times = new HashMap<>();//未收录在词典中的词语及出现次数

    public Sentence(String s){
        this.string = s;
    }

    /**
     * 将一句话分为几个关键词，默认分成2个关键词
     * @return 关键词的个数
     */
    public int toWords() {
        List<String> keywordList = HanLP.extractKeyword(string, KEYS);
        for (String s:keywordList){
            Word w = Dictionary.dic.get(s);
            if (w==null) {
                //记录下来该词语出现的次数，最后对它们打标签
                times.merge(s, 1, Integer::sum);

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
}
