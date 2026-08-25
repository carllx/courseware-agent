# Nielsen_1994_Enhancing_Usability_Heuristics

!!!5?
HumaFnactormsCompuhSngystems CHI’94* “CekbIa/mhgkdepewie)fce”
Enhancing the Explanatory Power of Usability Heuristics
Jakob Nielsen
Bellcore
445 South Street
Morristown, NJ 07960
Email: nielsen@bellcore. com (primary) or nielsen.chi@xerox.com (backup)
Electronic business card: nielsen-info@bellcore. com
ABSTRACT would be insufficient to hand different groups of usability spe-
Several published sets of usability heuristics were compared cialists different lists of heuristics and let them have a go at a
with a database of existing usability problems drawn from a sample interface: it would be impossible for the evaluators to
variety of projects in order to determine what heuristics best wipe their minds of the additional usability knowledge they
explain actual usability problems. Based on a factor analysis hopefully had, so each evaluator would in reality apply certain
of the explanations as well as an analysis of the heuristics heuristics from the sets he or she was supposed not to use.
providing the broadest explanatory coverage of the problems,
Instead of finding the “winner” among the existing sets of
a new set of nine heuristics were derived: visibility of system
heuristics, the present study aims at synthesizing a new set of
status, match between system and the real world, user control
usability heuristics that is as good as possible at explaining
and freedom, consistency and standards, error prevention,
the usability problems that occur in real systems. As a seed
recognition rather than recall, flexibility and efficiency of
for this effort, I collected the seven sets of usability heuristics
use, aesthetic and minimalist design, and helping users rec-
listed in the appendix. As can be seen from the appendix,
ognize, diagnose, and recover from errors.
these sets are very different in scope and nature, and they
Keywords: Heuristic evaluation, Usability problems. were indeed selected from the many available lists with the
goal of including a wide variety of perspectives on usability.
INTRODUCTION
RATING THE USABILITY EXPLANATIONS
Heuristic evaluation [11] [13] is a “discount usability engi-
neering” method for evaluating user interfaces to find their The usability heuristics were used to explain a database of
usability problems. Basically, a set of evaluators inspects the 249 usability problems collected by the author from 11 ear-
interface with respect to a small set of fairly broad usability lier projects. Of these 11projects, 7 were evaluated with heu-
principles, which are referred to asthe “heuristics.” The orig- ristic evaluation and 4 with user testing; 4 were evaluated at
inal set of usability heuristics used for several early studies an early stage of their development lifecycle and 7 were eval-
was developed with the main goal of making the method uated at a late stage; and 2 had character-based interfaces, 6
easy to teach [12], since it is an important aspect of discount had graphical user interfaces, and 3 had telephone-operated
usability engineering that the methods can be widely used interfaces. Each of the 101 usability heuristics was rated for
and are easy to transfer to new organizations. how well it explained each of the 249 usability problems,
using the following rating scale:
In recent years, heuristic evaluation has seen steadily more
widespread use, and many users of the method have devel- O= does not explain the problem at all
oped their own sets of heuristics. Also, the user interface liter- 1 = may superficially address some aspect of the problem
ature abounds with lists of general usability principles, even 2 = explains a small part of the problem, but there are major
though they are not always explicitly intended for use in heu- aspects of the problem that are not explained
ristic evaluation. Given the many available lists of usability 3 = explains a major part of the problem, but there are some
heuristics, it is an open question to what extent one list is bet- aspects of the problem that are not explained
ter than another and how one could construct an optimal list of
4 = fairly complete explanation of why this is a usability
usability heuristics. The relative merits of the various lists can
problem, but there is still more to the problem than is
only be determined by a shoot-out type comparative test,
explained by the heuristic
which is beyond the scope of the present study. Note that it
5 = complete explanation of why this is a problem
Permission to copy without fee all or part of this material ia There is some degree of subjectivity in this kind of rating, so
granted provided that the copies are not made or distributed for
one should not rely on fine distinctions or details in the
direct commercial advantage, the ACM copyright notice and the
resulting data. Jeffries [6] found that three usability special-
title of the publication and its date appear, and notice is given
ists only had full agreement on about two-thirds of the items
that copying is by permission of the Association for Computing
Machinery. To copy otherwise, or to republish, requires a fee in a simple classification of usability problems, and the
and/or specific permission. present rating scale surely also has less than perfect reliabil-
CH194-4/94 Boston, Massachusetts USA
91994 ACM 0-89791-650-6/94/01 52... $3.50

BostonM,assachusUeSttsAoApril24-28,1994 HumaFnactorinsComputinSgystems
Q ,,
ity. Unfortunately, additional raters were not available as it G2 Speak the user’s language .67
F1 Metaphors from the real world .63
was necessary to have participated in the original projects in
B1 Familiar user’s conceptual model .62
order to assess the degree to which the heuristics explained
E7 Use of user’s background knowledge .51
the usability problems. Thus, it is important not to rely on C6 Learnable through natural, conceptual model .47
detailed ratings of individual usability problems. GI 8 Follow real-world conventions .45
B3 Screen representation matches non-computer .37
The appendix gives the mean rating for each usability hettris- E2 Encourage users to import pre-existing tasks .35
D2 Identity cues between actions and user’s goals .31
tic, showing how well it was judged to explain the usability
G3 Understand the user’s language .27
problems. It is not reasonable to view this as a kind of com-
petition between the sets of heuristics for severid reasons: Factor 3: User control and freedom 4.6%
First, three of the sets were not originally intended for heuris- G23 Undo and redo should be supported .89
D4 Obvious way to undo actions .86
tic evaluation (the Star set was intended for interface design,
F8 Forgiveness: make actions reversible .75
Poison and Lewis’ set was limited to improving “guessabil- Cl 8 Ability to undo prior commands .64
ity, ” and Carroll and Rosson’s set was intended for claims A6 Clearly marked exits .52
analysis) and these three sets do indeed achieve lower scores Cl 9 Ability to re-order or cancel tasks .45
B7 Modeless interaction .31
than the others. Second, the database of usability problems
F6 User control: allow user to initiate/control actions .30
includes many problems from character-based interfaces and F11 Modelessness: allow users to do what they want .27
telephone-operated interfaces, which may not be a strength
of the Macintosh and SunSoft heuristics since they were Factor 4: Consistency and standards 4.2yo
A4 Consistency: express same thing same way .87
probably optimized for graphical user interfaces. Finally, the B5 Consistency .87
original set of heuristics no doubt has an advantage since a F4 Consistency: same things look the same .86
large part of the database comes from interfaces that were C3 Uniform command syntax .57
studied aspart of the original heuristic evaluation project. GI 9 Conform to platform interface conventions .46
C4 Consistent key definitions throughout .34
B4 Universal commands: a few, generic commands .33
FACTOR ANALYSIS C5 Show similar info at same place on each screen .31
A principal components analysis of the data shows that it is Factor 5: Error prevention 3.770
not the case that a few factors account for most of the vari- A9 Prevent errors from occurring in the first place .83
G22 System designed to prevent errors .73
ability in the usability problems. The two most important fac-
G3 Understand the user’s language .54
tors account for about 670 of the variance each. The seven E6 What planning mistakes are most likely? .37
factors that account for more than 3% of the variance each E9 What slips are most likely? .35
only add up to 30% of the variance. Indeed, there is a gradual D2 Identity cues between actions and user’s goals .30
decline in the significance of the factors, with no particular Factor 6: Recognition rather than recall 3.1%
sharp drop-off point that might indicate that a core factor set F3 See-and-point instead of remember-and-type .72
had been found. There are 25 factors that account for 1% or D1 Make the repertoire of available actions salient .68
more of the variance each, and these 25 factors together B2 Seeing and pointing: objects and actions visible .57
G16 All user needs accessible through the GUI .53
account for 62% of the variance.
El 2 What features often missed and at what cost? .52
Cl OProvide lists of choices and picking from lists .42
The following is a list of the seven most important factors A3 Minimize the users’ memory load .37
from the factor analysis. Each factor was given a descriptive F2 Direct manipulation: visible objects, visible results .33
name in order to summarize the underlying usability phe- E8 Easy or difficult to perform (execute) task? .32
nomenon that seems to be covered by most of the heuristics El Evoke goals in the user .31
C20 Allow access to operations from other apps. .30
that are highly loaded for that factor. For each factor, the list
A6 Clearly marked exits .29
states the proportion of the total variance in the usability Cl 3 Show icons and other visual indicators .29
problem ratings accounted for by that factor. Finally, the heu- G20 Integrated with the rest of the desktop .27
ristics with loadings of .25 or more are listed for each factor
Factor 7: Flexibility and efficiency of use 2.8%
(the codes in front of the heuristics refer to the appendix GI 4 Accelerators should be provided .80
where many of them are explained in more detail). A7 Shortcuts: Accelerators to speed up dialogue .80
B8 User tailorability to speed up frequent actions .62
Factor 1: Visibility of system status 6.l% F6 User control: allow user to initiate/control actions .43
A5 Feedback: keep user informed about what goes on .81 G12 System should be efficient to use .42
C8 Provide status information .70 G17 User interface should be customizable .42
F7 Feedback: show that input has been received .70 Cl 9 Ability to re-order or cancel tasks .28
El 3 Features change as user carries out task .69 G21 Keyboard core functions should be supported .26
G4 Feedback provided for all actions .56 GI 1 Physical interaction with system feels natural .26
G5 Feedback timely and accurate .48
El OIndicate progress in task performance .46 The last three factors in the top ten, each accounting for
F2 Direct manipulation: visible objects, visible results .39
about 25Z0of the variance, can be described as aesthetic and
D3 Identity cues system response vs. user’s goals .34
Cl 3 Show icons and other visual indicators .32 minimalist design, well-structured features that are easy to
F5 WYSIWYG: do not hide features .32 discriminate, and use of default values so that the user does
El 5 What incorrect inferences are most likely .27 not have to re-enter information. Note, by the way, that the
Factor 2: Match between system and real world 5.9% labels used to describe the factors are the author’s subjective
A2 Speak the user’s language .78
C7 Contains familiar terms and natural language .71
153

%?!
HumaFnactorinsComputiiSgystems
-.1
attempt to abstract the main usability thrust of each facton It Top Heuristics to Explain All the Usability Problems
would have been possible to use other names instead. A4 Consistency: same thing, same way 23~o 237.
A2 Speak the user’s language 1670 390/.
The difference between factors 1 and 6 seems to be that “vis-
ibility of system status” deals mostly with revealing what is F7 Feedback: show receipt of user’s input 1370 527.
happening in the system, whereas “recognition rather than B2 Seeing/pointing vs. rememberinghyping 7~o 590/0
recall” deals mostly with making the user’s future options F1OAesthetic integrity, keep design simple 70/0 6570
salient. The difference between factors 3 and 7 seems to be A7 Shortcuts and accelerators 6Y. 71 0/0
that “user control and freedom” is focused on minimizing the GI 8 Real-world conventions 4% 7670
extent to which the system traps the user in a specific state El 8 Help error recognition/recovery 470 80%
from which there is no escape, whereas “flexibility and effi- F8 Forgiveness: reversible computer actions 370 830/0
ciency of use” is focused on allowing the user additional
DI Salient repertoire of available actions 2% 85%
options to sidestep the regular interaction techniques.
The factors revealed by the factor analysis do seem to cover ToDHeuristics to Exdain the Serious Usabilitv. Problems
fundamental usability principles, but unfortunately it was not B2 Seeing/pointing vs. remembering/typi ing 22% 22?10
possible to account for a reasonably large part of the variabil- F4 Consistency: same thing looks the sa
ity in the usability problems with a small, manageable set of G5 Feedback timelv and accurate 117°/o[5 W
usability factors. In other words, usability problems are due I D1 Salient re~ertoire of available actions I 12%1 7
to a broad variety of underlying phenomena.
F8 Forgiveness: reversible computer actions 770 770/0
B1 Familiar user’s conceptual model 5V0 82%
EXPLANATORY COVERAGE
F7 Feedback: show receipt of user’s input 570 877.
53 factors are needed to account for 90% of the variance in A9 Prevent errors from occurring 40/0 900/.
the usability problems. This is too much for practical heuri- D5 Easy to discriminate action alternatives 2°h 9370
stic evaluations where evaluators are asked to compare each B7 Modeless interaction 2?/0 9570
interface element against the list of heuristics. Thus, instead
of finding a set of usability factors that account for all usabil- Table 1 The ten heuristics that achieve the widest cover-
age with respect to explaining usability problems. The top
ity phenomena, we will have to reduce our ambitions to find-
list are heuristics to explain the complete database of 249
ing a set of usability heuristics that account reasonably well
usability problems and the bottom list are heuristics to
for the majority of the usability problems. It is likely that the
explain the 82 serious usability problems. For each heuris-
seven (or ten) factors listed in the previous section could be tic, thejirst percentage indicates the proportion of problems
used as such a set, but we do not currently have empirical it explains (that have not already been explained by a
evidence to confirm the value of this new set of heuristics. higher-ranked heuristic), and the second percentage indi-
cates the cumulative proportion of usability problems
Instead, we will look at the explanatory coverage that is pos- explained by at least-on~ element of the list of heuristics.
sible by various combinations of the existing heuristics for
which we do have data. Since we have seen that perfection is
impossible with a reasonably small set of heuristics, we will Concentrating on Major Usability Problems
consider a usability problem to be “explained” by a set of It is often noted that a very large proportion of the usability
heuristics if it has achieved an explanation score of at least 3 problems found by heuristic evaluation tends to be minor
(“explains a major part of the problem, but there are some problems [7]. This preponderance of minor problems is seen
aspects of the problem that are not explained”) from at least as a drawback by many [2], even though it is still possible to
one of the heuristics in the set. Whh this scoring method, a focus on the serious problems by using a severity rating
set of heuristics did not get additional credit for having multi- method [8] [11 ] to prioritize the list of usability problems
ple heuristics that explained a problem. This was done found by a heuristic evaluation of a given interface. In any
because it is currently an open issue to what extent it is better case, it is probably desirable to increase the proportion of
to have a good match between a usability problem and a sin-
serious usability problems found by heuristic evaluation.
gle heuristic (meaning that the evaluator has it pegged) or to
have a match between the problem and several heuristics Of the 249 usability problems in the database used for the
(meaning that more aspects of the problem are known). The present analysis, 82 can be classified as serious usability
appendix lists the proportion of usability problems problems in that they have high potential for causing major
“explained” by each heuristic as well as the proportion of delays or preventing the users from completing their task
problems explained by each set of heuristics. [11]. The bottom part of Table 1 lists those heuristics that
give maximum explanation coverage for this set of serious
The widest explanatory coverage will be realized by first usability problems. It can be seen from the table that the
choosing the heuristic that explains the most usability prob- major usability problems are somewhat more concentrated
lems, then adding the heuristic that explains the most of the around a few heuristics than is the group of usability prob-
remaining problems (i.e., those that have not already been lems as a whole: the four heuristics with the widest explana-
explained), and so on. The top part of Table 1 lists the ten tory coverage explain 70% of the major problems but only
heuristics that taken together explain the most usability prob- 65% of the full set of problems (which is dominated by the
lems as assessed by this approach. 167 minor problems).
154

BostonM,assachusUeSttsA* April24-28,1994 HumaFnactorinsComputin$g’s(ems
!%?
It can be seen from Table 1 that there is not much difference malist design, and helping users recognize, diagnose, and
between the heuristics that explain the full database and recover from errors. These heuristics seem to be excellent for
those that explain the major problems. Most principles occur explaining previously found usability problems. It remains to
in both lists, either as exact duplicates or in slightly altern- be seen to what extent they are also good for finding new
ative wordings. The main difference seems to be that the list problems, which of course is the main goal of heuristic eval-
of heuristics covering the serious problems gives more uation.
weight to usability principles associated with making things
visible and salient in the interface (to the extent that there are Acknowledgments
two feedback rules on the list—the reason this can happen is The author would like to thank Alan McFarland and nine CHZ’94
that these rules were described differently in the source docu- referees for comments on earlier versions of this manuscript,
ments, meaning that there is some degree of non-overlap in
the problems they explain). References
1. Apple Computer. Macintosh Human Interface Guidelines.
Comparing the heuristics explaining the major problems with
Addison-Wesley, Reading, MA, 1992.
those explaining the minor problems (not listed for reasons
2. Brooks, P.Adding value to usability testing. In Nielsen, J.,
of space), shows that the heuristics in the top-10 for the
and Mack, R. L. (Eds.), Usability Inspection Methods,
major problems that are not in the top-10 for the minor prob-
John Wiley & Sons, New York, NY, 1994, 253–270.
lems are D1 (make the repertoire of available actions salient),
3. Carroll, J. M., and Rosson, M. B. Getting around the task-
B 1 (familiar user’s conceptual model), A9 (prevent errors),
artifact cycle: How to make claims and design by scenario.
D5 (easy to discriminate available action alternatives), and ACM Trans. Znfor. Systems 10,2 (April 1992), 181–212.
B7 (modeless interaction). Thus, closer attention to these 4. Holcomb, R., and Tharp, A. L. An amalgamated model of
heuristics may help increasing the proportion of serious software usability. In Knafl, G. (Ed.), Proceedings of the
usability problems found by heuristic evaluation. 13th IEEE COMPSAC International Conference, IEEE
Computer Society, Washington, D. C., 1989.
Among the five heuristics with the widest explanatory cover-
5. Holcomb, R., and Tharp, A. L. What users say about soft-
age of minor usability problems, three do not occur on the
ware usability. International Journal of Human–Computer
top- 10 list for major problems: A2 (speak the user’s lan-
Interaction 3, 1 (1991), 49–78.
guage), F1 O (aesthetic integrity), and A7 (shortcuts and
6. Jeffries, R. Usability problem reports: Helping evaluators
accelerators). One might argue that these heuristics should be
communicate effectively with developers. In Nielsen, J.,
disregarded in the future since they tend to find minor prob- and Mack, R. L. (Eds.), Usability Inspection Methods,
lems. Even so, F1Oand A7 should be kept since aesthetic John Wiley & Sons, New York, NY, 1994, 271–292.
integrity is important for subjective satisfaction anti sales and 7. Jeffries, R. J., Miller, J. R., Wharton, C., and Uyeda, K. M.
shortcuts and accelerators are relevant for expert user perfor- User interface evaluation in the real world: A comparison
mance. These qualities are important for overall usability of four techniques. Proc. ACM CHI’91 Conf. (New
even though any individual usability problem in these cate- Orleans, LA, 28 April 28–3 May), 119–124.
gories will not cause the system to be unusable which is why 8. Karat, C. A comparison of user interface evaluation meth-
they tend not to be classified as major. ods. In Nielsen, J., and Mack, R. L. (Eds.), Usability
Inspection Methods, John Wiley & Sons, New York, NY,
CONCLUSIONS 1994, 203–232.
9. Molich, R., and Nielsen, J. Improving a human-computer
Almost all of the seven usability factors found above are rep-
dialogue. Communications of the ACM 33, 3 (March
resented in the lists of top-10 heuristics in Table 1. The
1990), 338–348.
exceptions are that factor 5 (error prevention) is not repre- 10. Nielsen, J. Usability Engineering. Academic Press,
sented in the set of heuristics to explain the full database and Boston, MA, 1993.
factor 7 (flexibility and efficiency of use) is not represented 11. Nielsen, J. Heuristic evaluation. In Nielsen, J., and Mack,
in the set of heuristics to explain the major usability prob- R. L. (Eds.), Usabili~ Inspection Methods, John Wiley &
lems. Given the above comments that efficiency issues are Sons, New York, NY, 1994, 25–64.
important even though they were often not classified as 12. Nielsen, J., and Molich, R. Teaching user interface design
major problems, it would seem that Table 1 indicates the based on usability engineering. ACM SIGCHI Bulletin 21,
potential for the seven usability factors to form the backbone 1 (July 1989), 45-48.
of an improved set of heuristics. Two important heuristics 13. Nielsen, J., and Molich, R. Heuristic evaluation of user
from Table 1 are left out from the usability factors: F1O (aes- interfaces. Proc. ACM CHI’90 Conf. (Seattle, WA, 1–5
thetic integrity) and El 8 (help users to recognize, diagnose, .4pril 1990), 249–256.
and recover from errors). Error handling and aesthetic integ- 14. Poison, P. G., and Lewis, C. H. Theory-based design for
rity should probably be added as the eight and ninth heuri- easily learned interfaces. Human–Computer Interaction 5,
sticsto the set of factors. 2&3 (1990), 191–220.
15. Rohn, J. A. Usability Engineering: Improving Customer
The analysis in this paper has thus resulted in a candidate set Satisfaction While Lowering Development Costs. Bro-
of nine heuristics: visibility of system status, match between chure, SunSoft, Inc., Mountain View, CA, 1993.
system and the real world, user control and freedom, consis- 16. Smith, D. C., Irby, C., Kimball, R., Verplank, B., and
tency and standards, error prevention, recognition rather than Harslem, E. Designing the Star user interface. BYTE 7, 4
recall, flexibility and efficiency of use, aesthetic and mini- (April 1982), 242-282.
155

APPENDIX: LIST OF SEVEN SETS OF HEURISTICS FROM THE USER INTERFACE LITERATURE
In most cases, the sets of heuristics suggested by other authors have been rewritten for the sake of brevity and to achieve a con-
sistent format. The exact wording of these heuristics as printed here is therefore the responsibility of the present author and does
not necessarily correspond to the way the original authors would have edited their principles.
For each heuristic, the table lists its mean explanatory score across the 249 usability problems in the sample. The explanatory
power of each heuristic was scored on a O–5 scale for each usability problem, with O indicating that the heuristic did not explain
the problem at all and 5 indicating that the heuristic provided a complete explanation of why the user interface issue in question
constituted a usability problem. The table also lists the proportion of the usability problems that were explained at a level of 3 or
more, with a score of 3 indicating that the heuristic explained a major part of the problem while leaving some aspects of the
problem unexplained.
For each full set of heuristics (indicated by boldfaced type), the table lists the mean across usability problems of the best expla-
nation provided by any heuristic in the group as well as the proportion of problems for which the set had at least one heuristic
explai~ing the pro-blern at a level of at le;st 3.
F
m
%
3~s
Code Usability Heuristic S.=(D
SQDI
Q=.>
o
3
The ten usability heuristics explained in detail in [1O].This is a slightly modified version
A 3.72 82%
of the original heuristics used by Molich and Nielsen [9][13]
Simple and natural dialogue: Dialogues should not contain information which is irrelevant or rarely
Al needed. Every extra unit of information in a dialogue competes with the relevant units of information .78 10%
and diminishes their relative visibility. All information should appear in a natural and logical order.
Speak the user’s language: The dialogue should be expressed clearly in words, phrases and concepts
142 1.04 20%
familiar to the user, rather than in system-oriented terms.
Minimize the users’ memory load: The user should not have to remember information from one part of
A3 the dialogue to another. Instructions for use of the system should be visible or easily retrievable when- .53 10970
ever appropriate.
Consistency: Users should not have to wonder whether different words, situations, or actions mean the
A4 1.14 23%
same thing.
Feedback: The system should always keep users informed about what is going on, through appropriate
A5 .70 12%
feedback within reasonable time.
Clearly marked exits: Users often choose system functions by mistake and will need a clearly marked
A6 .28 6%
“emergency exit” to leave the unwanted state without having to go through an extended dialogue.
Shortcuts: Accelerators—unseen by the novice user—may often speed up the interaction for the expert
A7 .41 8%
user such that the system can cater to both inexperienced and experienced users.
Good error messages: They should be expressed in plain language (no codes), precisely indicate the 4
A8 .51 1070
D. roblem. and constructively suw. .zest a solution.
Prevent errors: Even better than good error messages is a careful design that prevents a problem from
A9 .64 11%
occurring in the first place.
EHelp and documentation: Even though it is better if the system can be used without documentation, it
Al O may be necessary to provide help and documentation. Any such information should be easy to search, be .23 4%
focused on the user’s task, list concrete steps to be carried out, and not be too large.
B The usability principles used in the design of the Star user interface [16] 2.38
B1 Familiar user’s conceptual model: Use analogies and have the user interact with concrete objects .40
62 Seeing and pointing versus remembering and typing: Make objects and actions visible. Allow users to .7/lo7 1070
create new objects by copying and editing old ones.
EWhat you see is what you get: Screen representation of objects matches their non-computer representa-
B3 .47 ----i 6%
tion 3
B4 Universal commands: A few, basic generic commands used throughout the system .22 4%
B5 Consistency. 1.08 22%
B6 Simplicity Simple things should be simple; complex things should be possible. .40 6%
B7 Modeless interaction: Follow the noun-verb svntax. Have each mechanism serve one m. tm.ose. .19 3%
User tailorability: Allow speed-up of frequently performed operations (e.g., document templates, meta-
B8 .21 4~o
operations) and changes in interface appearance (e.g., change file sort order). I
156

Bos[onM,assachusUeSttsA* April24=281,994 HumaFnac{oirnsComputinSgystems
%?
Code Usability Heuristic
t
I C ,I Usabilitv . .txincird.es studied b.v, .H.o—lco__m_b and Tharp [4][5] 2.90 64%
cl Able to accompli ish the task for which the s~ftware is intended. .10
-—
Perform tasks reliably and without errors. .15
.51
Consistent key definition throughout .23
Show similar information at the same place on each screen. .36
El==== Learnable through natural, conceptual modeL .24 :
L
C7 Contains familiar terns andnatural language. .69 14%
C8 Provide statusinformation. .54 1190
C9 Don’t require information enteredonce to berecentered. .14 3%
Clo Provide lists of choices and allow picking from the lists. .08 o%
cl 1 Provide default values for input fields. .04 o%
C12 Prompt before destructive operations. .10 2%
C13 Show icons and other visual indicators. .11 270
cl 4 Immediate problem and error notification. .18 4T0
cl 5 Messages that provide specific instructions for actions. .49 9%
C16 On-line help system available. .07 1%
C17 Informative, written documentation. .10 2%
Cl 8 Ability to undo results of prior commands. .14 2%
cl 9 Ability tore-order or cancel tasks. .29 6%
C20 Allow access to operations from other applications/operating system from within the interface .05 1%
D Design principles for successful guessing suggested by Poison and Lewis [14] 2.31 47~o
DI Make the repertoire of available actions salient. .42 970
D2 Use identity cues between actions and user goals. .52 12%
D3 Use identity cues between system responses and user goals. .80 13%
D4 Provide an obvious way to undo actions. .28 6%
D5 Make available action alternatives easy to discriminate. .32 6%
D6 offer few alternatives: This increases the chance of guessing the correct one. .38 7%
D7 Tolerate at most one hard-to-understand action in a repertoire from which the user has to select. .13 2%
D8 Require as short a chain of choices aspossible to complete an action. .17 4%
E Artifact claims analysis questions listed by Carroll and Rosson [3] 1.99 4470
El How does the artifact evoke goals in the user? .41 7%
E2 How does the artifact encourage users to import pre-existing tasks? .21 2%
How does the artifact suggest that a particular task is appropriate or inappropriate?, simple or difficult?,
E3 .29 5%
basic or advanced?, risky or safe?
E4 What inappropriate goals are most likely?, most costly? .10 1Yo
What distinctions must be understood in order to decompose a task goal into methods?, how are these
E5 .39 7%
distinctions conveyed by the artifact?
E6 What planning mistakes are most likely?, most costly? .23 3%
How does the artifact encourage the use of background knowledge (concepts, metaphors, skills) in plan-
E7 .29 4%
ning a task?
E8 How- doesthe artifact make it easy or difficult to perform (execute) a task? .25 370
E9 What slips are most likely?, most costly? .30 6%
EIO How does the artifact indicate progress in task performance? .10 2%
Ell What are the most salient features of the artifact?, what do these features communicate to the user? .18 2%
E12 What features are commonly missed and at what cost? .17 3%
What features of the artifact change as users carry out a task?, what do these changes communicate to
E13 .26 4%
the user?
E14 How doesthe artifact guide the user to make correct inferences? .24 4%
E15 What incorrect inferences are most likely?, most costly? .13 2%
157

!%?!
HummFactorinsCompu{iSngystems CHI’94* “Ce/ebrffhI)M/Serdepemiwe”
J
Code Usability Heuristic
t16 How does the artifact encourage the use of background knowledge in making inferences? .06 o%
E17 How does the artifact convey completion of a task? .03 o%
E18 How does the artifact hekr users to recomize, diamtose, and recover from errOrS? .45 10%
E19 How does the artifact encourage elaboration and rerneval of task goals and methods? .11 170
F Human interface principles listed in the Macintosh Human Interface Guidelines [1] 3.09 6670
FI Metaphors from the real world to take advantage of people’s knowledge of the world. .31 6%
Direct manipulation: objects on screen remain visible while user performs physical actions on them,
F2 .24 3~o
and the impact of these operations is immediately visible.
F3 See-and-point instead of remember-and-type: users act by choosing between visible alternatives .43 8’70
F4 Consistency: same thing looks the same, same actions are done the same way. 1.11 22%
WYSIWYG (what you see is what you get): do not hide features (unless there is a way to make hidden
F5 .28 3%
things visible)
F6 User control: allow the user to initiate and control actions. .46 7%
Feedback: immediately show that user’s input has been received and is being operated on. Inform users
F7 .76 14%
of expected delays. Also, tell the user how to get out of the current situation.
F8 Forgiveness: make computer actions reversible. Always warn people before they lose data. .32 6%
F9 Perceived stability: finite set of objects that do not go away (but maybe dimmed). .35 5%
Aesthetic integrity: things should look good, keep graphic design simple, follow the graphic language of
FIO .77 12%
the interface without introducing arbitrary images to represent concepts.
Fll Modelessness: allow u.eou.le to do whatever they want whenever they want it. .20 3%
Accessibility for users who differ from the “average” user (cognitive or physical limitations, different
F12 .12 2%
culture and language of worldwide users)
G SunSoft usability guidelines [15] 3.31 7370
G1 Core functionality . should be understandable within an hour .04 1%
G2 System should speak the user’s language .78 14%
G3 System should understand the user’s language .29 6?Z0
G4 Feedback should be provided for all actions .32 6’%0
G5 Feedback should be timelv and accurate .57 12970
1 .-.
G9 I Interface should be lo~icallv ordered .12 2%
1
G13 I Reasonable defaults should be rxovided .07 1%
G14 Accelerators should be provided .31 6%
G15 Users should not have to enter system-accessible information .12 2%
Everything the user needs should be accessible through the GUI (or, in general, through whatever inter-
G16 .13 3%
face stvle is chosen for the interface)
G17 The user interface should be customizable .11 2%
G18 System should follow real-world conventions .72 15~o
G19 System should follow platform interface conventions .50 10%
G20 System should be effectively integrated with the rest of the desktop .06 270
G21 Keyboard core functions should be supported .17 3%
G22 System should be designed to prevent errors .49 8%
G23 Undo and redo should be suppofied .21 4%
G24 Good visual desism: There is no substitute for a good !zraDhic artist .54 7%
UNIX is a registered trademark of Unix System Laboratories
158