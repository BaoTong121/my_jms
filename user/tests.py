from django.test import TestCase

# Create your tests here
import bcrypt


aa = bcrypt.hashpw('123.com'.encode(), bcrypt.gensalt()).decode()
print(aa)
print(bcrypt.checkpw('123.com'.encode(), aa.encode()))