# MDA_Hunicke_2004

MDA: A Formal Approach to Game Design and Game Research
Robin Hunicke, Marc LeBlanc, Robert Zubek
hunicke@cs.northwestern.edu, marc_leblanc@alum.mit.edu, rob@cs.northwestern.edu
Abstract methodology will clarify and strengthen the iterative
processes of developers, scholars and researchers alike,
In this paper we present the MDA framework (standing for
making it easier for all parties to decompose, study and
Mechanics, Dynamics, and Aesthetics), developed and
taught as part of the Game Design and Tuning Workshop at design a broad class of game designs and game artifacts.
the Game Developers Conference, San Jose 2001-2004.
MDA is a formal approach to understanding games (cid:150) one Towards a Comprehensive Framework
which attempts to bridge the gap between game design and
development, game criticism, and technical game research. Game design and authorship happen at many levels, and
We believe this methodology will clarify and strengthen the the fields of games research and development involve
iterative processes of developers, scholars and researchers people from diverse creative and scholarly backgrounds.
alike, making it easier for all parties to decompose, study While it(cid:146)s often necessary to focus on one area, everyone,
and design a broad class of game designs and game regardless of discipline, will at some point need to consider
artifacts. issues outside that area: base mechanisms of game
systems, the overarching design goals, or the desired
experiential results of gameplay.
Introduction
AI coders and researchers are no exception. Seemingly
All artifacts are created within some design methodology. inconsequential decisions about data, representation,
Whether building a physical prototype, architecting a algorithms, tools, vocabulary and methodology will trickle
software interface, constructing an argument or upward, shaping the final gameplay. Similarly, all desired
implementing a series of controlled experiments (cid:150) design user experience must bottom out, somewhere, in code. As
methodologies guide the creative thought process and help games continue to generate increasingly complex agent,
ensure quality work. object and system behavior, AI and game design merge.
Specifically, iterative, qualitative and quantitative analyses Systematic coherence comes when conflicting constraints
support the designer in two important ways. They help her are satisfied, and each of the game(cid:146)s parts can relate to
analyze the end result to refine implementation, and each other as a whole. Decomposing, understanding and
analyze the implementation to refine the result. By creating this coherence requires travel between all levels of
approaching the task from both perspectives, she can abstraction (cid:150) fluent motion from systems and code, to
consider a wide range of possibilities and content and play experience, and back.
interdependencies.
We propose the MDA framework as a tool to help
This is especially important when working with computer designers, researchers and scholars perform this
and video games, where the interaction between coded translation.
subsystems creates complex, dynamic (and often
unpredictable) behavior. Designers and researchers must
MDA
consider interdependencies carefully before implementing
changes, and scholars must recognize them before drawing
Games are created by designers/teams of developers, and
conclusions about the nature of the experience generated.
consumed by players. They are purchased, used and
eventually cast away like most other consumable goods.
In this paper we present the MDA framework (standing for
Mechanics, Dynamics, and Aesthetics), developed and
Creates Consumes
taught as part of the Game Design and Tuning Workshop
Game
at the Game Developers Conference, San Jose 2001-2004
[LeBlanc, 2004a]. MDA is a formal approach to
Designer Player
understanding games (cid:150) one which attempts to bridge the
gap between game design and development, game The production and consumption of game artifacts.
criticism, and technical game research. We believe this

The difference between games and other entertainment
products (such as books, music, movies and plays) is that
their consumption is relatively unpredictable. The string of
events that occur during gameplay and the outcome of M D A
those events are unknown at the time the product is Player
finished. Designer
The MDA framework formalizes the consumption of The designer and player each have a different perspective.
games by breaking them into their distinct components:
When working with games, it is helpful to consider both
the designer and player perspectives. It helps us observe
Rules System (cid:147)Fun(cid:148) how even small changes in one layer can cascade into
others. In addition, thinking about the player encourages
experience-driven (as opposed to feature-driven) design.
(cid:133)and establishing their design counterparts:
As such, we begin our investigation with a discussion of
Aesthetics, and continue on to Dynamics, finishing with
the underlying Mechanics.
Mechanics Dynamics Aesthetics
Aesthetics
What makes a game (cid:147)fun(cid:148)? How do we know a specific
Mechanics describes the particular components of the
type of fun when we see it? Talking about games and play
game, at the level of data representation and algorithms.
is hard because the vocabulary we use is relatively limited.
Dynamics describes the run-time behavior of the
In describing the aesthetics of a game, we want to move
mechanics acting on player inputs and each others(cid:146)
away from words like (cid:147)fun(cid:148) and (cid:147)gameplay(cid:148) towards a
outputs over time.
more directed vocabulary. This includes but is not limited
to the taxonomy listed here:
Aesthetics describes the desirable emotional responses
evoked in the player, when she interacts with the game
system. 1. Sensation 5. Fellowship
Game as sense-pleasure Game as social framework
Fundamental to this framework is the idea that games are 2. Fantasy 6. Discovery
more like artifacts than media. By this we mean that the Game as make-believe Game as uncharted territory
content of a game is its behavior (cid:150) not the media that 3. Narrative 7. Expression
streams out of it towards the player. Game as drama Game as self-discovery
4. Challenge 8. Submission
Thinking about games as designed artifacts helps frame Game as obstacle course Game as pastime
them as systems that build behavior via interaction. It
supports clearer design choices and analysis at all levels of
For example, consider the games Charades, Quake, The
study and development.
Sims and Final Fantasy. While each are (cid:147)fun(cid:148) in their own
right, it is much more informative to consider the aesthetic
components that create their respective player experiences:
MDA in Detail
Charades: Fellowship, Expression, Challenge.
MDA as Lens
Quake: Challenge, Sensation, Competition, Fantasy.
Each component of the MDA framework can be thought of
The Sims: Discovery, Fantasy, Expression, Narrative.
as a (cid:147)lens(cid:148) or a (cid:147)view(cid:148) of the game (cid:150) separate, but causally
linked. [LeBlanc, 2004b]. Final Fantasy: Fantasy, Narrative, Expression,
Discovery, Challenge, Submission.
From the designer(cid:146)s perspective, the mechanics give rise to
dynamic system behavior, which in turn leads to particular
Here we see that each game pursues multiple aesthetic
aesthetic experiences. From the player(cid:146)s perspective,
goals, in varying degrees. Charades emphasizes Fellowship
aesthetics set the tone, which is born out in observable
over Challenge; Quake provides Challenge as a main
dynamics and eventually, operable mechanics.
element of gameplay. And while there is no Grand Unified
Theory of games or formula that details the combination
and proportion of elements that will result in (cid:147)fun(cid:148), this

taxonomy helps us describe games, shedding light on how For example, the model of 2 six-sided die will help us
and why different games appeal to different players, or to determine the average time it will take a player to progress
the same players at different times. around the board in Monopoly, given the probability of
various rolls.
Aesthetic Models
Using out aesthetic vocabulary like a compass, we can
define models for gameplay. These models help us
describe gameplay dynamics and mechanics.
For example: Charades and Quake are both competitive.
They succeed when the various teams or players in these
games are emotionally invested in defeating each other.
This requires that players have adversaries (in Charades,
teams compete, in Quake, the player competes against
computer opponents) and that all parties want to win.
It(cid:146)s easy to see that supporting adversarial play and clear
feedback about who is winning are essential to competitive
games. If the player doesn(cid:146)t see a clear winning condition,
Similarly, we can identify feedback systems within
or feels like they can(cid:146)t possibly win, the game is suddenly
gameplay to determine how particular states or changes
a lot less interesting.
affect the overall state of gameplay. In Monopoly, as the
leader or leaders become increasingly wealthy, they can
Dynamic Models
penalize players with increasing effectiveness. Poorer
Dynamics work to create aesthetic experiences. For players become increasingly poor.
example, challenge is created by things like time pressure
and opponent play. Fellowship can be encouraged by
sharing information across certain members of a session (a
team) or supplying winning conditions that are more
difficult to achieve alone (such as capturing an enemy
base).
Expression comes from dynamics that encourage
individual users to leave their mark: systems for
purchasing, building or earning game items, for designing,
constructing and changing levels or worlds, and for
creating personalized, unique characters. Dramatic tension
comes from dynamics that encourage a rising tension, a
release, and a denouement.
As with aesthetics, we want our discussion of dynamics to As the gap widens, only a few (and sometimes only one) of
remain as concrete as possible. By developing models that the players is really invested. Dramatic tension and agency
predict and describe gameplay dynamics, we can avoid are lost.
some common design pitfalls.
Using our understanding of aesthetics and dynamics, we
can imagine ways to fix Monopoly (cid:150) either rewarding
players who are behind to keep them within a reasonable
distance of the leaders, or making progress more difficult
for rich players. Of course (cid:150) this might impact the game(cid:146)s
ability to recreate the reality of monopoly practices (cid:150) but
reality isn(cid:146)t always (cid:147)fun(cid:148).
Mechanics
22 33 44 55 66 77 88 99 1100 1111 1122 Mechanics are the various actions, behaviors and control
Die Rolls mechanisms afforded to the player within a game context.
Together with the game(cid:146)s content (levels, assets and so on)
Probabilistic distribution of the random variable 2 D6.
the mechanics support overall gameplay dynamics.
63
ni
ecnahC
Thermometer
Room
Too Cold!
Controller
Too Hot!
A thermostat, which acts as a feedback system.
Move
Roll
Losers
$$$$$$ Pay Up!
Winners
$$$$$$
Cash In!
The feedback system in Monopoly.

For example, the mechanics of card games include cannot be evaluated in vacuo, aside from their effects on a
shuffling, trick-taking and betting (cid:150) from which dynamics system behavior and player experience.
like bluffing can emerge. The mechanics of shooters
include weapons, ammunition and spawn points (cid:150) which First Pass
sometimes produce things like camping and sniping. The
Consider an example Babysitting game [Hunicke, 2004].
mechanics of golf include balls, clubs, sand traps and
Your supervisor has decided that it would be beneficial to
water hazards (cid:150) which sometimes produce broken or
prototype a simple game-based AI for tag. Your player will
drowned clubs.
be a babysitter, who must find and put a single baby to
sleep. The demo will be designed to show off simple
Adjusting the mechanics of a game helps us fine-tune the
emotive characters (like a baby), for games targeted at 3-7
game(cid:146)s overall dynamics. Consider our Monopoly
year-old children.
example. Mechanics that would help lagging players could
include bonuses or (cid:147)subsidies(cid:148) for poor players, and
penalties or (cid:147)taxes(cid:148) for rich players (cid:150) perhaps calculated What are the aesthetic goals for this design? Exploration
when crossing the Go square, leaving jail, or exercising and discovery are probably more important than challenge.
monopolies over a certain threshold in value. By applying As such the dynamics are optimized here not for
such changes to the fundamental rules of play, we might be (cid:147)winning(cid:148) or (cid:147)competition(cid:148) but for having the baby
able to keep lagging players competitive and interested for express emotions like surprise, fear, and anticipation.
longer periods of time.
Hiding places could be tagged manually, paths between
Another solution to the lack of tension over long games of them hard-coded; the majority of game logic would be
Monopoly would be to add mechanics that encourage time devoted to maneuvering the baby into view and creating
pressure and speed up the game. Perhaps by depleting baby-like reactions. Gameplay mechanics would include
resources over time with a constant rate tax (so people talking to the baby ((cid:147)I see you!(cid:148) or (cid:147)boo!(cid:148)), chasing the
spend quickly), doubling all payouts on monopolies (so baby (with an avatar or with a mouse), sneaking about,
that players are quickly differentiated), or randomly tagging and so on.
distributing all properties under a certain value threshold.
Second Pass
Tuning Now, consider a variant of this same design (cid:150) built to work
Clearly, the last step our Monopoly analysis involves play with a franchise like Nickelodeon(cid:146)s (cid:147)Rugrats(cid:148) and aimed
testing and tuning. By iteratively refining the value of at 7-12 year-old-girls. Aesthetically, the game should feel
penalties, rate of taxation or thresholds for rewards and more challenging (cid:150) perhaps there is some sort of narrative
punishments, we can refine the Monopoly gameplay until involved (requiring several (cid:147)levels(cid:148), each of which
it is balanced. presents a new piece of the story and related tasks).
When tuning, our aesthetic vocabulary and models help us In terms of dynamics, the player can now track and interact
articulate design goals, discuss game flaws, and measure with several characters at once. We can add time pressure
our progress as we tune. If our Monopoly taxes require mechanics (i.e. get them all to bed before 9 pm), include a
complex calculations, we may be defeating the player(cid:146)s (cid:147)mess factor(cid:148) or monitor character emotions (dirty diapers
sense of investment by making it harder for them to track cause crying, crying loses you points) and so on.
cash values, and therefore, overall progress or competitive
standings. For this design, static paths will no longer suffice (cid:150) and it(cid:146)s
probably a good idea to have them choose their own hiding
Similarly, our dynamic models help us pinpoint where places. Will each baby have individual characteristics,
problems may be coming from. Using the D6 model, we abilities or challenges? If so, how will they expose these
can evaluate proposed changes to the board size or layout, differences to the player? How will they track internal
determining how alterations will extend or shorten the state, reason about the world, other babies, and the player?
length of a game. What kinds of tasks and actions will the player be asked to
perform?
MDA at Work Third Pass
Finally, we can conceive of this same tag game as a full-
Now, let us consider developing or improving the AI blown, strategic military simulation (cid:150) the likes of Splinter
component of a game. It is often tempting to idealize AI Cell or Thief. Our target audience is now 14-35 year old
components as black-box mechanisms that, in theory, can men.
be injected into a variety of different projects with relative
ease. But as the framework suggests, game components Aesthetic goals now expand to include a fantasy element
(role-playing the spy-hunting military elite or a loot-

seeking rogue) and challenge can probably border on better decompose that experience, and use it to fuel new
submission. In addition to an involved plot full of intrigue designs, research and criticism respectively.
and suspense, the player will expect coordinated activity
on the part of opponents (cid:150) but probably a lot less
emotional expression. If anything, agents should express References
fear and loathing at the very hint of his presence.
Barwood, H. & Falstein, N. 2002. (cid:147)More of the 400:
Discovering Design Rules(cid:148). Lecture at Game Developers
Dynamics might include the ability to earn or purchase
Conference, 2002. Available online at:
powerful weapons and spy equipment, and to develop
http://www.gdconf.com/archives/2002/hal_barwood.ppt
tactics and techniques for stealthy movement, deceptive
behavior, evasion and escape. Mechanics include
Church, D. 1999. (cid:147)Formal Abstract Design Tools.(cid:148) Game
expansive tech and skill trees, a variety of enemy unit
Developer, August 1999. San Francisco, CA: CMP Media.
types, and levels or areas with variable ranges of mobility,
Available online at:
visibility and field of view and so on.
http://www.gamasutra.com/features/19990716/design_tool
s_01.htm
Agents in this space, in addition to coordinating movement
and attacks must operate over a wide range of sensory
Hunicke, R. 2004. (cid:147)AI Babysitter Elective(cid:148). Lecture at
data. Reasoning about the player(cid:146)s position and intent
Game Developers Conference Game Tuning Workshop,
should indicate challenge, but promote their overall
2004. In LeBlanc et al., 2004a. Available online at:
success. Will enemies be able to pass over obstacles and
http://algorithmancy.8kindsoffun.com/GDC2004/AITutori
navigate challenging terrain, or will you (cid:147)cheat(cid:148)? Will
al5.ppt
sound propagation be (cid:147)realistic(cid:148) or will simple metrics
based on distance suffice?
LeBlanc, M., ed. 2004a. (cid:147)Game Design and Tuning
Workshop Materials(cid:148), Game Developers Conference 2004.
Wrapping Up
Available online at:
Here we see that simple changes in the aesthetic
http://algorithmancy.8kindsoffun.com/GDC2004/
requirements of a game will introduce mechanical changes
for its AI on many levels (cid:150) sometimes requiring the LeBlanc, M. 2004b. (cid:147)Mechanics, Dynamics, Aesthetics: A
development of entirely new systems for navigation, Formal Approach to Game Design.(cid:148) Lecture at
reasoning, and strategic problem solving. Northwestern University, April 2004. Available online at:
http://algorithmancy.8kindsoffun.com/MDAnwu.ppt
Conversely, we see that there are no (cid:147)AI mechanics(cid:148) as
such (cid:150) intelligence or coherence comes from the
interaction of AI logic with gameplay logic. Using the
MDA framework, we can reason explicitly about aesthetic
goals, draw out dynamics that support those goals, and
then scope the range of our mechanics accordingly.
Conclusions
MDA supports a formal, iterative approach to design and
tuning. It allows us to reason explicitly about particular
design goals, and to anticipate how changes will impact
each aspect of the framework and the resulting
designs/implementations.
By moving between MDA(cid:146)s three levels of abstraction, we
can conceptualize the dynamic behavior of game systems.
Understanding games as dynamic systems helps us develop
techniques for iterative design and improvement (cid:150)
allowing us to control for undesired outcomes, and tune for
desired behavior.
In addition, by understanding how formal decisions about
gameplay impact the end user experience, we are able to