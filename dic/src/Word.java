public class Word {
    public String name;
    public String emotion;
    public int strength = 0;
    public int polarity = 0;

    public Word(String name, String emotion, String strength, String polarity){
        this.name = name;
        this.emotion = emotion;
        this.strength = Integer.parseInt(strength);
        this.polarity = Integer.parseInt(polarity);
        this.polarity = this.polarity==2 ? -1 : this.polarity;
    }

    public Word(String name, String emotion){
        this.name = name;
        this.emotion = emotion;
    }

    public String toString(){
        return this.name + "," + this.emotion + "," + this.strength + "," + this.polarity + "\n";
    }
}
