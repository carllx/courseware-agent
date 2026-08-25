# Nielsen_Molich_1990_Heuristic_Evaluation

CHI 90 Procee&qs April 1990
HEURISTIC EVALUATION OF USER INTERFACES
Jukob Nielsen and Rolf Molich
Technical University of Denmark B altica A/S
Department of Computer Science Mail Code B22
DK-2800 Lyngby Copenhagen Klausdalsbrovej 601
Denmark DK-2750 Ballerup
dat JN@NEUVMl . bitnet Denmark
ABSTRACT ical or formal evaluation methods.
Heuristic evaluation is an informal method of usability In real life, most user interface evaluations are heuristic
analysis where a number of evaluators are presented with evaluations but almost nothing is known about this kind of
an interface design and asked to comment on it. Four ex- evaluation since it has been seen as inferior by most re-
periments showed that individual evaluators were mostly searchers. We believe, however, that a good strategy for
quite bad at doing such heuristic evaluations and that they improving usability in most industrial situations is to study
only found between 20 and 51% of the usability problems those usability methods which are likely to see practical
in the interfaces they evaluated. On the other hand, we use [Nielsen 19891. Therefore we have conducted the
could aggregate the evaluations from several evaluators to series of experiments on heuristic evaluation reported in
a single evaluation and such aggregates do rather well, this paper.
even when they consist of only three to five people.
KEYWORDS: Usability evaluation, early evaluation, us- HEURISTIC EVALUATION
ability engineering, practicaml ethods.
As mentioned in the introduction, heuristic evaluation is
INTRODUCTION done by looking at an interface and trying to come up with
an opinion about what is good and bad about the interface.
There are basically four ways to evaluate a user interface: Ideally people would conduct such evaluations according
Formally by some analysis technique, automatically by a to certain rules, such as those listed in typical guidelines
computerized procedure, empirically by experiments with documents. Current collections of usability guidelines
teat users, and heuristically by simply looking at the inter- [Smith and Mosier 19861 have on the order of one thou-
face and passing judgement according to ones own opinion. sand rules to follow, however, and are therefore seen as in-
Formal analysis models are currently the object of ex- timidating by developers. Most people probably perform
tensive research but they have not reached the stage where heuristic evaluation on the basis of their own intuition and
they can be generally applied in real software development common sense instead.
projects. Automatic evaluation is completely infeasible ex-
cept for a few very primitive checks. Therefore current We have tried cutting the complexity of the rule base by
practice is to do empirical evaluations if one wants a good two orders of magnitudes by relying on a small set of
and thorough evaluation of a user interface. Unfortunately, heuristics such as the nine basic usability principles from
in most practical situations, people actually do nof conduct [Molich and Nielsen 1990-Jli sted in Table 1. Such smaller
empirical evaluations because they lack the time, expertise, sets of principles seem more suited as the basis for
inclination, or simply the tradition to do so. For example, practical heuristic evaluation. Actually the use of very
M.&ted et al. 119893f ound that only 6% of Danish compa-
nies doing software development projects used the thinking
aloud method and that nobody used uny other other empir- Simple and natural dialogue
Speak the user’s language
Minimize user memory load
Be consistent
Provide feedback
Provide clearly marked exits
Provide shortcuts
Good error messages
Permission to copy without fee all or part of this material is granted Prevent errors
provided that the copies are not made or distributed for direct
Table 1. Nine usability heuristics {discussed
commercial advantage, the ACM copyright notice and the title of
the publication and its date appear, and notice is given that copying further h [Molich and Nielsen 19901).
is by permission of the Association for Computing Machinery. TO
copy otherwise, or to republish requires a fee and/or specific
permission.
249
0 1990 ACM O-89791 -345-O/90/0004-0249 1.50

Cl-II 90 procee&ngs Apil1990
complete and detailed guidelines as checklists for evalua- many situations it is realistic to wanott o conduct a usability
tions might be considered a. formalism, especially when evaluation in the specification stage of a software develop-
they take the form of interface stand;&. ment process where no running system is yet available.
We have developed this specific list of heuristics during The evaluators were 37 computer science students who
several years of experience with te.aching and consulting were taking a class in user interface design and had had a
about usability engineering [Nielsen and Molich 19891. lecture on our evaluation heuristics before the experiment.
The nine heuristics can be presented in a single lecture and The interface contained a total of 52 known usability
explain a very large proportion of the problems one ob- problems.
serves in user interface designs. These nine principles cor-
respond more or less to principles which are generally ret- Experiment 2: Mantel
ognized in the user interface commu.nity, and most people
For experiment 2 we used a design which was constructed
might think that they were “obvious”’ if it was not because
for the purpose of the test. Again the evaluators had access
the results in the following sections of this paper show that
only to a written specification and not to a running system.
they am difficult to apply in practice. The reader is referred
The system was a design for a small information system
to wolich and Nielsen 19901 for a more detailed expla-
which a telephone company wolild make available to its
nation of each of the nine heuristics.
customers to dial in via their modems to find the name and
address of the subscriber having a ,given telephone number.
EMPIRICAL TEST OF HEURISTIC EVALUATION
This system was called “Mantel” as an abbreviation of our
To test the practical applicability of heuristic evaluation, hypothetical telephone company,. Manhattan Telephone
we conducted four experiments where people who were not (neither the company nor the system has any relation to any
usability experts analyzed a user interface heuristically. existing company or system). The entire system design
The basic method was the same in all four experiments: consisted of a single screen and a :few system messagess o
The evaluators (“subjects”) were given a user interface de- that the specification could be contained on a single page.
sign and asked to write a report pointing out the usability
problems in the interface as precisely as possible. Each re- The design document used for this experiment is reprinted
port was then scored for the usability problems that were as an appendix to [Molich and Nielsen 19901 which also
mentioned in it. The scoring was done by matching with a gives a complete list and in-depth explanation of the 30
list of usability problems developed by the authors. Actu- known usability problems in the Mantel design.
ally, our lists of usability problems had to be modified after
we had made an initial pass through the reports, since our The evaluators were readers of the Danish Computerworld
evaluators in each experiment discovered some problems magazine where our design was printed as an exercise in a
which we had not originally identified ourselves. This contest. 77 solutions were mailed in, mostly written by in-
shows that even usability experts are not perfect in doing dustrial computer professionals. Our main reason for con-
ducting this experiment was to ensure that we had data
heuristic evaluations.
from real computer professionals and not just from stu-
dents. We should note that these evaluatnrs did not have
Scoring was liberal to the extent that credit was given for
the mentioning of a usability problem even if it was not de- the (potential) benefit of having attended our lecture on the
scribed completely. usability heuristics.
Table 2 gives a short summary of the four experiments Experiments 3 and 4: Two Voice Response Systems:
which are described further in the following. “Savings” and “Transport”
Experiments 3 and 4 were conducted to get data from
heuristic evaluations of “live” systems (as opposed to the
specification-only designs in experiments 1 and 2). Both
experiments were done with the same.g roup of 34 com-
puter science students as evaluators. Again, the students
were taking a course in user interface design and were
given a lecture on our usability heuristics, but there was no
overlap between the group of evaluators in these experi-
ments and the group from experiment 1.
Tabk 2. Summaryo f the four experiments.
Both interfaces were “voice response” systems where users
Experiment 1: Telsdata would dial up an information system from a touch tone
Experiment 1 tested the user interlace to the Danish video- telephone and interact with the system by pushing buttons
tex system, Teledata. The evaluators were given a set of ten on the 12-key keypad. The first syqem was run by a large
screen dumps from the general search system and from the Savings Union to give their customers information about
Scandinavian Airlines (SAS) subsystem. This means that their account balance, current foreign currency exchange
the evaluators did not have accesst o a “live” system, but in rates, etc. This interface is refer& to as the “Savings” de-
250

CHI !30 l’meedings April 1990
sign in this article and it contained a total of 48 known us- THE USABILITY PROBLEMS
ability problems. The second system was used by the mu-
nicipal public transportation company in Copenhagen to We have already mentioned a usability problem related to
provide commuters with information about bus routes. This the “consistency” rule in the description of experiments 3
interface is referred to as the “Transport” design and had a and 4. A few other examples of usability problems am:
total of 34 known usability problems. l The Mantel system overwrites the telephone number en-
tered by the user so that it is no longer visible when the
Them were four usability problems which were related to name and address of the corresponding subscriber is dis-
inconsistency across the two voice response systems, Since played (found by 95%).
the two systems are aimed at the same user population in l The Transport system shifts from reading submenus to
reading the main menu without any pause or indication that
the form of the average citizen and since they are accessed
through the same terminal equipment, it would improve the user is moved to another level of menu (found by 62%).
their collective usability if they both used the same The error message “IJNKNOWN IP” in Teledata (where
l
conventions. Unfortunately there are differences, such as IP stands for information provider) can be made much
more readable (found by 54%).
the use of the square1 key. In the Savings system, it is an
end-of-command control character, while it is a command l Users who do not have the printed user’s guide wiIl never
learn that the Savings system has an online help facility
key for the “return to the main menu” command in the
(found by 35%).
Transport system which does not use an end-of-command
9 The key to accessing certain information in the Transport
key at ah. The four shared inconsistency problems have
system is the transport company’s internal departmental or-
been included in the count of usability problems for both
ganization instead of the bus numbers known by the public
systems.
(found by 12%).
Since the same evaluators were used for both voice re-
The validity of these usability problems is an important
sponse experiments, we can compare the performance of
question: WiIl they in fact present problems to real users,
the individual evaluators. In this comparison, we have ex-
and to what degree do they constitute the complete set of
cluded the four consistency problems discussed above
usability problems? We have not conducted traditional
which are shared among the two systems. A regression
empirical usability tests to measure this. On the other hand,
anaIysis of the two sets of evaluations is shown in Figure 1
we do have two arguments in support for the validity of the
and indicates a very weak correlation between the perfor-
problems as usabihty problems. The first argument is sim-
mance of the evaluators in the two experiments (R2=0.33,
ply that most of these design issues are “obviously” prob-
p<O.Ol). So while some people are better than others at
lems according to established knowledge in the usability
doing heuristic evaluation of user interfaces, this tendency
field. The second, and perhaps more convincing argument
is not very strong. We do not have enough evidence to
is that the very method of our experiments actualIy forms a
form a firm conclusion but it seems that it might be the
kind of empirical support for the usabihty problems. For
case that there is very little consistency in the ability of
evaluators to find usability problems. ‘Ihe two evaluations
compared in Figure 1 concerned quite similar interfaces
(both were voice response systems), and it would be a
plausible hypothesis that evaluators would perform even
less consistently in evaluations of more varied systems.
We should note that the evaluators in these two experi-
ments all had the same level of usability expertise. Even
though we do not have formal evidence to show this, we do
believe that usability experts will be better at heuristic
evaluation than average computer professionals. It is likely
that experience in usability and empirical user tests pro-
vides a good background for recognizing and conceptua.li~
ing usability problems. With regard to the latter, expertise 8 1 II . , . , _ , _ , j
in running user tests would probably not be as much help %
as the observations of actual user behavior made by the 10% 30% 50%
experienced tester over the years.
Problems found in Transport design
Figure 1. Scatterplot of the proportion of
usability problems found by the same
evaluators in two different interfaces. The
1 This key is also sometimes called the “pound key”. In regression line has I?=033 and shows that
fact one of the inconsistency problems was that this single there is only a very weak correlation between
key had two different names in the two systems (firkant the evaluators’ perforniance in the two
and rude, respectively, in Danish). experiments.
251

CHI 90 Proceediw
- Teledata
- Mantel
40-49% 60-69% 80-89%
Proportion of the total number of usability problems found in each interface
Figure 2. Distribution for each of the four experiments of the number of usability problems found by the
evaluators (expressed as percent of the total number of problems in each interface to enable comparisons).
each system we have had at least 34 people work their way vidual usability “problems” in the phase of a development
through the interface. If we view these people as experi- process where one has completed the overall design and
mental subjects rather than as evaluators, we realize that it needs to polish it. It would also be interesting to consider
is very unlikely that any of the systems would have had any more holistic evaluations of entire interfaces such as those
major usability problem which did not bother some of these that would be required to select which of two competing
subjects enough to complain about it in their report. products to purchase or which of two completely different
design approaches to pursue. It is likely, however, that a
In spite of these arguments, it is alwa,ysi mpossible to know different set of techniques will be needed for that kind of
for sure whether one has found every single usability evaluation.
problem in an interface. It might be. that the next subject
would stumble over something new. Therefore we have EVALUATION RESULTS
stated for each experiment the ‘known” number of usabil-
ity problems, and the statistics in the following sections are The most basic resnlt from the four experiments is that
based on this number of known problems. heuristic evaluation is difficult. The average proportion of
usability problems found was $l%., 38%, 26%, and 20% in
Furthermore, the usability problems of an interface do not the four experiments respectively. So even in the best case
form a fixed set in real life. For any actual use of a system only half of the problems were found, and the general case
by real users in a real context, only some of its potential was rather poor. Actually, even these numbers are not all
weaknesses will surface as problems. Some aspects of a that bad. Even finding some problems is of course much
design might never bother a particular user and could better than tiding no problems, and one could supplement
therefore not be said to be “problems” as far as that user is the heuristic method with other usability engineering meth-
ods to increase the total number of problems found.
concerned. Even so, we will still consider a design item as
a usability problem if it could be expected to bother some
users during some reasonable use of the system. The deci- Figure 2 shows the distribution of the number of problems
sion whether or not to remove the problem in a redesign found in each of the four experiments. We can see that the
should then be based on a judgement of the number of distributions as expected mostly have a shape like the nor-
users it impacts and a trade-off analysis of whether remov- mal distribution, even though the curve for the Transport
experiment is somewhat skewed. In other words, most
ing it would reduce the efficiency of use or other desirable
usability parameters for other users. One can only get the evaluators do about average, a few do very well, and a few
option to make this judgement and trade-off analysis, how- do rather badly.
ever, if one has identified the usability problem in the first
Table 3 presents information related to individual differ-
place.
ences in the performance of evalu.ators. First, the number
A weakness of our approach is that we only looked at indi- of usability problems found is expressed in percent of the
Table 3. Individual differences in evaluators’ ability to find usability problems.
252

CHI 90 Pmceedngs
poor 4 b good
Evaluator’s ability to find usability problems
Mantel exneriment
hard Figure 3. Diagrams showing who found which usabil-
ity problems.
8 l
m Each column corresponds to one evaluator, and each
row corresponds to one usability problem. Each
n l square indicates whether one evaluator found one
problem. That square is black if the evaluator as-
signed to the column found the problem assigned tc
the row and white if that evaluator did not find that
problem.
For each experiment, the evaluators are sorted ac-
cording to the number of problems they found, and the
problems are sorted according to how many evalua-
tors found them.
The figure shows the data from the Mantel and Sav-
ings experiments, but the diagrams for the other two
experiments look similar.
Black squares in the upper left corners indicate hart;
problems found by poor evaluators while whitt
squares in the bottom right indicate easy problems
find usability problems ~o verlooked by good evaluators.
Savings exwriment
total number of usability problems in each interface. For
each of the five experiments, the table then lists the pro- We see from Tables 2 and 3 that some systems are easier to
portion of problems found by the worst and best evaluator, evaluate heuristically than others. One interesting trend
the first and ninth de&e, and first and third quartile, as from Table 3 is that the individual differences between
well as the ratios between these values: In the Mantel ex- evaluators are larger the more difficult the interface is to
periment, one of the evaluators did not find any problems evaluate. Table 2 further shows that the voice response sys-
at all, so the table also lists the problems found by the sea tems were especially hard to evaluate. The problem with
ond worst evaluator. The Mantel experiment has been ex- heuristic evaluation of voice interfaces is that they have an
cluded from the calculation of the averages of the mini- extremely low persistence [Nielsen 19871 because all sys-
mums and of the max/min ratios. tem messages are gone as soon as they are uttered. This
again means that evaluators get no chance to ponder details
We see that the individual differences correspond to the of the interface design at their leisure.
Q3/Q1 ratios of about 2 listed by Egan [1988] for text edit-
In general, there were rather few false positives in the form
ing but are lower than the ratios of 2 to 4 listed for infonna-
tion search and for programming. They correspond closely of evaluators stating that something was a usability prob-
lem when we would not classify it as such. Therefore we
to the QS/Q 1 ratio of 1.8 for time needed to learn
have not conducted a formal analysis of false positives. For
HyperCard programming [Nielsen 19901 by the same
a practical application of heuristic evaluation, false posi-
category of computer science students as those used in
tives might present a problem to the extent that one evalua-
three of the four experiments.
tor’s finding of a false positive could sidetrack the discus-
253

CHI 90 Proceedings April 1990
sion in a development group. Our experience is that a given
false positive normally is not found by more than a single Because of this phenomenon, we have the potential for dra-
evaluator, so the other members of the development group matically improving the overall result by forming aggre-
should be able to convince the finder of the false positive gares of evaluators since the “collected wisdom” of several
that it is not a real usability problem. If not, then an evaluators is not just equal to that of the best evahrator in
empirical test couId serve as the ultimate arbiter. We would the group. Aggregates of evaluators, are formed by having
in general recommend that one does not rely exclusively on several evaluators conduct a heuristic evaluation and then
heuristic evaluation during the usability engineering collecting the usability problems found by each of them to
process. Such methods as thinking aloud should be used to form a larger set.
supplement the heuristic evaluation results in any case.
For tbis aggregation process to work, we have to assume
We should note that we have only tested heuristic evalua- that there is some authority that is able to read through the
tion of fairly small-scale interfaces. We do not know what reports from the individual evaluators and recognize the
happens during the heuristic evaluatioa of much larger in- usability problems from each report. This authority could
terface designs. Furthermore, we studied evaluations of be a usability expert or or it could be the group itself during
complete designs in the form of paper prototypes or nm- a meeting of the evaluators. We have not tested this
ning systems. It is also of interest what happens during the assumption empirically but it seemsr easonable for the kind
“inner loop” of design [Newell and Card 19851 where a of usability problems discussed in tbis paper since they are
designer rapidly evaluates various alternative subdesigns of a nature where they are “obvious”’ as soon as somebody
before they are finalized in a complete design. It is likely has pointed them out.
that such evaluations are often heuristic in nature, so some
of the same results may apply. Our experience from conducting the four experiments and
discussing them with the evaluators indicates that people
AGGREGATED EVALUATIONS are usually willing to concede that s~omethingi s a usability
problem when it is pointed out to them by others. At least
Figure 2 and Table 3 show that some evaluators do better for the kind of usability problems considered in this paper,
than others. One might have supposed that the difference in the main difticulty lies in finding them in the first place,
performance between evaluators was due to an inherent not in agreeing on the aggregated list.
rank ordering of the difficulty of finding the usability
problems, such that a “good” evaluator would be able to On the basis of our data showing which evaluators found
find all the easy problems found by a “poor” evaluator as which usability problems, we have constructed hypotheti-
well as some additional, harder problems. Figure 3 shows, cal aggregates of varying sixes to test how many problems
however, that this is not the case. Even poor evaluators can such aggregates would theoretically find. The aggregates
sometimes find hard problems as indicated by the black were not formed in a real project but given our assumption
squares in the upper left part of the diagrams. And good of a perfect authority to form the conclusions, that should
evaluators may sometimes overlook: easy problems as make no difference. For each of our four experiments, ag-
indicated by the white squares in the lower right part of the gregates were formed by choosing the number of people in
diagrams. In other words, the finding of usability problems the aggregate randomly from the total set of evaluators in
does not form a perfect cumulative scale (a Guttman2 scale that experiment. For each experiment, it would of course
[Guttman 19441). have been possible to select an optimal aggregate of the
better evaluators but in a real company one would not have
that luxury. Normally one would have to use whatever staff
2 The evaluations do approximate a Guttrnan scale with an was available, and that staff would have been hired on the
average Guttman reproducibility coefficient R = 0.85 basis of many other qualifications than their score in
(coefficients ranging from 0.82 to 0.87). The average heuristic evaluation experiments. And in any case, Figure 1
minimal marginal reproducibility, MMR is 0.80 (ranging indicates that people who are good evaluators in one exper-
from 0.79 to 0.82), however, indicating that the scale is not iment may not be all that good in the next experiment.
truly unidimensional and cumulative since the coefficient
of scalability is only 0.06. The Guttman coefficient indi- Figure 4 shows the results from selecting random aggre-
cates the degree to which the data follows a nnidimen- gates of evaluators. The figure shows the average number
sional cumulative scale, with a value of 1 indicating a per- of usability problems found by each size of aggregate.
fect scale. The Guttman coefficient of ~0.85s hows that only These averages were calculated by a Monte Carlo tech-
15% of the data deviates from that expected of such a per- nique where we selected between five and nine thousand
fect scale. But the minimal marginal reproducibility indi-
cates the degree to which the individual values could be
predicted from the average values even disregarding predicting for each evaluator that he or she would not find
potential scaling properties. From knowing e.g. that a the problem. So the assumption of strict ordering only
certain usability problem was only found by 20% of the gains us an improvement from 80% to 85%. indicating that
evaluators, we would be able to correctly predict 80% of it has poor explanatory powers. Ln any case, it is the
the data for that problem without taking that evaluators deviation of 15% from the Guttman scale which allows US
general problem-finding abilities into account by just to form the aggregates we discuss here.
254

CHI 90 l’vxx&ngs April 1990
0 5 10 15 20 25 30
Number of evaluators in aggregate
Figure 4. Proportion of usability problems found by aggregates of size 1 to 30.
random aggregatesf or each aggregate size and experiment. each other towards a certain way of approaching the analy-
Table 4 gives the exact numbers for selected sixes of ag- sis and therefore only discover certain usability problems.
gregates. It is likely that the variety in discovered usability problems
apparent in our experiments would have been smaller if the
It is apparent from Figure 4 that the cmves for the four ex- evaluators had worked in groups. And it is of course the
periments have remarkably similar shapes.E ach curve rises variety which is the reason for the improvement one gets
drastically in the interval from one evaluator to about five from using aggregates of evaluators.
evaluators, it then flattens out somewhat around the in-
terval from five to ten evaluators, and the point of dimin- CONCLUSIONS
ishing returns seemst o have been reached at aggregates of
about ten evaluator. It is interesting to see that even for the This study shows that heuristic evaluation is difficult and
Transport interface which was the hardest to analyze, that one should not rely on the results of having a single
aggregates of five evaluators are still able to find more than person look at an interface. The results of a heuristic evalu-
half of the usability problems. In general, we would expect ation will be much better if you have several people con-
aggregates of five evaluators to find about two thirds of the duct the evaluation, and they should probably do so inde-
usability problems which is really quite good for an infor- pendently of each other. The number of usability results
mal and inexpensive technique like heuristic evaluation. found by aggregates of evaluators grows rapidly in the in-
terval from one to five evaluators but reaches the point of
For the aggregated evaluation to produce better results than diminishing returns around the point of ten evaluators. We
the individual evaluations, it is likely that the evaluators recommend that heuristic evaluation is done with between
should do their initial evaluations independently of each three and five evaluators and that any additional resources
other and only compare results after each of them has are spent on alternative methods of evaluation.
looked at the design and written his/her evaluation report.
The reason we believe this is that evaluators working to- Major advantages of heuristic evaluation am:
gether in the initial evaluation phase might tend to bias It is cheap.
l
It is intuitive and it is easy to motivate people to do it.
l
It does not require advance planning.
l
It can be used early in the development process.
l
~1 A disadvantage of the method is that it sometimes identi-
fies usability problems without providing direct sugges-
tions for how to solve them. The method is biased by the
current mindset of the evaluators and normally does not
Table 4. Average proportion #usability problems
generate breakthroughs in the evaluated design.
found in each of the four interfaces for various sized
aggregates of evaluators.
255

CHI 90 procee&w April1990
ACKNOWLEDGEMENTS interface design. Communications of the ACM 33,3
(March 1990).
The authors would like to thank Jan C. Clausen, John
5. Newell, .A. and Card, SK. The prospects for psycho-
Schnizlein. and the anonymous CifKW referees for helpful
logical science in human-computer interaction. Hu-
comments.
man-computer Znteraction 1,3 (1985), 209-242.
6. Nielsen, J. Classification of dialog techniques: A
REFERENCES
CHI+GI’87 workshop, Toronto,, April 6, 1987. ACM
1. Egan, D.E. Individual differences in human-computer SIGCHI ,Bulletin 19,2 (October 1987), 30-35.
interaction. In: M. Helander (Ed.) Handbook ofHu- 7. Nielsen, J. Usability engineering at a discount, in Sal-
man-Computer Interaction,. Elsevier Science Publish- vendy, G. and Smith, M.J. (Eds.): Designing and Us-
ers, Amsterdam, 1988, pp. 543-568. ing Human-Computer Interfoxes and Knowledge
2. Guttmau, L. A basis for scaling qualitative data. Amer- Bused Systems. Elsevier Sciencle Publishers, Amster-
ican Sociological Review 9 (1944),, 139-150. dam 198!), 394-401.
3. M&ted, U., Vamild, A., and Jorgensen, A.H. Hvordan 8. Nielsen, J. Assessing the learnability of HyperCard as
sikres kvaliteten af brugergrrensefladen i systemud- a programming language. Manuscript submitted for
viklingen (“Assuring the quality of user interfaces in publication 1990.
system development,” in Danish). hoc. No&DATA’89 9. Nielsen, J. and Molich, R. Teaching user interface de-
Joint Scandinavian Computer Conference (Copen- sign based on usability engineering. ACM SIGCHZ
hagen, Denmark, 19-22 June 1989),479-484. Bulletin 21, 1 (July 1989), 45-48.
4. Molich, R. and Nielsen, J. Improving a human-com- 10. Smith, S.L. and Mosier, J.N. Guidelines for Designing
puter dialogue: What designers know about traditional User Interface Software. Report MTR-10090, The
MITRE Cop, Bedford, MA, August 1986.
256