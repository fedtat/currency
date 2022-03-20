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
