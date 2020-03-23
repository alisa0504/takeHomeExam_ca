from fake_useragent import UserAgent
import random

ua = UserAgent()
user_agent_list = list()
for i in range(50):
    user_agent_list.append(ua.random)
print(user_agent_list[0])
