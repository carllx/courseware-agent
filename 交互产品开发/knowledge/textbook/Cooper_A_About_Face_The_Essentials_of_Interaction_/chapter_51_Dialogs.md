# Dialogs

Dialogs are pop-up windows superimposed over the application's main window. A dialog engages users in a conversation by offering information and requesting some input. When the user has finished viewing the information or selection from options presented, he can dismiss or accept the dialog. The dialog then disappears, returning the user to the main application window.

DESIGN PRINCIPLE

Put primary interactions in the primary window.

In the modern era of modeless toolbar and ribbon controls, a hallmark of poor interaction design is a user interface that consists primarily of control-laden modal dialogs. It is very difficult to create fluid interactions if you force users through a maze of pop-up dialogs. If a user is the chef, and the application is the kitchen, a dialog is the pantry. The pantry plays a secondary role, as should dialogs. They are supporting actors rather than lead players, and although they may move the action forward, they should not be the engines of motion. Primary actions and controls for an application belong in its main screen or window.

# Appropriate use of dialogs

It's sometimes useful to take users out of their flow to force them to focus on particular questions. Dialogs are appropriate for functions or features that are out of the normal course of things: Anything that is confusing, dangerous, or rarely used can be usefully placed in a dialog. This is particularly true for actions that make immediate and major changes to the application state. Such changes can be jarring, and should be cordoned off from users who are unfamiliar with them. For example, a function that allows wholesale reformatting of a document should be considered a dislocating action. The dialog helps prevent this feature from being invoked accidentally by ensuring that a big, friendly Cancel button is always present, and also by providing the space to show more protective and explanatory information along with the risky controls. The dialog can graphically show users the function's potential effects with a thumbnail of what the changes will look like. And of course, a robust Undo function (see Chapter 15) should be provided for such actions.

Dialogs are also well suited for concentrating information related to a single subject, such as the properties of a domain object—an invoice or customer, for example. They also can gather all information relevant to a function performed by an application, such as printing reports. This has obvious benefits to users: With all the information and controls related to a given subject in a single place, users don't have to search around the interface as much for a given function, and navigation excise is reduced.

