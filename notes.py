# script for random data generation for ContactUs DB:
#
#     In[1]:
#     import random, string
#
#     In[2]:
#     from faker import Faker
#
#     In[3]: fake = Faker()
#
#     In[4]: chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
#
#     In[5]:
#     for _ in range(50):
#         ...: random_string = "".join(random.choice(chars) for _ in range(random.randint(5, 10)))
#         ...: random_subject = "".join(random.choice(chars) for _ in range(random.randint(20, 45)))
#         ...: random_message = "".join(random.choice(chars) for _ in range(random.randint(30, 100)))
#         ...: ContactUs(email_from=f"{fake.name().split()[0]}_{random_string}@gmail.com", subject=random_subject, message = random_message).save()


# script for random data generation for Rate DB:
#
# In [1]: import random
#
# In [2]: from currency.models import Rate
#
# In [3]: for _ in range(20):
#    ...:     Rate(type=random.choice(['USD', 'EUR']), source=random.choice(['PrivatBank', 'MonoBank']), buy=random.randint(25,40), sell=random.randint(27,45)).save()
