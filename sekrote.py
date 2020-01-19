
import sys
import os
from enum import Enum
from cryptography.fernet import Fernet

key = bytes( str( open('./key','rb').readline() )[2:-1], 'utf-8')

class Command(Enum):
	OPEN = 1
	HELP = 2
	UNKNOWN = 3

crypto = Fernet(key)

def getCommand( com ):
	if com.upper() == "OPEN":
		return Command.OPEN
	elif com.upper() == "HELP":
		return Command.HELP
	else:
		return Command.UNKNOWN

def filepath():
	return './notes/';

def fileForDate( date, encrypted ):
	suffix = '_decrypt';
	if encrypted:
		suffix = '_encrypt'
	return filepath() + date + suffix + '.sekrote'

def decryptedFileForDate( date ):
	return fileForDate( date, False )

def encryptedFileForDate( date ):
	return fileForDate( date, True )

def encrypt( text ):
	bytes_encoding = text.encode('utf-8')
	text = crypto.encrypt( bytes_encoding )
	return text

def decrypt( text ):
	if text == "":
		return text
	text = bytes(text[2:-1], 'utf-8')
	text = crypto.decrypt( text ).decode('utf-8')
	return text

def deleteFile( file ):
	os.system( "rm " + file )

def fileExists( file ):
	return os.path.exists(file)

def prepareFileForDate( date ):
	# read the encrypted file and decrypt it
	print('Reading file for date ' + str(date))
	encryptedFileName = encryptedFileForDate( date )
	encryptedText = ""
	if( fileExists( encryptedFileName ) ):
		encryptedF = open( encryptedFileName, 'r' )
		for line in encryptedF.readlines():
			encryptedText += line + "\n";
		encryptedText = encryptedText[:-1]

	decryptedText = decrypt( encryptedText )
	decryptedFileName = decryptedFileForDate( date )
	decryptedF = open( decryptedFileName, 'w' )
	decryptedF.write( str( decryptedText ) )
	decryptedF.close()

def endForDate( date ):
	# encrypt the file back and delete the decrypted file
	print('Writing file for date ' + str(date))
	decryptedFileName = decryptedFileForDate( date )
	decryptedF = open( decryptedFileName, 'r' )
	decryptedText = ""
	for line in decryptedF.readlines():
		decryptedText += line
	encryptedText = encrypt( decryptedText )

	encryptedFileName = encryptedFileForDate( date )
	encryptedF = open( encryptedFileName, 'w' )
	encryptedF.write( str( encryptedText ) )
	encryptedF.close()

	deleteFile( decryptedFileName )

def editFile( date ):
	# open the decrypted file in sublime
	decryptedFileName = decryptedFileForDate( date )
	os.system( str.format("subl -w " + decryptedFileName) )

def open_(date):
	prepareFileForDate(date)
	editFile(date)
	endForDate(date)

def help():
	print('\n');
	print('***************************** HELP *****************************')
	print('python sekrote.py open\tOpen the note for a given date!')
	print('python sekrote.py help\tShow this help')

def start():
	print('*'*50)
	print('THE AWESOME SECRET NOTE!')
	print('*'*50)

	command = getCommand( str(sys.argv[1]) )
	if command == Command.UNKNOWN:
		help()
		exit(0)

	if command == Command.OPEN:
		date = str( sys.argv[2] )
		open_(date)
	elif command == Command.HELP:
		help()
		exit(0)
	else:
		print('What is this mysterious command?')
		exit(1)


def main():
	start();

if __name__ == "__main__":
	main()