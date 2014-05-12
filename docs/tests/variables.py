import os,binascii
TEST_SEED=binascii.b2a_hex(os.urandom(15))[:5]
