import os
from os.path import join, getsize
	
def main():
	for root, dirs, files in os.walk('.'):
		for f in [os.path.join(root,q) for q in files if q.endswith(".cc")]:
			inlines = [l.rstrip() for l in open(f,"r")]
			output =[]
			specialnext = False
			mode = 0
			#print "opened",f,len(inlines)
			for l in inlines:
				if l == "TF_CALL_double(REGISTER_CPU_KERNELS);":
					print f,"found",l
					specialnext = True
					mode = 0
					output.append(l)
				elif l == "REGISTER_KERNELS_CPU(double);":
					print f,"found",l
					specialnext = True
					mode = 1
					output.append(l)					
				elif l == "TF_CALL_double(HANDLE_TYPE_NAME_CPU);":
					print f,"found",l
					specialnext = True
					mode = 2
					output.append(l)	
				elif l.find("TF_CALL_double") == 0 and l.find("CPU") > 0:
					print f,"found",l
					specialnext = True
					mode = 3
					output.append(l)														
				else:
					if specialnext:
						specialnext = False
						if mode == 0:
							if l.find("TF_CALL_posit") < 0:
								output.append("TF_CALL_posit(REGISTER_CPU_KERNELS);")
							else:
								print "existent mode 0"
						elif mode == 1:
							if l != "REGISTER_KERNELS_CPU(posit);":
								output.append("REGISTER_KERNELS_CPU(posit);")
							else:
								print "existent mode 1"
						elif mode == 2:
							if l != "TF_CALL_posit(HANDLE_TYPE_NAME_CPU);":
								output.append("TF_CALL_posit(HANDLE_TYPE_NAME_CPU);")
							else:
								print "existent mode 2"
						elif mode == 3:
							if l.find("posit") < 0:
								output.append(last.replace("double","posit"))
							else:
								print "existent mode 3"

					output.append(l)
				last = l
			if len(output) > len(inlines):
				print "\tdone ",len(output)-len(inlines)
				o = open(f,"w")
				o.write("\n".join(output))
				o.close()

if __name__ == '__main__':
	main()