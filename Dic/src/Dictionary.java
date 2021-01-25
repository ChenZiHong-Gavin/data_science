import java.io.IOException;
import java.util.HashMap;

public class Dictionary {
    public static HashMap<String,Word> dic = new HashMap<>();
    static {
        try {
            dic = DataUtil.construct();
        } catch (IOException e) {
            e.printStackTrace();
        }
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
