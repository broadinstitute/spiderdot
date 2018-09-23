# spiderdot
accessing isilon information for data curation
simple script to test connection by looking for a directory

code needs to be updated in the following areas:
  * location of the configuration file - update configuraiton file with server and user information
  * configuration that is to be used
  * path to test with

Notes:
To get this working, I discovered that a number of parameters were required.  Parameters were identified when errors occured during the testing of the script.  
Made guesses (some were trial and error) at what the values were to be.  Some I found by searching the web.  

Currently getting a permission denied at the root level, which is a good sign.
The code is connecting - my user account needs permissions to the parent directory for the cluster.
