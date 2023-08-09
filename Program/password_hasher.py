#importing the modules
import math #for jumbled initial hashing
import random, string #random for access code generation, string for valid ASCII list for hash

#class that can be imported for password hashing
class PasswordHasher():
    def __init__(self):
        #creates the list of character ASCIIs that will be used in the hash
        self.ascii_list = list(map(ord, string.ascii_letters + string.digits))

    #function to set hash initially
    def set_hash(self, pswd):
        #initialises some variables
        self.ascii_str = ""
        self.a_list = []
        hash = ""

        #even if the password is blank, it is given the default value of EOL
        if pswd == '':
            pswd = '\n'

        #initialises a global list with ASCII value of each letter in password
        self.pswd_list = [ord(pswd[i]) for i in range(len(pswd))]

        #the first hashing
        for i in range(len(self.pswd_list)):
            #uses the math module to change every ASCII value of the password to a conjugate number 
            self.pswd_list[i] = math.ceil(round(math.pow(round(math.log(round(self.pswd_list[i]*math.pi, 2), abs(round(math.tan(i+1), 2))), 2), 2), 2)*100)
            self.ascii_str += str(self.pswd_list[i]) #using the loop creates a string of digits

        #decoding the jumbled number string (self.ascii_str)
        for x in range(len(self.ascii_str)):
            #creates a list of numbers close to valid ASCIIs from the string
            if self.ascii_str[x] == '1' and x <= (len(self.ascii_str)-3):
                self.a_list.append(int(self.ascii_str[x: x+3]))
            else:
                self.a_list.append(int(self.ascii_str[x: x+2]))

        #the second hashing
        for x in self.a_list:
            if x in self.ascii_list:
                hash += chr(x)
            else:
                x += 48
                if x in self.ascii_list:
                    hash += chr(x)

        return hash #a hashed string of varying length is returned

    def get_hash(self, pswd, check=0):
        #initialising some variables and constants
        self.check = check #access code (deafult: random), else provided by user to match password
        hash = self.set_hash(pswd) #gets the hash of password provided
        salt = self.set_hash(hash) #gets the hash of the password hash (mimics salting)
        final = salt + hash #a more random hash string after plain salting
        store = "" #temporary storage variable
        leftout = "" #fixed hash size setting helper variable
        count = 0 #while loop counter
        rand = random.randint(2, 10) #generates random access code for initial hashing (2-10)
        HASH_LEN = 64 #fixed length of hash

        #if no access code provided by user, access code replaced by that random code
        if not self.check:
            self.check = rand

        #if hash length gets more than HASH_LEN
        while len(final) > HASH_LEN:
            count += 1
            for i in range(0, len(final), self.check): #access code is used as loop skipping variable
                store += final[i] #shortens the hash by skipping
                try:
                    if count == 1:
                        leftout += final[i+1] #collects some discarded part of the hash while shortening
                except:
                    pass
            
            #hash is updated and 'store' variable is reset to ''
            final = store
            store = ''

        #if hash length gets less than HASH_LEN
        while len(final) < HASH_LEN:
            final += self.set_hash(leftout)[:HASH_LEN-len(final)] #adds the required padding using 'leftout'
            leftout = self.set_hash(leftout) #if length of 'leftout' is less than required then its hash is used instead

        #returns the final hash alongwith the embedded access code
        return f"${self.check}${final}"