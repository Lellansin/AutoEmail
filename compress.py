import zipfile

class Zip(zipfile.ZipFile):
	"""docstring for Zip"""
	def __init__(self, zip_name='archive.zip'):
		super(Zip, self).__init__(zip_name, 'w', zipfile.ZIP_DEFLATED)
		self.files = []

	def __del__(self):
		self.close()

	def setFiles(self, files):
		self.files = files

	def addFile(self, file):
		self.file.push(file)

	def zip(self):
		for item in self.files:
			try:
				self.write(item)
			except Exception, e:
				raise e

def test():
	test = Zip()
	test.setFiles(['pic/(1).png', 'pic/(2).png', 'pic/(3).png'])
	test.zip()
	print 'ok'

if __name__ == '__main__':
	test()