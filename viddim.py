from __future__ import generator_stop
import re
import argparse
import os
import subprocess
import shutil
import random

# print(cv2.__version__)

def sort_nicely( l ):
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )
	return l

def parse_args():
	desc = "make dance music with images" 
	parser = argparse.ArgumentParser(description=desc)

	parser.add_argument('-f','--framerate', type=int,
		default=24,
		help='video framerate (default: %(default)s)')

	parser.add_argument('-i','--input_folder', type=str,
		default='./input/',
		help='Directory path to the inputs folder. (default: %(default)s)')

	parser.add_argument('-p','--playlist', type=str,
		default=None,
		help='Directory path to a file containing a playlist. (default: %(default)s)')

	parser.add_argument('-o','--output_folder', type=str,
		default='./output/',
		help='Directory path to the outputs folder. (default: %(default)s)')

	parser.add_argument('-r','--riddims', type=str,
		default=None,
		help='Directory path to a file containing viddims. (default: %(default)s)')

	parser.add_argument('--random', dest='random', action='store_true')


	args = parser.parse_args()
	return args

def make_video(output_folder,folder_path,framerate):
	cmd=f'ffmpeg -y -r {framerate} -i "{folder_path}/%09d.png" -vcodec libx264 -pix_fmt yuv420p "{output_folder}/riddim.mp4"'
	subprocess.call(cmd, shell=True)

def viddim_files(riddims, playlist, files):

	frame_folder = os.path.join(args.output_folder,'frames')
	if not os.path.exists(frame_folder):
		os.makedirs(frame_folder)
	

	count = 0
	if (args.random):
		fcount = random.randint(0, len(files))
	else:
		fcount = 0
	# for filename in files:
	# 	print(filename)

	# 	file_path = os.path.join(args.input_folder, filename)

	# 	new_path = os.path.join(args.output_folder, str(count).zfill(9)+'.png')
	# 	shutil.copy2(file_path,new_path)

	# 	count+=1

	print(len(playlist))

	for p in playlist:
		
		if fcount > len(files)-1: 
			print('out of film')
			break
		
		if (p.startswith("goto")):
			goto = p.split(":")[-1]
			# print(goto)
			if goto.startswith("+") or goto.startswith("-"):
				fcount = fcount + int(goto)
			else:
				fcount = int(goto)
		else:
			riddim = next(item for item in riddims if (item["name"] == p) )
		
			print(fcount)
			if(type(riddim['beat']) is int):
				file_path = os.path.join(args.input_folder, files[fcount])
				for b in range(riddim['beat']):
					new_path = os.path.join(frame_folder, str(count).zfill(9)+'.png')
					shutil.copy2(file_path,new_path)
					count+=1

				if (args.random):
					fcount = random.randint(0, len(files))
				else:
					fcount+=1

			else:
				for bcount,el in enumerate(riddim['beat']):
					# print(el)
					if fcount > len(files)-1: 
						print('out of film')
						break
					# print(el)
					# print(files[fcount])
					file_path = os.path.join(args.input_folder, files[fcount])

					for b in range(el):
						new_path = os.path.join(frame_folder, str(count).zfill(9)+'.png')
						shutil.copy2(file_path,new_path)
						count+=1

					if (args.random):
						fcount = random.randint(0, len(files))
					else:
						fcount+=1


	print('out of beats')
	make_video(args.output_folder,frame_folder, args.framerate)
	print(f'frames used: {fcount}')

	# for filename in files:
	# 	print(filename)

	# 	file_path = os.path.join(args.input_folder, filename)

	# 	# for p in playlist:
	# 	# 	print(playlist[p])

	# 	print(playlist)

	# 	# new_path = os.path.join(args.output_folder, str(count).zfill(9)+'.png')
	# 	# shutil.copy2(file_path,new_path)

	# 	count+=1

def main():
	global args
	args = parse_args()
	os.environ['OPENCV_IO_ENABLE_JASPER']= "true"
	print('processing images...')

	if not os.path.exists(args.output_folder):
		os.makedirs(args.output_folder)

	files = [ f for f in os.listdir(args.input_folder) if (not f.startswith('.') and os.path.isfile(os.path.join(args.input_folder, f))) ]
	# files = [ f for f in os.listdir(args.input_folder) if os.path.isfile(os.path.join(args.input_folder, f))]
	files = sort_nicely(files)

	if(args.riddims):
		riddims = []
		with open(args.riddims) as file:
		    for line in file:
		    	parts = line.strip().split(':')
		    	beats = parts[1].strip().split(',')
		    	riddims.append({ "name": str(parts[0].strip()), "beat": tuple(int(b) for b in beats) })
		#print(riddims)
	else:
		# some default riddims to use
		riddims = [
			{ "name": "hold3", "beat": (72) },
			{ "name": "hold2", "beat": (48) },
			{ "name": "hold", "beat": (24) },
			{ "name": "four_24", "beat": (4,4,4,4,4,4) },
			{ "name": "second_holdend", "beat": (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,36) },
			{ "name": "one_24", "beat": (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1) },
		]

	if(args.playlist):
		playlist = []
		with open(args.playlist) as file:
		    for line in file:
		    	for el in line.strip().split(','):
		    		playlist.append(str(el.strip()))
		print(playlist)
	else:
		playlist = [
			"one_24","one_24","four_24","four_24",
			"one_24","one_24","four_24","four_24",
			"hold","hold","four_24","four_24","four_24","one_24","one_24","hold",
			"one_24","one_24","one_24","one_24","four_24","four_24",
			"four_24","four_24","hold","hold","hold","hold","one_24","one_24","four_24","four_24",
			"one_24","one_24","hold2","one_24","one_24","hold", # lpips,interpolation,lpips,truncation
			"one_24","one_24","one_24","one_24","hold",
			"four_24","one_24","one_24","one_24","one_24",
		]

	viddim_files(riddims, playlist, files)





if __name__ == "__main__":
	main()
