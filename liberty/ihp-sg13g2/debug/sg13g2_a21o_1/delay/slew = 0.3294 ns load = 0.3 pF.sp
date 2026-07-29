.title comb_delay
.include /home/marcus/.ciel/ciel/ihp-sg13g2/versions/ee974c3adc69d0f36adbf20577079f0df419d702/ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice
.include /home/marcus/.ciel/ciel/ihp-sg13g2/versions/ee974c3adc69d0f36adbf20577079f0df419d702/ihp-sg13g2/libs.tech/ngspice/models/sg13g2_moslv_mod.lib
.lib /home/marcus/.ciel/ciel/ihp-sg13g2/versions/ee974c3adc69d0f36adbf20577079f0df419d702/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
VDD VDD 0 1.2V
VSS VSS 0 0.0V
VNW VNW 0 1.2V
VPW VPW 0 0.0V
CX vX 0 0.3pF
VB1 vB1 0 PWL(0s 1.2V 9.882000000000002e-10s 1.2V 1.5372e-09s 0.0V)
Xdut vX VDD VSS vB1 VDD VSS sg13g2_a21o_1
.options TEMP = 25C
.options TNOM = 25C
.options autostop
.options trtol = 1
.meas TRAN cell_fall__b1_to_x trig v(vB1) val=0.6 fall=1 targ v(vX) val=0.6 fall=1
.meas TRAN fall_transition__b1_to_x trig v(vX) val=0.96 fall=1 targ v(vX) val=0.24 fall=1
.tran 0.041175ns 329.40000000000003ns 0s
.end