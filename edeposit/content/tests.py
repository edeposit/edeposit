# Integration tests for Library
ztc.ZopeDocFileSuite(
    'Library.txt',
    package='edeposit.content',
    optionflags = OPTION_FLAGS,
    test_class=TestCase)

