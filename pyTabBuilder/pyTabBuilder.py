import taglib
from sys import argv
from pyechonest import config, song
import os, inspect

config.ECHO_NEST_API_KEY = """FNKMVYZLQUSB4XHGP"""
config.CODEGEN_BINARY_OVERRIDE = """{}/echoprint-codegen""".format(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))



def getTags(path):
	s = song.identify(path, codegen_start=20, codegen_duration=40)[0]
	return {
		u'TITLE': s.title,
		u'ARTIST': s.artist_name
	}




def buildTags(path):
	tags = getTags(path)
	s = taglib.File(path)
	for key in tags.iterkeys():
		s.tags[key] = [tags[key]]
	s.save()

def isMusicFile(filename):
	extensions = ['.mp3', '.ogg', '.wma', '.m4a']
	for extension in extensions:
		if filename.endswith(extension):
			return True
	return False



def main():
	if len(argv) != 2 or (not os.path.isdir(argv[1]) and not os.path.isfile(argv[1])):
		print "argument error"
		exit(1)
	if os.path.isdir(argv[1]):
		success = 0
		fail = 0
		count = 0
		for filename in os.listdir(argv[1]):
			count += 1
			if os.path.isfile(os.path.join(argv[1], filename)) and isMusicFile(filename):
				try:
					buildTags(os.path.join(argv[1], filename))
					success += 1
				except Exception as e:
					fail += 1
					# try:
					# 	print e
					# except Exception:
					# 	pass
			print """building tags, progress:{}%""".format(round(float(count) / float(len(os.listdir(argv[1]))) * 100.0, 1))
		print """Tag build completed! Success: {}  Fail: {}""".format(success, fail) 
	else:
		try:
			buildTags(argv[1])
		except Exception:
			print "Failed!"
			exit(1)

if __name__ == "__main__":
	main()