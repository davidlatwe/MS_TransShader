
import pymel.core as pm
import json
import os


def exportShader(*args):
	"""
	"""
	sceneDir = str(pm.sceneName().dirname())
	sceneName = str(pm.sceneName().namebase)
	shaderNetFile = '/'.join([sceneDir, sceneName + '__shaderNet.ma'])
	shaderMapFile = '/'.join([sceneDir, sceneName + '__shaderMap.json'])

	# select meshes that you want to export
	selectedMesh = pm.ls(sl= 1, typ= 'mesh')
	# select shader
	pm.hyperShade(smn= True)
	# export selected shaderNetwork
	pm.exportSelected(shaderNetFile, type= 'mayaAscii', f= 1)
	# export shader assign map
	selectedShader = pm.ls(sl= 1)
	shaderMap = {}
	for shader in selectedShader:
		pm.hyperShade(objects= shader)
		meshAssigned = pm.ls(sl= 1)
		shaderMap[str(shader.name())] = [str(m.name()) for m in meshAssigned]
	with open(shaderMapFile, 'w') as jsonFile:
		json.dump(shaderMap, jsonFile, indent=4)


def importShader(*args):
	"""
	"""
	result = pm.fileDialog2(cap= 'Select Exported Shading File', fm= 1, okc= 'Select')
	if not result:
		return
	else:
		shaderNetFile = result[0]
	shaderNetName = shaderNetFile.split('__shaderNet.ma')[0]
	shaderMapFile = shaderNetName + '__shaderMap.json'
	# import shading network
	namespace = Path(shaderNetFile).namebase.replace('.', '_')
	pm.createReference(shaderNetFile, ns= namespace)
	# Remap shader
	shaderMap = {}
	with open(shaderMapFile) as jsonFile:
		shaderMap = json.load(jsonFile)
	for shader in shaderMap:
		impShad = namespace + ':' + shader
		if pm.objExists(impShad):
			pm.select(cl= 1)
			for mesh in shaderMap[shader]:
				meshFace = ''
				if '.f' in mesh:
					meshFace = '.f' + mesh.split('.f')[1]
					mesh = mesh.split('.f')[0]
				print '? ' * 10
				print mesh
				print '? ' * 10
				for realMesh in pm.ls(mesh, r= 1):
					if realMesh.intermediateObject.get():
						realMesh = pm.listRelatives(realMesh.getParent(), ni= True, typ= 'mesh', s= 1)[0]
					if meshFace and realMesh:
						realMesh = pm.ls(realMesh.name() + meshFace)
					pm.select(realMesh, add= 1)
			print '- + '*10
			print shader
			print pm.ls(sl= 1)
			print '- + '*10
			pm.hyperShade(a= impShad)
		else:
			pm.warning('Shader Not Found !  ' + impShad)


def ui_main():
	"""
	"""
	windowName = 'ms_transShader_mainUI'
	windowWidth = 200
	windowHeight = 120

	if pm.window(windowName, q= 1, ex= 1):
		pm.deleteUI(windowName)

	pm.window(windowName, t= 'MS_TransShader', s= 0, mxb= 0, mnb= 0)
	pm.columnLayout(adj= 1)
	pm.button(l= 'Export', h= 60, c= exportShader)
	pm.button(l= 'Import', h= 60, c= importShader)
	pm.setParent('..')

	pm.window(windowName, e= 1, w= windowWidth, h= windowHeight)
	pm.showWindow(windowName)