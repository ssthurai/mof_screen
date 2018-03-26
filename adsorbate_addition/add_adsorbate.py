import numpy as np
from ase.io import read, write
from ase import Atoms, Atom
from settings import coremof_path, ads_species, ads_mol_idx, newmofs_path, error_path, overlap_tol
from ase.collections import g2
from ase.build import molecule

def add_ads_species(cif_file,ads_site):
#add adsorbate to original CIF and save new CIF

	mof_temp = read(coremof_path+cif_file)
	if len(ads_species) == 1:
		adsorbate = Atoms([Atom(ads_species,ads_site)])
	else:
		if ads_species in g2.names:
			adsorbate = molecule(ads_species)
			for i, atom in enumerate(adsorbate):
				if i != ads_mol_idx:
					atom.position += ads_site - adsorbate[ads_mol_idx].position
			adsorbate[ads_mol_idx].position = ads_site
		else:
			raise ValueError('Only molecules in the g2 collection are supported')
		
	mof_temp.extend(adsorbate)

	return mof_temp

def write_oms_file(refcode,cif_file,ads_sites,best_to_worst_idx,cluster):
#write CIF file with OMS-adsorbate

	basename = refcode+'_'+ads_species
	success = False
	for idx in best_to_worst_idx:
		mof = add_ads_species(cif_file,ads_sites[idx,:])
		dist_mat = mof.get_distances(len(mof)-1,np.arange(0,len(mof)-1).tolist(),mic=True)
		if sum(dist_mat <= overlap_tol) == 0:
			print('SUCCESS: '+refcode+' ('+str(cluster)+')')
			write(newmofs_path+basename+'_OMS'+str(idx)+'.cif',mof)
			success = True
			break
		else:
			del mof[-1]
	if success == False:
		print('ERROR: '+refcode+' ('+str(cluster)+')')
		write(error_path+basename+'_'+str(cluster)+'.cif',mof)

def write_ads_file(refcode,cif_file,ads_site):
#write CIF file with adsorbate

	basename = refcode+'_'+ads_species
	success = False
	mof = add_ads_species(cif_file,ads_site)
	dist_mat = mof.get_distances(len(mof)-1,np.arange(0,len(mof)-1).tolist(),mic=True)
	if sum(dist_mat <= overlap_tol) == 0:
		print('SUCCESS: '+refcode)
		write(newmofs_path+basename+'.cif',mof)
		success = True
	if success == False:
		print('ERROR: '+refcode)
		write(error_path+basename+'.cif',mof)