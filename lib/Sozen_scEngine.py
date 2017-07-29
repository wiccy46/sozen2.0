## this is python code copied from EmoSonEvolOpt-3-study-GUI
## to define the sound models and provide functions to play and save
## to be used for any stufy GUI that branch of it...

import pandas
import pickle
import subprocess, time
import OSC, time
import numpy
import platform

OS_INFO = platform.system()
if OS_INFO == "Windows":
	SCPATH = 


class SC:
    """SC is a class to start SuperCollider language as subprocess 
    and control it via a pipe. So far all output goes to the stdout
    (c) 2016 thermann@techfak.uni-bielefeld.de"""


    def __init__(self, sclangpath="/Applications/SuperCollider.app/Contents/Resources/sclang"):
        self.scp = subprocess.Popen([sclangpath], shell=False, stdin=subprocess.PIPE)        
    def cmd(self, cmdstr):
        self.scp.stdin.write(cmdstr.replace('\n','').replace('\t','') +'\n');    
    def boot(self):
        self.cmd("s.boot")
    def exit(self):
        self.scp.stdin.close()
    def __del__(self):
        print "delete SC instance"
        self.exit()

sc = SC()

sc.cmd(r"""
Server.default = s = Server.local;
/*{s.makeGui;}.defer;*/ 
s.boot.doWhenBooted({ Routine({
/* synth definitions *********************************/
"load synth definitions".postln;
SynthDef(\jj1, {|out=0, amp=0.6, pitch=50, chirp=0, dur=0.5, att=0.0, decslope=(-12),
	amint=0, amfreq=0, lfnfrq=0, lfnint=0, vowel=2, voweldiff=0, bright=1, pan=0 |

	var sig, sum, aenv, fenv, amsig, va, ve, vi, vo, vu, blend;

	amsig = SinOsc.kr(amfreq, mul: 0.5*amint, add: 0.5);
	aenv = Line.ar(0, decslope,dur, doneAction: 2).dbamp * EnvGen.kr(Env.new([0, 1, 1, 0], [att*dur, dur-(dur*att)-0.01, 0.01]));
	fenv = Line.kr(pitch, pitch+chirp, dur).midicps + LFNoise1.kr(lfnfrq, lfnint*pitch.midicps);
	vu = Vowel(\u, \tenor);
	vo = Vowel(\o, \tenor);
	va = Vowel(\a, \tenor);
    ve = Vowel(\e, \tenor);
	vi = Vowel(\i, \tenor);
	blend = Line.kr(vowel, vowel+voweldiff, dur);
	sig =  Formants.ar(fenv, vu
		.blend(vo, blend.linlin(0,1,0,1,\minmax))
		.blend(va, blend.linlin(1,2,0,1,\minmax))
		.blend(ve, blend.linlin(2,3,0,1,\minmax))
		.blend(vi, blend.linlin(3,4,0,1,\minmax))
		.brightenExp(bright.reciprocal, 1));
	sum = sig*amsig*aenv;
	Out.ar(0, Pan2.ar(sum, pan, amp));
}).add();

SynthDef(\reverb, {|outbus, mix=0.25, room=0.15, damp=0.5, amp=1.0|
	var sig;
	sig = In.ar(outbus, 2);
	ReplaceOut.ar(outbus,
		FreeVerb2.ar( sig[0], sig[1], mix, room, damp, amp));
}).add();
s.sync;
/* init code *******************************************/
"execute initialization code".postln;
s.sendMsg("/s_new", "reverb", 1001, 1, 0, "outbus", 0, "room", 0.7, "mix", 0.1, "damp", 0.9);
/* test signals ***************************************/
"create test signals".postln;
y = Synth.new(\default, [\freq, 800]); 0.15.wait; y.free;
}).play} , 1000);
""")

# maxprocess = subprocess.call(["/usr/bin/open", "-a", "AbstractModelV1.app"])


# clientSC  = OSC.OSCClient(); clientSC.connect(("127.0.0.1", 57110))
# def sc_msg(onset, msgAdr="/s_new", msgargs=["s1", 2000, 1, 0, "freq", 300, "amp", 0.5]):
#     global clientSC
#     bundle = OSC.OSCBundle()
#     msg = OSC.OSCMessage()
#     msg.setAddress(msgAdr)
#     msg.extend(msgargs)
#     bundle.append(msg)
#     bundle.setTimeTag(onset)
#     clientSC.send(bundle)

# clientMAX = OSC.OSCClient(); clientMAX.connect(("127.0.0.1", 9000)) 
# def max_msg(onset, msgAdr="/s_new", msgargs=["freq", 300, "amp", 0.5]):
#     global clientMAX
#     bundle = OSC.OSCBundle()
#     msg = OSC.OSCMessage()
#     msg.setAddress(msgAdr)
#     msg.extend(msgargs)
#     bundle.append(msg)
#     bundle.setTimeTag(onset)
#     clientMAX.send(bundle)

# # TH: for vocal synth
# parspec_vocal = numpy.array([ # name, min, max, scaling (lin/exp), default
# #("evrate", 0.2, 4, "exp", 0.5, "Hz"),
# #("irregularity", 0, 1, "lin", 0, "%"),
# ("dur", 0.005, 1.5, "exp", 0.4, "secs"), 
# ("att", 0.001, 0.5, "exp", 0.001, "secs"),
# ("decslope", -50, 10, "lin", -12, "dB/rm time"),
# ("amint",  0, 1, "lin", 0, "intensity"),
# ("amfreq", 1, 50, "exp", 1, "Hz"),
# ("pitch", 20, 85, "lin", 50, "midinote"),
# ("chirp", -36, 36, "lin", 0, "semitones/dur"),
# ("lfnfrq", 5, 50, "exp", 5, "Hz"),
# ("lfnint", 0, 0.5, "lin", 0, "rel. pitch"),
# ("vowel", 0, 4, "lin", 2.5, "uoaei"),
# ("voweldiff", -2.5, 2.5, "lin", 0, "delta"),
# ("bright", 0.2, 1, "lin", 0.5, "arb.u.")], dtype=[
#       ('name', 'S20'), ('min', '>f4'), ('max', '>f4'), ('scaling', 'S10'), ('default', '>f4'), ('unit', 'S20')])

# # JJ: New parspec
# parspec_abstract = numpy.array([ # name, min, max, scaling (lin/exp), default
# #("evrate", 0.2, 4, "exp", 0.5, "Hz"),
# #("irregularity", 0, 1, "lin", 0, "%"),
# ("dur", 0., 1., "lin", 0.5, "secs"),
# ("att", 0., 1., "lin", 0.3, "%"),
# ("desvol", 0., 1., "lin", 0.5, "dB/dur"),
# ("pitch", 0, 1., "lin", 0.5, "Hz"),
# ("chirp", 0., 1., "lin", 0.5, "semitones/dur"),
# ("lfndepth", 0., 1., "lin", 0., "rate"),
# ("lfnfreq", 0, 1., "lin", 0., "Hz"),
# ("amdepth", 0., 1., "lin", 0., "rate"),
# ("amfreq", 0., 1., "lin", 0., "Hz"),
# ("richness", 0., 1., "lin", 0.5, "%"),
# ("lpfreq", 0., 1., "lin", 0.5, "Hz")  # I wonder if this is important.       
#     ], dtype=[
#       ('name', 'S20'), ('min', '>f4'), ('max', '>f4'), ('scaling', 'S10'), ('default', '>f4'), ('unit', 'S20')])

# parspecs = { "abstract" : parspec_abstract, "vocal" : parspec_vocal} 


# def parmap(par=("pitch", 20, 85, "lin", 50, "midinote"), val=0.5):
#     mi, ma = par[1], par[2]
#     if(par[3]=="lin"): return mi+(ma-mi)*val
#     if(par[3]=="exp"): return mi*numpy.exp(numpy.log(ma/mi)*val)

# def parunmap(par=("pitch", 20, 85, "lin", 50, "midinote"), val=40):
#     mi, ma = par[1], par[2]
#     if(par[3]=="lin"): return (val-mi)/(ma-mi)
#     if(par[3]=="exp"): return numpy.log(val/mi)/numpy.log(ma/mi)
    
# def parvecmap(parspec, vec):
#     return numpy.array([parmap(parspec[k], v) for k,v in enumerate(vec)])

# def parvecunmap(parspec, vec):
#     return numpy.array([parunmap(parspec[k], v) for k,v in enumerate(vec)])    

# # test code:
# # print parvecunmap(parspec_vocal, parspec['default']) # get default parameters

# def playevent(soundmodel, v):
#     # v is unmapped vector, i.e. vector elements in [0,1]
#     ps = parspecs[soundmodel];
#     vec = parvecmap(ps, v);
#     if(soundmodel=='vocal'):
#         sc_msg(0, "/s_new", ["jj1", 1002+numpy.random.randint(900), 1,1] + 
#            [x for pair in zip(ps['name'].tolist(), vec) for x in pair] );
#     if(soundmodel=='abstract'):
#         max_msg(0, "/s_new" , [x for pair in zip(ps['name'].tolist(), vec) for x in pair] )
        
# # playevent('vocal', v)

