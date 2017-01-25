s.boot;

~b = (-8,-7..8).collect{|i| Buffer.read(s, thisProcess.nowExecutingPath.dirname +/+ "/audio/sine/n" ++ i ++ ".wav") };

(
x = SynthDef("tutorial-PlayBuf",{ arg out = 0,  amp = 0.9,  bufnum;
    Out.ar( out,
        amp * PlayBuf.ar(2, bufnum, BufRateScale.kr(bufnum))

    )
});
)

x.play(s,[\amp, 0.9, \bufnum, ~b[2]]);

(
OSCdef(\trigger, {|m| x.play(s,[\bufnum, ~b[m[1]], \amp, m[2]]); m.postln;}, "/choice");
)



