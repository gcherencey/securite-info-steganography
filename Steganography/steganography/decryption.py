#!/usr/bin/env python

'''
Created on Jan 21, 2013

Executable module for decryption data into a image

@author: Cherencey Gaylord
'''

from Crypto.Cipher import AES
from optparse import OptionParser
import Image
import logging
import os

def main(args=None):
    '''Main method which get nom_fichier_image nom_fichier_message key_AES as arguments'''
    
    response = defineParser(args)
    
    if os.path.exists(response[0]):
        
        if len(response[1]) % 16 == 0:
            
            print("Started ...")
            
            encryptor = AES.new(response[1], AES.MODE_ECB)
            
            logging.info("Decryption message with key " + response[1] + "from image" + response[0])
            clearMessage = encryptor.decrypt(getMessageFromImage(response[0]))
            
            logging.info("Done")
            print("Done")
    
            print(clearMessage)
            
        else:
            
            logging.error("The key must be 16 characters long")
        
    else:
        logging.error("This file doesn't exist")

def getMessageFromImage(nameImage):
    '''Method which extract and print the message from the picture'''
    
    messageSizeString = ""
    
    messageInBinary = ""  
    messageCrypted = ""
    
    image = Image.open(nameImage)
    image.load()
    
    redPart, greenPart, bluePart = image.split()
    redPart = list(redPart.getdata())

    for bit in redPart[0:8]:  
        messageSizeString += str(bit%2)
        
    messageSizeInt = int("".join(messageSizeString), 2)
    
    for bit in redPart[8:8*(messageSizeInt+1)]:               
        messageInBinary += str(bit%2)
    
    messageInBinary = "".join(messageInBinary)
    
    for octet in range(0,messageSizeInt):
        caractere = messageInBinary[8*octet:8*octet+8]
        messageCrypted += chr(int(caractere,2))
    
    return messageCrypted
    

def defineParser(args):
    """Definition of the parser and the behavior following the options"""

    parser = OptionParser(usage="""Usage: %prog nom_fichier_image key_AES [options] : Use the -h option to get help""")

    parser.add_option("-v", "--verbose",
                      action = "store_const",
                      const = logging.INFO,
                      dest = "level",
                      help = "Print a message each time  a  module  is initialized")
    parser.add_option("-d", "--debug",
                      action = "store_const",
                      const = logging.DEBUG,
                      dest = "level",
                      help = "Print debug information")

    (options, args) = parser.parse_args(args)

    if len(args) == 0:
        parser.error("You have to put parameters")
    
    elif len(args) == 1:
        parser.error("Not enough arguments")
        
    elif len(args) > 2:
        parser.error("Too many arguments")

    logging.basicConfig(format = '%(asctime)s -> %(levelname)s : %(message)s',
                        level = options.level,
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

    logging.info("Argument passed %s", args)

    return args
   
##########################################
# permitted to make the module executable
    
if __name__ == '__main__':
    main()