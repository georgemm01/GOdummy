Globus API Wrapper for Dummies
===
Jorge D. Morales<br>
06/18/2017<br>

This is a minimally simplfied globus wrapper. The idea is to simplify the usage for just moving data from a python script (or notebook). 

The guide assumes that you already have a GO account, and the **globusonline-transfer-api-client**. 
At its core this wrapper is using the globus-api examples/tutorial with a few added wrappers, if you read the GOdummy.py it will be easy to tell, as the name implies, this is just a simplified wrapper. 


---
## Prerequisites

1. Python 2.6 or 2.7 (the globus API is not supporting 3.x)
2. A [Globus Online](https://www.globus.org/app/account) account (just click and get one)
3. The [globus transfer-api-client](https://github.com/globusonline/transfer-api-client-python) (just install with pip as instructed in the link)
4. Access to two end points, at least one has to be a static endpoint, one of them can be a [personal endpoint](https://www.globus.org/globus-connect-personal).

## Setup

1. Just clone the repository (all you really need is the GOdummy.py wrapper, but some examples are provided)
   ``` 
            git clone https://github.com/georgemm01/GOdummy.git
	    ```
    
2. Make sure that ```GOdummy.py``` is in your ```PYTHONPATH```, or in your working area, so that you can import it to your script

3. You can run the ```example.py``` or ```example.ipynb```

That's it! You should be good to GOdummy!


