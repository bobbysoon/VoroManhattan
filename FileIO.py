from os import makedirs, stat
from os.path import split,exists

def fileRead(fp):
	try:
		h=open(fp,'rt');text=h.read().strip();h.close();return text
	except: return None

def fileWrite(fp, text):
	dfp= split(fp)[0]
	if dfp and not exists(dfp): makedirs(dfp)
	h=open(fp,'wt')
	if h:
		h.write(text);h.close()
	else:
		raise ValueError('fileWrite failed')

def fileSize(fp):
	try:	return stat(fp).st_size
	except:	return None
