# Integration tests for edeposit.content.ebook
ztc.ZopeDocFileSuite(
    'edeposit.content.epublication.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase),

# -*- extra stuff goes here -*-

        # Integration tests for AuthorFolder
        ztc.ZopeDocFileSuite(
            'AuthorFolder.txt',
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

