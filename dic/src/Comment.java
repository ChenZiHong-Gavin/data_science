import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import java.io.*;

public class Comment {
//    public static final String FILE_PATH = "src/data/weibo标注.csv";
//    public static final String PATH = "src/data/calculate.csv";
    public static final String FILE_PATH = "src/data/分段数据/20.3.10-20.6.json";
    public static final String PATH = "src/data/分段结果/3-6.txt";

    public static final boolean TAG = false;//手动标签模式，默认关闭

    public static File f = new File(FILE_PATH);
    public static int cnt = 0;
    public static int[] times = new int[21];

    public static void main(String[] args) throws IOException {
        JSONObject j = JSON.parseObject(readJsonFile());

        int t = 0;
        try {
            String s = j.getString(cnt+"");cnt++;
            while (s!=null) {
                Sentence comment = new Sentence(s);
                t += comment.toWords();
                for (Word w : comment.words) {
                    if (w!=null)
                        decode(w.emotion);
                }
                s = j.getString(cnt+"");cnt++;
            }

            if (TAG)
                top_N(100);

        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            System.out.println("程序终止，已处理评论:"+(cnt-1));
            System.out.print  ("        已形成词典:");

            Dictionary.toFile();

            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(PATH))));
            int s = 0;
            for (int i=0;i<21;i++){
                bw.write((i+1) + ":" + times[i] + "\n");
                s += times[i];
            }
            bw.write("total emotions:" + s + "\n");
            bw.write("total words:" + t + "\n");
            bw.write("total comments:" + (cnt-1));
            bw.flush();
        }
    }

    /**
     * 给出现频数前N名的词语打标签
     * @param n 前N名
     * @throws IOException
     */
    public static void top_N(int n) throws IOException {
        for (int i = 0; i < n; i++) {
            int max = -1;
            String key = "";
            for (String s: Sentence.times.keySet()) {
                if (max < Sentence.times.get(s)){
                    max = Sentence.times.get(s);
                    key = s;
                }
            }
            tag(key);
            Sentence.times.remove(key);
        }
    }

    /**
     * 给一个词语打标签
     *@param key 要打标签的词语
     */
    public static void tag(String key) throws IOException {
        System.out.println(key + "(" + Sentence.times.get(key) + "次):");
        Word w;

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] str = br.readLine().split(" ");
        if (str.length == 1 && str[0].equals("q")){//退出
            throw new NullPointerException("已退出程序");
        }else if (str.length==1 && str[0].equals("")) {//无情绪
            w = new Word(key, "None");
        }else {
            while (str.length != 3) {//输入格式错误
                System.out.println("Wrong input!");
                str = br.readLine().split(" ");
            }
            w = new Word(key, str[0], str[1], str[2]);
        }

        Dictionary.dic.put(key, w);
        br.close();
    }

    /**
     * 该情绪的出现次数++
     * @param emotion 情绪
     */
    public static void decode(String emotion){
        if (emotion.equals("PA")) times[0]++;
        else if (emotion.equals("PE")) times[1]++;
        else if (emotion.equals("PD")) times[2]++;
        else if (emotion.equals("PH")) times[3]++;
        else if (emotion.equals("PG")) times[4]++;
        else if (emotion.equals("PB")) times[5]++;
        else if (emotion.equals("PK")) times[6]++;
        else if (emotion.equals("NA")) times[7]++;
        else if (emotion.equals("NB")) times[8]++;
        else if (emotion.equals("NJ")) times[9]++;
        else if (emotion.equals("NH")) times[10]++;
        else if (emotion.equals("PF")) times[11]++;
        else if (emotion.equals("NI")) times[12]++;
        else if (emotion.equals("NC")) times[13]++;
        else if (emotion.equals("NG")) times[14]++;
        else if (emotion.equals("NE")) times[15]++;
        else if (emotion.equals("ND")) times[16]++;
        else if (emotion.equals("NN")) times[17]++;
        else if (emotion.equals("NK")) times[18]++;
        else if (emotion.equals("NL")) times[19]++;
        else if (emotion.equals("PC")) times[20]++;
    }

    /**
     * 读取一个json文件，以字符串形式返回
     * @return json文件内容
     */
    public static String readJsonFile() {
        String jsonStr = "";
        try {
            Reader reader = new InputStreamReader(new FileInputStream(f));
            int ch = 0;
            StringBuilder sb = new StringBuilder();
            while ((ch = reader.read()) != -1) {
                sb.append((char) ch);
            }
            reader.close();
            jsonStr = sb.toString();
            return jsonStr;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
