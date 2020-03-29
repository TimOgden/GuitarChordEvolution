import javax.sound.midi.*;

/**
 *
 * @author togden
 */
public class SoundSynthesizer {

    Synthesizer synthesizer;
    MidiChannel[] mc;
    int guitarPreset = 25;
    int currentChannel = 1;
    public SoundSynthesizer() {
        try {
            synthesizer = MidiSystem.getSynthesizer();
            synthesizer.open();
        } catch (MidiUnavailableException e) {
            System.out.println(e);
            System.out.println("Could not access the default synthesizer!");
        }
        mc = synthesizer.getChannels();
        Instrument[] instruments = synthesizer.getAvailableInstruments();
        Instrument guitar = instruments[guitarPreset];
        synthesizer.loadInstrument(guitar);
        for(int string = 1; string<=6; string++)
            mc[string].programChange(guitar.getPatch().getProgram());
        
    }

    public void playNote(int note, int force, int timeToWait) {
        
        mc[currentChannel].noteOn(note, force);
        if(currentChannel > 6)
            currentChannel = 1;
        else
            currentChannel++;
        waitForMilliseconds(timeToWait);
    }

    public void waitForMilliseconds(int time) {
        try {
            Thread.sleep(time);
        } catch (InterruptedException e) {

        }
    }
    
    public void closeSynthesizer() {
        synthesizer.close();
    }
    
    public void clearOutChannels() {
        for(MidiChannel m : mc)
            m.allNotesOff();
    }

}
