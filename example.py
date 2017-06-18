# coding: utf-8


# Globus API Wrapper for Dummies
# ==========================================================
# Jorge D. Morales<br>
# 06/18/2017<br>
# 
# This is a minimally simplfied globus wrapper. 
# The idea is to simplify the usage for just moving data from a python script (or notebook). 
# 
# The guide assumes that you already have a GO account, and the **globusonline-transfer-api-client**. 
# At its core this wrapper is using the globus-api examples/tutorial with a few added wrappers, 
# if you read the GOdummy.py it will be easy to tell, as the name implies, this is just a simplified wrapper. 
# 
# 
# ## Prerequisites
# 
# 1. A [Globus Online](https://www.globus.org/app/account) account (just click and get one)
# 2. The [globus transfer-api-client](https://github.com/globusonline/transfer-api-client-python) (just install with pip as instructed in the link)
# 3. Access to two end points, at least one has to be a static endpoint, one of them can be a [personal endpoint](https://www.globus.org/globus-connect-personal).
# 
#
# ## Setup
# 
# 1. Just clone the repository (all you really need is the GOdummy.py wrapper, but some examples are provided)
#     ``` 
#             git clone https://github.com/georgemm01/GOdummy.git
#     ```
#     
# 2. Make sure that ```GOdummy.py``` is in your ```PYTHONPATH```, or in your working area, so that you can import it to your script
# 
#
# 3. You can run the example.py or example.ipynb 
#
#
#

# ## 1. Import the GO API Wrapper for Dummies
from GOdummy import *


# ## 2. Initialize your credentials and the API
# (replace batman with your GO username)
credential=GOinit(username='batman')


# ## 3. Define the source and destination endpoints and autoactivate them
# If your GO credential is alowed it will activate inactive endpoints, otherwise you will have to initialize them, either by clicking in the GO website, or by running the globus connect personal in your personal endpoint. 
ep1='slac#osg'
ep2="batman#c6c38046"

GOendpoints(ep1,ep2)


# ## 4. Initialize your transfer 
t=GOpreTransfer(epoint1=ep1,epoint2=ep2,timeout=10) #timeout in minutes


# ## 5. Add the items you want to transfer
# (you can add as many as you wish, if the transfer takes more than the timeout it will abort)
t.add_item("/batpath/to/batdirectory/batfile.batsuffix",
           "/home/batman/batfilecopy.batsuffix")


# ## 6. Execute the transfer
GOTransfer(t)

