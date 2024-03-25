This is an olympiad geometry theorem prover.

It works by proving as many statements as it can from the currently known statements. There a number of statement kinds:
- Directed angle equalities modulo pi/180 degrees
- Directed angle equalities modulo 2pi/360 degrees
- Lenght ratio equalities
- collinearity, either with or without a specified order of points on the line.\
    A line can also be specified to be a radical axis (which is a generalisation of perpendicular bisector)
- concyclicity, either with or without a specified order of points on the circle\
    A circle can also have a specified midpoint.\
    One can also specify that a circle need not have a midpoint - this is usuall called a circline.
- Triangle similarities.

Each proposition can also be negated. We make the implicit assumption that any two different point are distinct. Each kind of proposition comes with it's own list of theorems that are tried for each known such proposition. Here is the list:

- Directed angle equalities modulo pi/180 degrees
    - AB || BC => A,B,C collinear
    - cyclic angles imply cyclic quadrilateral
    - double the equation so it is modulo 2pi
    - adding/subtracting any two equalities to get a new equality. This step is by far the most inefficient one, and it is the main reason for the slow speed of the program. It is not a fundamental problem, but a problem with the implmentation that I've chosen.

- Directed angle equalities modulo 2pi/360 degrees
    - AB || BC (mod 2pi) => A,B,C collinear in that order
    - the same equality holds modulo pi
    - if all coefficients are even, halve the equality to get a result modulo pi
    - adding/subtracting any two equalities to get a new equality

- There is some more complicated angle hunting for angles either mod pi or 2pi,
    which gives more readable proofs of combining angle equalities.

- Lenght ratio equalities
    - |AO|=|BO| =>
        - A,B on a circle with centre O
        - OAB is an isoceles triangle, so the base angles are equal modulo 2pi
        - O is on the perpendicular bisector of A,B
    - multiplying/dividing any two equalities to get a new equality
    - angle bisector theorem: if some ratio holds, and some points are collinear then we get an angle bisector modulo pi

- Collinearity
    - every two segments on the same line are collinear, modulo pi or 2pi depending on whether the points on the line are in order
    - for any two lines, if they share at least 2 points, then the union of the points of both lines is collinear
    - some more theorems about radical axis/perpendicular bisector

- Concyclicity
    - when two circles share their midpoint and a point on the circle, their union is a circle
    - for 4 points on a circle, we get cyclic angles, modulo pi or 2pi depending on whether the points were in order on the circle
    - for 3 points on a circle, and a centre, then central angle theorem gives some angles modulo 180
    - for 3 points on a proper circle, they are not collinear

- Triangle similarities.
    - triangle similarity gives the obvious angle and length ratio equalities


These theorems are always tried whenever a proposition of the associated kind is found. There are a few more theorems that are not related to a kind of proposition in this way, but instead are tried in a stand alone way:

- Finding similar triangles. We loop through all pairs of triplets of points, and try each of the similarity cases. Many cases split into a case for equally oriented triangles, and oppositely oriented triangles.
    - aa: when two angles are equal modulo pi, and one of the triangles is proper (i.e. the 3 points aren't collinear)
    - sas: when an angle is equal modulo 2pi and a corresponding ratio holds
    - sps: when an angle is equal, and is pi/2 modulo pi, and a corresponding ratio holds.
    - ssp: when an angle is equal, and is pi/2 modulo pi, and a corresponding ratio holds.
    - sss: when the side length ratios are the same
    - ssa: this isn't actually a triangle similarity but this case allows one to conclude one angle equality using the sine rule.
        This subsumes one direction of the angular bisector theorem.
    
- Thales's theorem: when O is the midpoint of AB and AC is perpendicular to BC, then ABC is a circle with midpoint O.

- inscribed circle: if A,B,C are not collinear, if AI and BI are perpendicular bisectors, then CI is a perpendicular bisector,
    and angle equality <AB + <CI = <AI + <BI + pi/2 holds.

.
-

Here are some examples of what an inputted problem looks like:

A B C E F M O Q\
Verhouding E,Q*=F,Q*\
Lijn B,M,C\
Lijn Q,E,F\
Lijn A,B,E\
Lijn A,C,F\
Lijn O,M,A\
Lijn Q,B,C\
HoekMod180 E,F+=Q,O+ 90\
HoekMod180 A,B+=B,O+ 90\
Verhouding M,B+=M,C+\
Verhouding A,B+=A,C+

EGMO 4 2021:\
A B C I D E F A'\
Lijn B,C,A'\
Lijn A,B,C None False False\
HoekMod360 A,I+A,I=A,B+A,C\
HoekMod360 B,I+B,I=B,A+B,C\
Lijn B,C,D\
Lijn B,I,F\
Lijn C,I,E\
HoekMod180 D,F+=C,I+ 90\
HoekMod180 D,E+=B,I+ 90\
Verhouding A,E*=A',E*\
Verhouding A,F*=A',F*


A B C D E F H X Y\
Cirkel E,F,D,H\
Lijn A,B,C None False False\
Lijn B,E,Y,H\
Lijn C,F,X,H\
Lijn A,B,X\
Lijn A,C,Y\
HoekMod180 A,B+=C,F+ 90\
HoekMod180 A,C+=B,E+ 90\
Lijn A,E,F\
HoekMod360 A,E+A,E=A,B+A,C 180\
HoekMod180 A,C+C,D=A,D+B,C\
HoekMod180 A,B+B,D=A,D+B,C


EGMO 1 2022:\
A B C P Q T H S\
Lijn T,H,S\
Lijn A,B,C None False False\
Lijn A,P,B\
Lijn A,Q,C\
Verhouding B,C*=B,Q*\
Verhouding B,C*=P,C*\
Verhouding T,A*=T,P*\
Verhouding T,A*=T,Q*\
HoekMod180 A,B+=C,H+ 90\
HoekMod180 A,C+=B,H+ 90\
Lijn B,S,Q\
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



