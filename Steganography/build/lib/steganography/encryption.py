#!/usr/bin/env python

'''
Created on Jan 21, 2013

@author: Cherencey Gaylord
'''

from optparse import OptionParser
import Image
import logging
import os
import re
from Crypto.Cipher import AES

FAILURE = 1
SUCCESS = 0

def main(args=None):
    
    response = defineParser(args)
    messageAES = ""
                     
    if os.path.exists(response[0]) and os.path.exists(response[1]):
        
        if len(response[2]) % 16 == 0:
            
            print("Started ...")
            logging.info("Extracting message from " + response[1])
            
            clearMessage = getMessageFromFile(response[1])
            
            if len(clearMessage) % 16 != 0:
                
                characterToAdd = 16 - len(clearMessage) % 16
                            
                for ajout in range(characterToAdd):
                    clearMessage = clearMessage + " "
            
            logging.info("Encryption message with AES with key " + response[2])
            encryptor = AES.new(response[2], AES.MODE_ECB)
            messageAES = encryptor.encrypt(clearMessage)
            
            logging.info("Hidding message into " + response[0])
            steganography(response[0], messageAES)
            
            logging.info("Done")
            print("Done")
            
        else:
            logging.error("The key must be 16 characters long")
        
    else:
        logging.error("This file doesn't exist")
        
def getMessageFromFile(nameFile):
    
    fichier = open(nameFile, "r")
    clearMessage = ""
        
    for line in fichier:
        clearMessage = clearMessage + line
            
    fichier.close()
    
    return clearMessage
        
def defineParser(args):
    """Definition of the parser and the behavior following the options"""

    parser = OptionParser(usage="""Usage: %prog nom_fichier_image nom_fichier_message key_AES (16 caracters long) [options] : Use the -h option to get help""")

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
    
    elif len(args) == 1 or len(args) == 2 :
        parser.error("Not enough arguments")
        
    elif len(args) > 3:
        parser.error("Too many arguments")

    logging.basicConfig(format = '%(asctime)s -> %(levelname)s : %(message)s',
                        level = options.level,
                        datefmt = '%m/%d/%Y %I:%M:%S %p')

    logging.info("Argument passed %s", args)

    return args

def isThisTypeOfFile(name):

    pattern_png = re.compile(".png$")
    pattern_bmp = re.compile(".bmp$")
    pattern_jpg = re.compile(".jpg$")
    pattern_jpeg = re.compile(".jpeg$")
    
    if pattern_bmp.search(name) or pattern_png.search(name) or pattern_jpg.search(name) or pattern_jpeg(name):
        return True

    else:
        return False

def steganography(nameImage, messageAES):
    
    if isThisTypeOfFile(nameImage):
        
        image = Image.open(nameImage)
        messageInAscii =""
        
        width, height = image.size
            
        image.load()
        redPart, greenPart, bluePart = image.split()
        redPart = list(redPart.getdata())
           
        messageSize = len(messageAES)
        lenMessageInBinary = bin(messageSize)[2:].rjust(8,"0")
        
        
        for bit in messageAES:
            messageInAscii += bin(ord(bit))[2:].rjust(8,"0")
            
        messageInAsciiJoin=''.join(messageInAscii)
            
        for iteration in range(8):
            redPart[iteration] = 2*int(redPart[iteration]/2) + int(lenMessageInBinary[iteration])
            
        for iteration in range(8*messageSize):
            redPart[iteration+8] = 2*int(redPart[iteration+8] // 2) + int(messageInAsciiJoin[iteration])        
                
        redPartWithMessage = Image.new("L",(width,height))
        redPartWithMessage.putdata(redPart)
            
        imgnew = Image.merge('RGB',(redPartWithMessage,greenPart,bluePart)) 
        
        logging.info("Picture with message is couverture.png")
        imgnew.save("couverture.png")
        
    else :
        logging.error("The file is not a valide image file")

if __name__ == '__main__':
    main()