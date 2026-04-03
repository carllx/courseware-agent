# DESIGN PRINCIPLE

Reflect the interface for typical navigation.

Almost any point-and-shoot digital camera is a good example of inflection: The most commonly used function—taking a picture—is provided by a prominent hardware button that is easily accessible at a moment's notice. Less commonly used functions, such as adjusting the exposure, require interaction with menus or touchscreen controls.

# Commensurate effort

The most important principle in the proper inflection of interfaces is commensurate effort. Although it applies to all users, it is particularly pertinent to perpetual intermediates. This principle simply states that people will willingly work harder for something that is more valuable. That value, by the way, is in the eye of the user. It has nothing to do with how technically difficult a feature is to implement, but rather is entirely related to the users' goals.

If the user really wants something, he will work harder to get it. If he needs to format beautiful documents with multiple columns, several fonts, and fancy headings to impress his boss, he will be highly motivated to explore the application's recesses to learn how. That user will put commensurate effort into the project.

But if another user wants only to print plain documents in a single column and one font, no amount of inducement will get him to learn those more advanced formatting features. Providing him with those options is unwelcome noise.

DESIGN PRINCIPLE

Users make commensurate effort if the rewards justify it.

If you add features to your application that are complex to manage, users will be willing to tolerate that complexity only if the rewards are worth it. This is why a product's user interface can't be complex for achieving simple results, but it can be complex for achieving complex results (as long as such results aren't needed very often).

# Progressive disclosure

A particularly useful design pattern that exemplifies commensurate effort is progressive disclosure. In progressive disclosure, advanced or less frequently used controls are hidden in an expanding pane, which offers a small expand/hide toggle control to give the user access. This type of design is a boon to expert users, because the toggle is usually "sticky"; that is, once left open, it stays that way. It also gives intermediates an easy window into more advanced features but allows them to be stowed away neatly when not in use. Many of Adobe's Creative Suite tools make good use of progressive disclosure in their tool palettes, as shown in Figure 10-2.

![](images/a432e989c6fd6d08aa52386ff04b00ba1c29998cd9a8c25ed7317c16173cb427.jpg)  
Figure 10-2: Adobe Creative Suite applications all make similar use of progressive disclosure to tame the complexity of their tool palettes for intermediates. Experts can expand them and take advantage of the sticky expansion state, which is remembered across sessions.

# Organizing for inflection

In general, controls and displays should be organized in an interface according to three attributes: frequency of use, degree of dislocation, and degree of risk exposure.

- Frequency of use means how often the controls, functions, objects, or displays are used in typical daily patterns of use. Items and tools that are most frequently used (many times a day) should be immediately in reach. Less frequently used items, used perhaps once or twice a day, should be no more than a click or two away. Other items can be two or three clicks away. Rarely used facilities shouldn't be removed from the product if they provide real benefits to your personas, but they should be removed from the everyday work space.   
- Degree of dislocation refers to the amount of sudden change in an interface or in the document/information being processed by the application caused by the invocation of a specific function or command. Generally speaking, it's a good idea to put these types of functions deeper into the interface.

- Degree of risk exposure deals with functions that are irreversible or may have other dangerous ramifications. Missiles require two humans turning keys simultaneously on opposite sides of the room to arm them. As with dislocating functions, you want to make these types of functions more difficult for your users to stumble across. The greater the ramifications, the more care you should take in exposing the function.

As users get more experienced with more complex features, they will search for shortcuts, and you should provide them. This not only helps intermediates expand their reach over time, but it's also a necessity for expert users.

# Designing for Three Levels of Experience

In designing digital products, our goal should be neither to pander to beginners (since they don't stay beginners for long) nor to rush intermediates into expertise. Our approach should be threefold:

To rapidly and painlessly move beginners into intermediacy   
- To avoid putting obstacles in the way of intermediates who want to become experts   
- Most of all, to keep perpetual intermediates happy as they move around the middle of the skill spectrum

We need to spend more time making our products powerful and easy to use for perpetual intermediate users. We must accommodate beginners and experts too, but not to the discomfort of the largest segment of users. The remainder of this chapter describes some basic strategies for accomplishing this.

# What beginners need

Beginners are undeniably sensitive, and it is easy to demoralize a first-timer, but we must keep in mind that the state of beginnerhood is never an objective. Nobody wants to remain a beginner. It is merely a rite of passage everyone must experience. Good software shortens that passage without bringing attention to it.

As an interaction designer, it's best to imagine that users—especially beginners—are simultaneously very intelligent and very busy. They need some instruction, but not very much, and the process has to be rapid and targeted. If a ski instructor begins lecturing on snowpack composition and meteorology, he will lose his students, regardless of their aptitude for skiing. Just because a user needs to learn how to operate a product doesn't mean that he needs or wants to learn how it works inside.

On the other hand, intelligent people always learn better when they understand cause and effect, so you must help them understand why things work as they do. We use mental models to bridge the contradiction. If the interface's represented model closely follows the user's mental model (as discussed in Chapter 1), it will provide the understanding the user needs without forcing him or her to figure out the implementation model.

Certain kinds of products, especially those used in a transient manner (like most mobile apps), a distracted manner (Google Glass and other heads-up displays would qualify here), or those used by people with certain disabilities, must be optimized for beginners rather than intermediates. Examples include devices such as ATMs, informational kiosks designed for public spaces like museums, and consumer medical devices such as blood glucometers (used by patients with diabetes, who may have visual acuity problems and dexterity issues due to chronic numbness in their fingers).

# Getting beginners on board

A new user must grasp the product's concepts and scope quickly, or he will abandon it. Thus, the designer's first order of business is to ensure that the product adequately reflects the user's mental model of his tasks. He may not recall from use to use exactly which command is needed to act on a particular object, but he will definitely remember the relationships between objects and actions—the important concepts—if the interface's conceptual structure is consistent with his mental model.

Getting beginners to a state of intermediacy requires extra help from the application, but this extra help will get in their way as soon as they become intermediates. This means that whatever extra help you provide, it must not be fixed into the interface. It must know how to go away when its services are no longer required.

Standard online help is a poor tool for providing such beginner assistance. We'll talk more about help in Chapter 16, but its primary utility is as a reference, and beginners don't need reference information; they need overview information, such as a guided tour, or UI elements designed to help users get accustomed to new functions, but which cease to be presented after repeated successful use.

A separate guide facility—displayed within a dialog box—is a fine means for communicating overview, scope, and purpose. As the user begins to use the product, a dialog box can appear that states the product's basic goals and tools, naming the main features. As long as the guide stays focused on beginner issues, like scope and goals, and avoids

A perpetual intermediate and expert issues (discussed later), it should be adequate for assisting beginners.

Beginners also rely heavily on menus to learn and execute commands (see Chapter 18 for a detailed discussion about why this is true). Menus may be slow and clunky, but they are also thorough and verbose, so they offer reassurance. The dialog boxes that the menu items launch (if they do so at all) should also be tersely explanatory and come with convenient Cancel buttons.

# Beginners across platforms

We are often asked if the concept of perpetual intermediates applies to non-desktop products. Ultimately, we believe the same considerations we apply to desktop software should be used here. A well-designed interface, regardless of platform should help its users quickly become familiar and comfortable with navigation and functionality.

Something else is worth considering: Users of websites, mobile apps, and devices that are not a critical path for their workflow—or are subject to casual consumer use—may not be accessed frequently enough by users for them to readily memorize their organizational constructs. This increases the importance of making such interactions as transparent and discoverable as possible, as well as the need for temporary assistive UI elements or guided tours that help reinforce understanding for new users.

# What experts need

Experts (sometimes called influencers in marketing circles) are also a vital group, because their opinions have a disproportionate effect on purchasing. Experts of course listen to other experts, but they also exert an influence on other prospective customers, setting the tone for product reviews and discussions. This remains true even with the rise of online product ratings, though perhaps less so than before the likes of Amazon came into existence. Still, in many cases, when a beginner considers your product, he will trust the expert's opinion more than an intermediate's. This sometimes results in a disconnect: When an expert says, "It's not very good," she may really mean "It's not very good for experts like me." Beginners don't realize this, however, and will often take an expert's advice, even though it may not apply to their situational needs.

Experts might occasionally look for esoteric features, and they might make heavy use of a few of them. However, they will definitely demand faster access to their regular working set of tools, which may be quite large. In other words, experts want shortcuts to everything.

Anyone who uses a digital product for hours a day will very quickly internalize the nuances of its interface. It isn't so much that they want to cram frequently used commands

into their heads, as much as it is unavoidable. Their frequency of use both justifies and requires the memorization.

Expert users constantly and aggressively seek to learn more and to see more connections between their actions and the product's behavior and representation. Experts appreciate new, powerful features. Their mastery of the product insulates them from becoming disturbed by the added complexity. Experts also appreciate high information density relative to intermediate or beginning users.

For some specialized products, it is appropriate to optimize the user experience for experts. In particular, tools that technically minded people rely on for a significant portion of their professional responsibilities should be aimed at a high degree of proficiency. Development and creative authoring tools generally fall into this category, as do scientific instrumentation and (nonconsumer) medical devices. We expect the users of those products to already possess the necessary technical knowledge and to be willing to invest significant time and effort in mastering the application.

# What perpetual intermediates need

It's amazing to think that the majority of real users—intermediates—typically are ignored, but more often than not that is still the case. You can see this in many enterprise applications and digital products. The overall design biases them toward expert users. At the same time, cumbersome tools such as wizards or the likes of Clippy—the infamously annoying ("Would you like help?") "smart" assistant created by Microsoft for its Office suite of products in the 1990s—are grafted onto the product to meet marketing's perception of new users. Experts rarely use them, and beginners soon want to discard these embarrassing reminders of their ignorance. But the perpetual intermediate majority is perpetually stuck with them.

Instead, perpetual intermediates need fast access to the most common tools. They don't need scope and purpose explained to them, because they already know these things. ToolTips (see Chapter 20) are the perfect perpetual intermediate idiom. ToolTips say nothing about scope and purpose and meaning; they only state function in the briefest of idioms, consuming the least amount of video space in the process.

Perpetual intermediates know how to use reference materials. They are motivated to dig deeper and learn, as long as they don't have to tackle too much at once. This means that online help is a perpetual intermediate tool. They use it by way of the index, so that part of help must be comprehensive.

Perpetual intermediates establish the functions that they use with regularity and those that they use only rarely. The user may experiment with obscure features, but he will soon identify—probably subconsciously—his frequently used working set. The user will

demand that the tools in his working set be placed front and center in the user interface, where they are easy to find and remember.

Perpetual intermediates usually know that advanced features exist, even though they may not need them or know how to use them. But the knowledge that they are there is reassuring to the perpetual intermediate, convincing him that he made the right choice investing in this product. The average skier may find it inspirational to know that a scary, black-diamond, expert run is just beyond those trees, even if she never intends to use it. It gives her something to aspire to and dream about, and it gives her the sense that she's at a good ski resort.

Your product must likely provide for both absolute newbies and the many possible cases an expert might encounter. But don't let this business requirement influence your design thinking. Yes, you must provide those features for expert users. Yes, you must support those transient beginners. But in most cases, you need to apply the bulk of your talents, time, and resources to designing the best interaction possible for your most representative users: the perpetual intermediates. When digital products follow the principle of commensurate effort, the learning curve doesn't go away, but it disappears from the user's mind—which is just as good.

