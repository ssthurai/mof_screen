def get_nprocs(submit_script):
	"""
	Get the number of processors from submit script
	Args:
		submit_script (string): name of submission script

	Returns:
		nprocs (int): number of total processors

		ppn (int): number of processors per node
	"""

	#Setup for MOAB
	with open(submit_script,'r') as rf:
		for line in rf:
			if 'nodes' in line or 'ppn' in line:
				line = line.strip().replace(' ','')
				nodes = int(line.split('nodes=')[1].split(':ppn=')[0])
				ppn = int(line.split('nodes=')[1].split(':ppn=')[1])
	nprocs = nodes*ppn

	#Setup for NERSC (KNL)
	# with open(submit_script,'r') as rf:
	# 	for line in rf:
	# 		if 'SBATCH -N' in line:
	# 			nodes = int(line.split('-N ')[1])
	# ppn = 64
	# nprocs = nodes*ppn

	#Setup for NERSC (SKX)
	# with open(submit_script,'r') as rf:
	# 	for line in rf:
	# 		if 'SBATCH -N' in line:
	# 			nodes = int(line.split('-N ')[1])
	# ppn = 32
	# nprocs = nodes*ppn

	#Setup for Stampede2
	# with open(submit_script,'r') as rf:
	# 	for line in rf:
	# 		if '-N' in line:
	# 			line = line.strip().replace(' ','')
	# 			nodes = int(line.split('-N')[1])
	# 		if '--ntasks-per-node' in line:
	# 			line = line.strip().replace(' ','')
	# 			ppn = int(line.split('=')[1])
	# nprocs = nodes*ppn

	#Setup for Thunder
	# with open(submit_script,'r') as rf:
	# 	for line in rf:
	# 		if 'select' in line:
	# 			line = line.strip().replace(' ','')
	# 			nodes = int(line.split('=')[1].split(':')[0])
	# 			ppn = int(line.split('=')[2])
	# nprocs = nodes*ppn

	return nprocs, ppn

def choose_vasp_version(gpt_version,nprocs):
	"""
	Choose the appropriate VASP version (std or gam)
	Args:
		gpt_version (bool): True if gamma-point only or False
		if standard version
		
		nprocs (int): total number of processors
	"""

	runvasp_file = open('run_vasp.py','w')

	#Setup for A.S. Rosen on Quest
	parallel_cmd = 'mpirun -n'
	vasp_path = '/home/asr731/software/vasp_builds/bin/'
	vasp_ex = [vasp_path+'vasp_std',vasp_path+'vasp_gam']
	module_cmd = 'module load mpi/openmpi-1.8.3-intel2013.2'

	#Setup for NERSC (KNL)
	# parallel_cmd = 'srun -n'+' '+str(nprocs)+' '
	# vasp_path = ''
	# vasp_ex = [vasp_path+'vasp_std',vasp_path+'vasp_gam']
	# module_cmd = 'module load vasp-tpc/5.4.1-knl'

	#Setup for NERSC (SKX)
	# parallel_cmd = 'srun -n'+' '+str(nprocs)+' '
	# vasp_path = ''
	# vasp_ex = [vasp_path+'vasp_std',vasp_path+'vasp_gam']
	# module_cmd = 'module load vasp-tpc/5.4.1'

	#Setup for Stampede2
	# parallel_cmd = 'ibrun -n'+' '+str(nprocs)+' '
	# vasp_path = ''
	# vasp_ex = [vasp_path+'vasp_std_vtst',vasp_path+'vasp_gam_vtst']
	# module_cmd = 'module load vasp/5.4.4'

	#Setup for Thunder
	# parallel_cmd = 'export VASP_NPROCS='+str(nprocs)+' && '
	# vasp_path = ''
	# vasp_ex = [vasp_path+'vasp-vtst_3.2',vasp_path+'vasp_real-vtst_3.2']
	# module_cmd = 'module load VASP/5.4.1'

	#Setting up run_vasp.py
	vasp_cmd = parallel_cmd+vasp_ex[0]
	gamvasp_cmd = parallel_cmd+vasp_ex[1]
	if gpt_version:
		runvasp_file.write("import os\nexitcode = os.system("
			+"'"+module_cmd+' && '+gamvasp_cmd+"'"+')')
	else:
		runvasp_file.write("import os\nexitcode = os.system("
			+"'"+module_cmd+' && '+vasp_cmd+"'"+')')

	runvasp_file.close()
