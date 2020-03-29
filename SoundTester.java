import javax.sound.midi.*;

/**
 *
 * @author togden
 */
public class SoundTester {
    public static SoundSynthesizer audioSource;
    private enum Direction { Down, Up };
    public static void main(String[] args) {
        playChordTab(-9999,7,9,9,8,7);
        waitForMilliseconds(1000);
        audioSource.closeSynthesizer();
    }
    
    
    /*
    Doing this method without a for loop to make it easier for python to
    pass the parameters in.
    */
    public static void playChordTab(int e_, int a, int d, int g, int b, int e) {
        if(audioSource==null) {
            audioSource = new SoundSynthesizer();
        }
        int[] notes = new int[]{0,e,b,g,d,a,e_};
        for(int i = 6; i>0; i--) {
            if(notes[i]!=-9999) {
                audioSource.playNote(Notes.openStrings[i] + notes[i], 80, 50);
            }
        }
        waitForMilliseconds(1000);
    }
    
    public static void initSynthesizer() {
        audioSource = new SoundSynthesizer();
    }
    
    public static void waitForMilliseconds(int time) {
        audioSource.waitForMilliseconds(time);
    }

}
