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

        # Integration tests for AMQPFolder
        ztc.ZopeDocFileSuite(
            'AMQPFolder.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for CatalogizationWorkPlansFolder
        ztc.ZopeDocFileSuite(
            'CatalogizationWorkPlansFolder.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for CatalogizationWorkPlan
        ztc.ZopeDocFileSuite(
            'CatalogizationWorkPlan.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ProducentUserPlansFolder
        ztc.ZopeDocFileSuite(
            'ProducentUserPlansFolder.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for ProducentUserPlan
        ztc.ZopeDocFileSuite(
            'ProducentUserPlan.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for E-Deposit:ProducentUserPlan
        ztc.ZopeDocFileSuite(
            'E-Deposit:ProducentUserPlan.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for AlephRecord
        ztc.ZopeDocFileSuite(
            'AlephRecord.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for OriginalFileContributingRequestsFolder
        ztc.ZopeDocFileSuite(
            'OriginalFileContributingRequestsFolder.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for OriginalFileContributingRequest
        ztc.ZopeDocFileSuite(
            'OriginalFileContributingRequest.txt',
            package='edeposit.content',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),



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

