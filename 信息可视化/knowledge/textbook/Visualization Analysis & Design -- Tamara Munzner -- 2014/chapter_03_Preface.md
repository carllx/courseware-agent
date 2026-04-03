# Preface

# Why a New Book?

I wrote this book to scratch my own itch: the book I wanted to teach out of for my graduate visualization (vis) course did not exist. The itch grew through the years of teaching my own course at the University of British Columbia eight times, co-teaching a course at Stanford in 2001, and helping with the design of an early vis course at Stanford in 1996 as a teaching assistant.

I was dissatisfied with teaching primarily from original research papers. While it is very useful for graduate students to learn to read papers, what was missing was a synthesis view and a framework to guide thinking. The principles and design choices that I intended a particular paper to illustrate were often only indirectly alluded to in the paper itself. Even after assigning many papers or book chapters as preparatory reading before each lecture, I was frustrated by the many major gaps in the ideas discussed. Moreover, the reading load was so heavy that it was impossible to fit in any design exercises along the way, so the students only gained direct experience as designers in a single monolithic final project.

I was also dissatisfied with the lecture structure of my own course because of a problem shared by nearly every other course in the field: an incoherent approach to crosscutting the subject matter. Courses that lurch from one set of crosscuts to another are intellectually unsatisfying in that they make vis seem like a grabbag of assorted topics rather than a field with a unifying theoretical framework. There are several major ways to crosscut vis material. One is by the field from which we draw techniques: cognitive science for perception and color, human–computer interaction for user studies and user-centered design, computer graphics for rendering, and so on. Another is by the problem domain addressed: for example, biology, software engineering, computer networking, medicine, casual use, and so on. Yet another is by the families of techniques: focus+context, overview/detail, volume rendering,

and statistical graphics. Finally, evaluation is an important and central topic that should be interwoven throughout, but it did not fit into the standard pipelines and models. It was typically relegated to a single lecture, usually near the end, so that it felt like an afterthought.

# Existing Books

Vis is a young field, and there are not many books that provide a synthesis view of the field. I saw a need for a next step on this front.

Tufte is a curator of glorious examples [Tufte 83, Tufte 91, Tufte 97], but he focuses on what can be done on the static printed page for purposes of exposition. The hallmarks of the last 20 years of computer-based vis are interactivity rather than simply static presentation and the use of vis for exploration of the unknown in addition to exposition of the known. Tufte’s books do not address these topics, so while I use them as supplementary material, I find they cannot serve as the backbone for my own vis course. However, any or all of them would work well as supplementary reading for a course structured around this book; my own favorite for this role is Envisioning Information [Tufte 91].

Some instructors use Readings in Information Visualization [Card et al. 99]. The first chapter provides a useful synthesis view of the field, but it is only one chapter. The rest of the book is a collection of seminal papers, and thus it shares the same problem as directly reading original papers. Here I provide a book-length synthesis, and one that is informed by the wealth of progress in our field in the past 15 years.

Ware’s book Information Visualization: Perception for Design [Ware 13] is a thorough book on vis design as seen through the lens of perception, and I have used it as the backbone for my own course for many years. While it discusses many issues on how one could design a vis, it does not cover what has been done in this field for the past 14 years from a synthesis point of view. I wanted a book that allows a beginning student to learn from this collective experience rather than starting from scratch. This book does not attempt to teach the very useful topic of perception per se; it covers only the aspects directly needed to get started with vis and leaves the rest as further reading. Ware’s shorter book, Visual Thinking for Design [Ware 08], would be excellent supplemental reading for a course structured around this book.

This book offers a considerably more extensive model and framework than Spence’s Information Visualization [Spence 07]. Wilkinson’s The Grammar of Graphics [Wilkinson 05] is a deep and thoughtful work, but it is dense enough that it is more suitable for vis insiders than for beginners. Conversely, Few’s Show Me The Numbers [Few 12] is extremely approachable and has been used at the undergraduate level, but the scope is much more limited than the coverage of this book.

The recent book Interactive Data Visualization [Ward et al. 10] works from the bottom up with algorithms as the base, whereas I work from the top down and stop one level above algorithmic considerations; our approaches are complementary. Like this book, it covers both nonspatial and spatial data. Similarly, the Data Visualization [Telea 07] book focuses on the algorithm level. The book on The Visualization Toolkit [Schroeder et al. 06] has a scope far beyond the vtk software, with considerable synthesis coverage of the concerns of visualizing spatial data. It has been used in many scientific visualization courses, but it does not cover nonspatial data. The voluminous Visualization Handbook [Hansen and Johnson 05] is an edited collection that contains a mix of synthesis material and research specifics; I refer to some specific chapters as good resources in my Further Reading sections at the end of each chapter in this book.

# Audience

The primary audience of this book is students in a first vis course, particularly at the graduate level but also at the advanced undergraduate level. While admittedly written from a computer scientist’s point of view, the book aims to be accessible to a broad audience including students in geography, library science, and design. It does not assume any experience with programming, mathematics, human–computer interaction, cartography, or graphic design; for those who do have such a background, some of the terms that I define in this book are connected with the specialized vocabulary from these areas through notes in the margins. Other audiences are people from other fields with an interest in vis, who would like to understand the principles and design choices of this field, and practitioners in the field who might use it as a reference for a more formal analysis and improvements of production vis applications.

I wrote this book for people with an interest in the design and analysis of vis idioms and systems. That is, this book is aimed

at vis designers, both nascent and experienced. This book is not directly aimed at vis end users, although they may well find some of this material informative.

The book is aimed at both those who take a problem-driven approach and those who take a technique-driven approach. Its focus is on broad synthesis of the general underpinnings of vis in terms of principles and design choices to provide a framework for the design and analysis of techniques, rather than the algorithms to instantiate those techniques.

The book features a unified approach encompassing information visualization techniques for abstract data, scientific visualization techniques for spatial data, and visual analytics techniques for interleaving data transformation and analysis with interactive visual exploration.

# Who’s Who

I use pronouns in a deliberate way in this book, to indicate roles. I am the author of this book. I cover many ideas that have a long and rich history in the field, but I also advocate opinions that are not necessarily shared by all visualization researchers and practitioners. The pronoun you means the reader of this book; I address you as if you’re designing or analyzing a visualization system. The pronoun they refers to the intended users, the target audience for whom a visualization system is designed. The pronoun we refers to all humans, especially in terms of our shared perceptual and cognitive responses.

I’ll also use the abbreviation vis throughout this book, since visualization is quite a mouthful!

# Structure: What’s in This Book

The book begins with a definition of vis and walks through its many implications in Chapter 1, which ends with a high-level introduction to an analysis framework of breaking down vis design according what–why–how questions that have data–task–idiom answers. Chapter 2 addresses the what question with answers about data abstractions, and Chapter 3 addresses the why question with task abstractions, including an extensive discussion of deriving new data, a preview of the framework of design choices for how idioms can be designed, and several examples of analysis through this framework.

Chapter 4 extends the analysis framework to two additional levels: the domain situation level on top and the algorithm level on the bottom, with the what/why level of data and task abstraction and the how level of visual encoding and interaction idiom design in between the two. This chapter encourages using methods to validate your design in a way that matches up with these four levels.

Chapter 5 covers the principles of marks and channels for encoding information. Chapter 6 presents eight rules of thumb for design.

The core of the book is the framework for analyzing how vis idioms can be constructed out of design choices. Three chapters cover choices of how to visually encode data by arranging space: Chapter 7 for tables, Chapter 8 for spatial data, and Chapter 9 for networks. Chapter 10 continues with the choices for mapping color and other channels in visual encoding. Chapter 11 discusses ways to manipulate and change a view. Chapter 12 covers ways to facet data between multiple views. Choices for how to reduce the amount of data shown in each view are covered in Chapter 13, and Chapter 14 covers embedding information about a focus set within the context of overview data. Chapter 15 wraps up the book with six case studies that are analyzed in detail with the full framework.

Each design choice is illustrated with concrete examples of specific idioms that use it. Each example is analyzed by decomposing its design with respect to the design choices that have been presented so far, so these analyses become more extensive as the chapters progress; each ends with a table summarizing the analysis. The book’s intent is to get you familiar with analyzing existing idioms as a springboard for designing new ones.

I chose the particular set of concrete examples in this book as evocative illustrations of the space of vis idioms and my way to approach vis analysis. Although this set of examples does cover many of the more popular idioms, it is certainly not intended to be a complete enumeration of all useful idioms; there are many more that have been proposed that aren’t in here. These examples also aren’t intended to be a historical record of who first proposed which ideas: I often pick more recent examples rather than the very first use of a particular idiom.

All of the chapters start with a short section called The Big Picture that summarizes their contents, to help you quickly determine whether a chapter covers material that you care about. They all end with a Further Reading section that points you to more information about their topics. Throughout the book are boxes in the margins: vocabulary notes in purple starting with a star, and

cross-reference notes in blue starting with a triangle. Terms are highlighted in purple where they are defined for the first time.

The book has an accompanying web page at http://www.cs.ubc. ca/~tmm/vadbook with errata, pointers to courses that use the book in different ways, example lecture slides covering the material, and downloadable versions of the diagram figures.

# What’s Not in This Book

This book focuses on the abstraction and idiom levels of design and doesn’t cover the domain situation level or the algorithm levels.

I have left out algorithms for reasons of space and time, not of interest. The book would need to be much longer if it covered algorithms at any reasonable depth; the middle two levels provide more than enough material for a single volume of readable size. Also, many good resources already exist to learn about algorithms, including original papers and some of the previous books discussed above. Some points of entry for this level are covered in Further Reading sections at the end of each chapter. Moreover, this book is intended to be accessible to people without a computer science background, a decision that precludes algorithmic detail. A final consideration is that the state of the art in algorithms changes quickly; this book aims to provide a framework for thinking about design that will age more gracefully. The book includes many concrete examples of previous vis tools to illustrate points in the design space of possible idioms, not as the final answer for the very latest and greatest way to solve a particular design problem.

The domain situation level is not as well studied in the vis literature as the algorithm level, but there are many relevant resources from other literatures including human–computer interaction. Some points of entry for this level are also covered in Further Reading.

