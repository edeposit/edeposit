# Integration tests for edeposit.content.ebook
ztc.ZopeDocFileSuite(
    'edeposit.content.epublication.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),

# Integration tests for ePublicationFolder
ztc.ZopeDocFileSuite(
    'ePublicationFolder.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),


# Integration tests for ePublication
ztc.ZopeDocFileSuite(
    'ePublication.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),

# -*- extra stuff goes here -*-

# Integration tests for ePeriodicalFolder
ztc.ZopeDocFileSuite(
    'ePeriodicalFolder.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),


# Integration tests for ISSN
ztc.ZopeDocFileSuite(
    'ISSN.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),


# Integration tests for ePeriodicalPart
ztc.ZopeDocFileSuite(
    'ePeriodicalPart.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),


# Integration tests for ePeriodical
ztc.ZopeDocFileSuite(
    'ePeriodical.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),


# Integration tests for BookFolder
ztc.ZopeDocFileSuite(
    'BookFolder.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),


# Integration tests for book
ztc.ZopeDocFileSuite(
    'Book.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),

