
from pymel.core import *
import json
import os


def exportShader(*args):
	"""
	"""
	sceneDir = str(system.sceneName().dirname())
	sceneName = str(system.sceneName().namebase)
	shaderNetFile = '/'.join([sceneDir, sceneName + '__shaderNet.ma'])
	shaderMapFile = '/'.join([sceneDir, sceneName + '__shaderMap.json'])

	# select meshes that you want to export
	selectedMesh = ls(sl= 1, typ= 'mesh')
	# select shader
	hyperShade(smn= True)
	# export selected shaderNetwork
	system.exportSelected(shaderNetFile, type= 'mayaAscii', f= 1)
	# export shader assign map
	selectedShader = ls(sl= 1)
	shaderMap = {}
	for shader in selectedShader:
		hyperShade(objects= shader)
		meshAssigned = ls(sl= 1)
		shaderMap[str(shader.name())] = [str(m.name()) for m in meshAssigned]
	with open(shaderMapFile, 'w') as jsonFile:
		json.dump(shaderMap, jsonFile, indent=4)


def importShader(*args):
	"""
	"""
	result = fileDialog2(cap= 'Select Exported Shading File', fm= 1, okc= 'Select')
	if not result:
		return
	else:
		shaderNetFile = result[0]
	shaderNetName = shaderNetFile.split('__shaderNet.ma')[0]
	shaderMapFile = shaderNetName + '__shaderMap.json'
	# import shading network
	namespace = Path(shaderNetFile).namebase.replace('.', '_')
	system.createReference(shaderNetFile, ns= namespace)
	# Remap shader
	shaderMap = {}
	with open(shaderMapFile) as jsonFile:
		shaderMap = json.load(jsonFile)
	for shader in shaderMap:
		impShad = namespace + ':' + shader
		if objExists(impShad):
			select(cl= 1)
			for mesh in shaderMap[shader]:
				meshFace = ''
				if '.f' in mesh:
					meshFace = '.f' + mesh.split('.f')[1]
					mesh = mesh.split('.f')[0]
				for realMesh in ls(mesh, r= 1):
					if ls(sl= 1):
						if not realMesh in listRelatives(ls(sl= 1), typ= 'mesh', ad= 1):
							continue
					if realMesh.intermediateObject.get():
						realMesh = listRelatives(realMesh.getParent(), ni= True, typ= 'mesh', s= 1)
					if meshFace and realMesh:
						realMesh = ls(realMesh[0] + meshFace)
					select(realMesh, add= 1)
			hyperShade(a= impShad)
		else:
			warning('Shader Not Found !  ' + impShad)


def ui_main():
	"""
	"""
	windowName = 'ms_transShader_mainUI'
	windowWidth = 200
	windowHeight = 120

	if window(windowName, q= 1, ex= 1):
		deleteUI(windowName)

	window(windowName, t= 'MS_TransShader', s= 0, mxb= 0, mnb= 0)
	columnLayout(adj= 1)
	button(l= 'Export', h= 60, c= exportShader)
	button(l= 'Import', h= 60, c= importShader)
	setParent('..')

	window(windowName, e= 1, w= windowWidth, h= windowHeight)
	showWindow(windowName)