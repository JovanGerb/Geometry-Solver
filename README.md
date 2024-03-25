Here are some examples of what an inputted problem looks like:
A B C E F M O Q
Verhouding E,Q*=F,Q*
Lijn B,M,C
Lijn Q,E,F
Lijn A,B,E
Lijn A,C,F
Lijn O,M,A
Lijn Q,B,C
HoekMod180 E,F+=Q,O+ 90
HoekMod180 A,B+=B,O+ 90
Verhouding M,B+=M,C+
Verhouding A,B+=A,C+

EGMO 4 2021:
A B C I D E F A'
Lijn B,C,A'
Lijn A,B,C None False False
HoekMod360 A,I+A,I=A,B+A,C
HoekMod360 B,I+B,I=B,A+B,C
Lijn B,C,D
Lijn B,I,F
Lijn C,I,E
HoekMod180 D,F+=C,I+ 90
HoekMod180 D,E+=B,I+ 90
Verhouding A,E*=A',E*
Verhouding A,F*=A',F*


A B C D E F H X Y
Cirkel E,F,D,H
Lijn A,B,C None False False
Lijn B,E,Y,H
Lijn C,F,X,H
Lijn A,B,X
Lijn A,C,Y
HoekMod180 A,B+=C,F+ 90
HoekMod180 A,C+=B,E+ 90
Lijn A,E,F
HoekMod360 A,E+A,E=A,B+A,C 180
HoekMod180 A,C+C,D=A,D+B,C
HoekMod180 A,B+B,D=A,D+B,C


EGMO 1 2022:
A B C P Q T H S
Lijn T,H,S
Lijn A,B,C None False False
Lijn A,P,B
Lijn A,Q,C
Verhouding B,C*=B,Q*
Verhouding B,C*=P,C*
Verhouding T,A*=T,P*
Verhouding T,A*=T,Q*
HoekMod180 A,B+=C,H+ 90
HoekMod180 A,C+=B,H+ 90
Lijn B,S,Q
Lijn C,S,P

These are all problems that the program can solve. Some take only 20 seconds (the last one for example), while others take something like 10 minutes.
The first input line says what all the points in the picture are. The second input line is the goal that has to be proven. The remaining lines are things given in the question. Here is what a couple of the statements mean:
-	Lijn T,H,S: these points are collinear
-	Lijn A,B,C None False False: these three points are not collinear
-	Verhouding B,C*=B,Q*: length BC equals length BQ
-	HoekMod180 A,B+=C,H+ 90: AB and CH are perpendicular
-	HoekMod180 A,B+=C,D+: AB and CD are parallel
-	Cirkel E,F,D,H: these points are concyclic
-	HoekMod180 G,D+F,C=D,F+D,C: angle GDF equals angle DCF with directed angles modulo 180
Notice that the input is space (and case) sensitive: adding or removing a space somewhere will mess it up.
The output consists of some things that it finds and thinks might be interesting, and when it finds a proof, it will print it. Often it will then find a slightly shorter proof, and then print the new proof, so if there are multiple proofs, just look at the last one.
In the second to last problem, I added the points X and Y to the input, even though they are not needed to define the problem. I did this because these points help the program to find the solution. So the program can only solve this problem if I tell it to consider these points. The program unfortunately slows down a lot when there are more points, so this question almost takes half an hour.
