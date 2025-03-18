## WORK IN PROGRESS ##

This is where we can add details of the app. It might be an idea to share what our current vision of what the app will be, as though we were describing it to Eleni, or Samia etc.


### PyCharm (MacOS) Setup Guide

#### Prerequisites
1.	Install Homebrew (if not already installed):  
    a. Open Terminal and run:  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    b. Then follow the onscreen instructions 

2.	Install Python 3.9 (in terminal):  
    a. brew install python@3.9
    b. Verify installation (in terminal):  python --version   
   
####  Clone the Repository
1.	Install GitHub Desktop (optional):  
    a. Download from https://desktop.github.com, sign in, and clone the group-10-software repository.  
   OR 
1.	use Terminal 
    a. git clone https://github.com/jbr-hill44/group-10-software.git
2.	Open Project in PyCharm:  
   a. Launch PyCharm CE.  
   b.	Go to File > Open and select the cloned group-10-software folder.

#### Configure Python Interpreter
1.	Set Up Virtual Environment:  
    a. In PyCharm, go to PyCharm > Settings > add Python Interpreter.  
      i. Set location to .venv (in your project folder).  
      ii. Ensure the base interpreter points to Python 3.9 (likely at /opt/homebrew/bin/python3.9).  
      iii. Click OK.

2.	Install Dependencies:  
    a.	Open the Terminal in PyCharm and run:  .venv/bin/pip3 install -r requirments.txt


####  Run the App
  1.	Using PyCharm Terminal:  
      a. source .venv/bin/activate 
      b. streamlit run match_navigation.py
