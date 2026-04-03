# DESIGNING FOR THE DESKTOP

Most modern desktop interfaces derive their appearance from the Xerox Alto, an experimental computer system developed in 1973 at Xerox's Palo Alto Research Center (PARC), now PARC, Inc. PARC's Alto was the first computer with a graphical interface and was designed to explore the potential of computers as desktop business systems. In creating the Alto, PARC researchers developed what became the four pillars of the desktop UI paradigm: windows, icons, menus (and other widgets), and pointer, or WIMP for short.

The Alto was designed as a networked office system in which documents could be composed, edited, and viewed in WYSIWYG (what you see is what you get) form; stored; retrieved; transferred electronically between workstations; and printed. The Alto system, and its commercially unsuccessful progeny, the Xerox Star, contributed many significant innovations to the vernacular of desktop computing that we now regard as commonplace: the mouse, the rectangular window, the scrollbar, the (virtual) pushbutton, the "desktop metaphor," object-oriented programming, multitasking, Ethernet, and laser printing.

PARC's effect on the industry and contemporary computing was profound. Both Steve Jobs and Bill Gates saw the Alto at PARC in the late 1970s and were indelibly impressed.

After hiring away many of PARC's most brilliant minds—who jumped ship after it was clear that Xerox was about to fumble the entire future of computing—Steve Jobs set about reincarnating the Alto/Star in the form of the Lisa. The Lisa was remarkable, accessible, exciting, far too expensive ($9,995 in 1983), and frustratingly slow. It also introduced new graphical idioms, such as drop-down menus, to the new visual language of computing.

About this time, less visually polished desktop interfaces also began to appear on expensive and more powerful UNIX workstations from companies like Sun Microsystems, which fared somewhat better with hardcore scientific and engineering audiences. Not deterred by the commercial failure of the Lisa, Jobs began a secret project to develop an affordable incarnation of the Alto.

The result was the legendary Macintosh, a machine that has had enormous influence on our technology, design, and culture. The Mac single-handedly brought an awareness of design and aesthetics to the industry. It not only raised the standards for user-friendliness, but it also enfranchised a whole population of skilled individuals from disparate fields who were previously locked out of computing because of the industry's self-absorption in techno-trivia. Microsoft, after creating some of the first software for the Mac, went on to develop its own WIMP interface for PCs—Windows—between them defining our personal computing paradigms for over two decades.

This chapter covers detailed design considerations for modern desktop GUIs of all flavors. It focuses on the behaviors of windows and their structural and navigational components, as well as pointer-driven selection and manipulation of onscreen objects.

# Anatomy of a Desktop App

As you may remember from our earlier discussion of software posture (see Chapter 9), the two primary types of desktop interfaces are sovereign and transient. By far, the majority of actual work that gets done on desktop applications is done in sovereign applications. Transients exist in supporting roles for brief, intermittent, or largely background tasks (such as music playback or instant messaging). Consequently, this section focuses on the basic structural patterns of sovereign desktop apps, the building blocks of which we'll discuss later in this chapter, as well as in Chapter 21.

# Primary and secondary windows

The top-level structure of desktop applications (as opposed to the operating system itself) is the window—the movable, resizeable container within which both content and functional controls for the app primarily reside. In terms of structuring your application, you can think of it as having a primary window and, in many cases, one or more secondary windows.

# Primary window

The primary window contains your application's content, typically expressed in the form of documents that can be created, edited, and shared. Less frequently, it contains other

sorts of objects with properties that can be manipulated and configured, or media that can be viewed or played. Primary windows often are divided into panes that contain content, a means of navigating between different content objects, and sets of frequently used functions for manipulating or controlling the content. Primary windows typically are designed to assume sovereign posture, filling most of the screen and supporting full-screen modes.

# Secondary windows

Secondary windows support the primary window, providing access to less frequently used properties and functions, typically in the form of dialogs. We'll discuss dialogs and their structure at length in Chapter 21. If your application allows panes located in the primary window to be detached and manipulated separately, these floating panels or palettes also take on a role as secondary windows.

# Primary window structure

Primary windows, as mentioned, frequently are subdivided into multiple functional areas:

A content or work area   
A menu bar   
- Multiple toolbars, panels, or palettes that help you navigate to or select content objects or operate on selected content objects within the work area

# Menu and toolbars

Menu and toolbars are collections of related actions the user can instruct the application to perform, such as "close this document" or "invert the colors of the current selection." Menus are accessed by clicking on words arranged near the top of the screen, and are often subject to standardization rules from the operating system. Toolbars are more specific to the application, often summoned or dismissed through menus, and—once active—present their functions as a collection of visual icons, often with small labels.

When function menus are included within the primary window, they appear across the top of the window within a menu bar. Traditional toolbars appear directly below the menu bar (or, in OS X, across the top of the window). Newer UI idioms such as Microsoft's ribbon seek to take the place of both menus and toolbars, replacing them with a tabbed toolbar-like construct. It is more verbose than a toolbar and therefore shares some of the pedagogic features of menus. We discuss menus, toolbars, and related UI idioms in detail later in this chapter.

# Content panes

Content panes form the primary work area within most desktop applications, whether it is the editable view of a form or document or (as in the case of a software music synthesizer, for example) a complex control panel. An application typically has one primary content area. But applications that support editing multiple documents or views of a document (such as in CAD software) side-by-side may have multiple content panes. These panes may affect each other or allow dragging and dropping of objects between them.

