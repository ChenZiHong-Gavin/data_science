import java.io.IOException;
import java.util.HashMap;

public class Dictionary {
    private static HashMap<String,Word> dic = new HashMap<>();
    static {
        try {
            dic = DataUtil.construct();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static HashMap<String, Integer> newWords = new HashMap<>();//未收录在词典中的词语及出现次数

    /**
     * 从词典中搜索一个词语
     * @param s 名称
     * @return 词语
     */
    public static Word get(String s) {
        return dic.get(s);
    }

    /**
     * 将一个词语添加到词典中
     * @param word 词语
     */
    public static void add(Word word){
        dic.put(word.name, word);
    }

    /**
     * 将词典保存为文件
     * @throws IOException
     */
    public static void toFile() throws IOException {
        System.out.println(dic.size());
        DataUtil.dic2file(dic);
    }
}
