# Many dynamic objects

import harfang as hg
from math import cos, sin

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 1280, 720
win = hg.RenderInit('Many dynamic objects', res_x, res_y, hg.RF_VSync | hg.RF_MSAA4X)

pipeline = hg.CreateForwardPipeline(4096)  # increase shadow map resolution to 4096x4096
res = hg.PipelineResources()

# create models
vtx_layout = hg.VertexLayoutPosFloatNormUInt8()

sphere_mdl = hg.CreateSphereModel(vtx_layout, 0.1, 8, 16)
sphere_ref = res.AddModel('sphere', sphere_mdl)
ground_mdl = hg.CreateCubeModel(vtx_layout, 60, 0.001, 60)
ground_ref = res.AddModel('ground', ground_mdl)

# create materials
shader = hg.LoadPipelineProgramRefFromFile('resources_compiled/core/shader/default.hps', res, hg.GetForwardPipelineInfo())

sphere_mat = hg.CreateMaterial(shader, 'uDiffuseColor', hg.Vec4(1, 0, 0), 'uSpecularColor', hg.Vec4(1, 0.8, 0))
ground_mat = hg.CreateMaterial(shader, 'uDiffuseColor', hg.Vec4(1, 1, 1), 'uSpecularColor', hg.Vec4(1, 1, 1))

# setup scene
scene = hg.Scene()
scene.canvas.color = hg.Color(0.1, 0.1, 0.1)
scene.environment.ambient = hg.Color(0.1, 0.1, 0.1)

cam = hg.CreateCamera(scene, hg.TransformationMat4(hg.Vec3(15.5, 5, -6), hg.Vec3(0.4, -1.2, 0)), 0.01, 100)
scene.SetCurrentCamera(cam)

hg.CreateSpotLight(scene, hg.TransformationMat4(hg.Vec3(-8.8, 21.7, -8.8), hg.Deg3(60, 45, 0)), 0, hg.Deg(5), hg.Deg(30), hg.Color.White, hg.Color.White, 0, hg.LST_Map, 0.000005)
hg.CreateObject(scene, hg.TranslationMat4(hg.Vec3(0, 0, 0)), ground_ref, [ground_mat])

# create scene objects
rows = []
for z in range(-100, 100, 2):
	row = []
	for x in range(-100, 100, 2):
		node = hg.CreateObject(scene, hg.TranslationMat4(hg.Vec3(x * 0.1, 0.1, z * 0.1)), sphere_ref, [sphere_mat])
		row.append(node.GetTransform())  # store the node transform directly
	rows.append(row)

# main loop
angle = 0

while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
	dt = hg.TickClock()
	angle += hg.time_to_sec_f(dt)

	for j, row in enumerate(rows):
		row_y = cos(angle + j * 0.1)
		for i, trs in enumerate(row):
			pos = trs.GetPos()
			pos.y = 0.1 * (row_y * sin(angle + i * 0.1) * 6 + 6.5)
			trs.SetPos(pos)

	scene.Update(dt)

	hg.SubmitSceneToPipeline(0, scene, hg.IntRect(0, 0, res_x, res_y), True, pipeline, res)
	hg.Frame()

	hg.UpdateWindow(win)

hg.RenderShutdown()
hg.DestroyWindow(win)
