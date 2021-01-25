import java.io.*;
import java.util.HashMap;

public class DataUtil {
    public static final String FILE_PATH = "src/data/情感词汇.csv";
    public static File f = new File(FILE_PATH);

    /**
     * 通过文件加载词典
     * @return 词典
     * @throws IOException
     */
    public static HashMap<String, Word> construct() throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(f)));
        HashMap<String, Word> map = new HashMap<>();
        String s = br.readLine();
        while(s!=null){
            String[] slides = s.split(",");
            map.put(slides[0], new Word(slides[0],slides[1],slides[2],slides[3]));
            s = br.readLine();
        }
        return map;
    }

    /**
     * 将词典以文件形式保存
     * @param map 词典
     * @throws IOException
     */
    public static void dic2file(HashMap<String,Word> map) throws IOException {
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f)));
        for (String s:map.keySet()){
            if (map.get(s)!=null)
                bw.write(map.get(s).toString());
        }
        bw.flush();
        bw.close();
    }
}
