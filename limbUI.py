# from functools import partial
import pymel.core as pm


# Class example
# -------------------------------------------------------------------------------
def snapObject(target, ctrlObject):
    prntConst = pm.parentConstraint(target, ctrlObject, w=1)

    pm.delete(prntConst)


# centerPivot
def centerPivot(target):
    pm.xform(target, cp=1)


def createOffsetGrp(target):
    pm.select(clear=1)

    offset_grp = pm.group(n=target[0] + '_grp_offset')
    prntConst = pm.parentConstraint(target, offset_grp, w=1)
    pm.delete(prntConst)
    pm.xform(offset_grp, cp=1)
    pm.select(clear=1)
    pm.parent(target, offset_grp)

    return offset_grp


# create control shapes
def createCube():
    cube_ctrl = pm.curve(d=1, p=[(1, 1, 1), (1, 1, -1), (-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, -1, 1), (1, -1, -1),
                                 (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (-1, -1, -1), (-1, -1, 1),
                                 (-1, 1, 1), (-1, -1, 1), (1, -1, 1)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    return cube_ctrl


def createSwitch():
    switch = pm.curve(d=1, p=[(0, 1, 0), (1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0), (4, 1, 0), (5, 0, 0), (4, -1, 0),
                              (3, -2, 0), (3, -1, 0), (2, -1, 0), (1, -1, 0), (0, -1, 0), (-1, -1, 0), (-2, -1, 0),
                              (-3, -1, 0), (-3, -2, 0), (-4, -1, 0), (-5, 0, 0), (-4, 1, 0), (-3, 2, 0), (-3, 1, 0),
                              (-2, 1, 0), (-1, 1, 0), (0, 1, 0), ],
                      k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    pm.xform(cp=True)
    pm.scale(.2, .2, .2)
    pm.makeIdentity(apply=True, t=True, r=True, s=True)
    return switch


def createRing():
    circle_ctrl = pm.circle(nr=[0, 1, 0])[0]

    circle_list = []
    circle_list.append(pm.duplicate(rr=True))
    pm.xform(ro=[90, 0, 0])

    circle_list.append(pm.duplicate(rr=True))
    pm.xform(ro=[90, 90, 0])

    circle_list.append(pm.duplicate(rr=True))
    pm.xform(ro=[90, 45, 0])

    circle_list.append(pm.duplicate(rr=True))
    pm.xform(ro=[90, -45, 0])

    pm.select(circle_list)
    pm.makeIdentity(apply=True, t=True, r=True, s=True)
    pm.pickWalk(d='down')
    pm.select(circle_ctrl, tgl=True)
    pm.parent(r=True, s=True)
    pm.delete(circle_list)
    pm.xform(circle_ctrl, cp=True)

    return circle_ctrl


def colorCtr(color=None, ctrl=None, *args):
    if (color == "RED"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(1.0, 0.0, 0.0)

    if (color == "BLUE"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(0.0, 0.0, 1.0)

    if (color == "LIGHTBLUE"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(0.0, 0.156, 1.0)

    if (color == "GREEN"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(0.0, 1.0, 0.0)

    if (color == "YELLOW"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(1.0, 1.0, 0.0)

    if (color == "PINK"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(1.0, 0.0, 1.0)

    if (color == "VOILET"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(0.188, 0.0, 1.0)

    if (color == "ORANGE"):
        ctrl.overrideEnabled.set(1)
        ctrl.overrideRGBColors.set(1)
        ctrl.overrideColorRGB.set(1.0, 0.094, 0.0)


def createHeirarchy(*args):
    pm.select(cl=1)
    rig_grup = pm.group(n="rig_grup")
    pm.select(cl=1)
    ctrl_grup = pm.group(n="ctrl_grup")
    pm.select(cl=1)
    deform_grup = pm.group(n="deform_grup")
    pm.parent(ctrl_grup, deform_grup, rig_grup)


def createFKSetup(fk_chain, *args):
    # create FK controls
    limb_arm = ['upperArm', 'foreArm', 'wrist']
    ctrl_grup = "ctrl_grup"
    i = 0
    # sel = pm.ls(selection = True)
    fk_ctrl_list = []
    fk_ctrl_offset_list = []
    for i in range(len(fk_chain)):
        fk_ctrl = pm.circle(n=limb_arm[i] + '_fk_ctrl', c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01,
                            s=8)
        fk_ctrl_offset = createOffsetGrp(fk_ctrl)
        snapObject(fk_chain[i], fk_ctrl_offset)

        pm.orientConstraint(fk_ctrl, fk_chain[i], mo=1)

        fk_ctrl_list.append(fk_ctrl)
        fk_ctrl_offset_list.append(fk_ctrl_offset)

        colorCtr("RED", fk_ctrl[0])
        pm.select(clear=1)
        i = i + 1

    for i in range(len(fk_chain) - 1):
        pm.parent(fk_ctrl_offset_list[i + 1], fk_ctrl_list[i][0])

    pm.select(clear=1)
    print fk_ctrl_offset_list
    return fk_ctrl_offset_list


# create setups
def createLimbGuide(*args):
    limb_arm = ['upperArm', 'foreArm', 'wrist']
    i = 0
    guideList = []
    for l in limb_arm:
        loc = pm.spaceLocator()
        pm.rename(loc, l + "_guide" + "_LOC")
        pm.setAttr(loc.translateX, i)
        i = i + 5
        guideList.append(loc)

    createHeirarchy()
    return guideList


# create stretch setup
def createLimb_ArmSetup(guideList, *args):
    # loc
    # guideList= createLimbGuide[0]
    # print(guideList)
    refresh_list = []
    ctrl_grup = "ctrl_grup"
    deform_grup = "deform_grup"
    root_ctrl = pm.circle(n="root_ctrl", c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=2, d=1, ut=0,
                          tol=0.01, s=8)
    colorCtr("VOILET", root_ctrl[0])
    root_ctrl_offset = createOffsetGrp(root_ctrl)
    pm.parent(root_ctrl_offset, "ctrl_grup")
    # arm_ctrl = pm.circle(n='arm_ctrl',c= (0, 0, 0),nr=( 0, 1, 0), sw= 360, r =1,d= 3,ut= 0, tol= 0.01,s=8)
    pm.select(clear=1)

    upper_loc = "upperArm_guide_LOC"  # upperlimb
    middle_loc = "foreArm_guide_LOC"  # middlelimb
    end_loc = "wrist_guide_LOC"  # endlimb

    # control list
    pm.select(clear=1)
    # get location of locators
    pos_upper = pm.xform(upper_loc, ws=1, t=1, q=1)
    pos_middle = pm.xform(middle_loc, ws=1, t=1, q=1)
    pos_end = pm.xform(end_loc, ws=1, t=1, q=1)
    # create joint chain on position
    jnt_chain = []
    # creating joint chain
    upper_arm_jnt = pm.joint(n="upper_arm_jnt", p=pos_upper, oj="yzx")
    lower_arm_jnt = pm.joint(n="lower_arm_jnt", p=pos_middle, oj="yzx")
    wrist_jnt = pm.joint(n="wrist_jnt", p=pos_end, oj="yzx")
    # orient joint chain
    pm.joint(upper_arm_jnt, e=1, oj='yzx', secondaryAxisOrient="zup", ch=1, zso=1)

    jnt_chain.append(upper_arm_jnt)
    jnt_chain.append(lower_arm_jnt)
    jnt_chain.append(wrist_jnt)
    # reorient last joint
    pm.setAttr(jnt_chain[2] + ".jointOrientX", 0)
    pm.setAttr(jnt_chain[2] + ".jointOrientY", 0)
    pm.setAttr(jnt_chain[2] + ".jointOrientZ", 0)

    # creat fk and ik chain
    ik_chain = pm.duplicate(jnt_chain)
    fk_chain = pm.duplicate(jnt_chain)
    pm.setAttr(ik_chain[0].visibility, 0)
    pm.setAttr(fk_chain[0].visibility, 0)

    pm.parent(jnt_chain[0], deform_grup)
    pm.parent(ik_chain[0], deform_grup)
    pm.parent(fk_chain[0], deform_grup)
    pm.select(clear=1)
    # ------------------------------------------------------------------------
    # create IK handle
    ik_hdl = pm.ikHandle(sj=ik_chain[0], ee=ik_chain[2], n="l_arm_ikHdl")

    ik_hdl_grp = createOffsetGrp(ik_hdl[0])
    pm.parent(ik_hdl_grp, deform_grup)
    pm.setAttr(ik_hdl_grp.visibility, 0)
    # create controls
    ik_ctrl = createCube()
    colorCtr("ORANGE", ik_ctrl)
    pm.rename(ik_ctrl, 'l_arm_ik_ctrl')
    snapObject(jnt_chain[2], ik_ctrl)
    ik_ctrl_grp = createOffsetGrp(ik_ctrl)
    pm.parent(ik_ctrl_grp, root_ctrl[0])

    # constraint ik hdl
    pm.pointConstraint(ik_ctrl, ik_hdl_grp, offset=[0, 0, 0], weight=1)
    # -------------------------------------------------------------------------
    # create locators for pole vector position

    loc1 = pm.spaceLocator(n="loc1")
    loc2 = pm.spaceLocator(n="loc2")

    grp1 = pm.group(loc1, n=loc1 + "grp1_offset")
    grp2 = pm.group(loc2, n=loc2 + "grp2_offset")
    # create elbow control
    elbow_ctrl = createRing()
    colorCtr("ORANGE", elbow_ctrl)
    pm.rename(elbow_ctrl, 'elbow_ctrl')
    elbow_ctrl_grp = createOffsetGrp(elbow_ctrl)
    pm.parent(elbow_ctrl_grp, root_ctrl[0])

    # point constraint grp1 to root and end
    pm.pointConstraint(ik_chain[0], ik_chain[2], grp1, offset=[0, 0, 0], weight=1)
    # aim const grp1 to root jnt
    pm.aimConstraint(ik_chain[0], grp1, offset=[0, 0, 0], weight=1, aimVector=[0, 1, 0], upVector=[0, 1, 0],
                     worldUpType="scene")
    # point const loc1 to middle joint, only y axis
    pm.pointConstraint(ik_chain[1], loc1, offset=[0, 0, 0], skip=["x", "z"], weight=1)
    # point const grp2 to middle joint
    pm.pointConstraint(ik_chain[1], grp2, offset=[0, 0, 0], weight=1)
    # aim constraint grp2 to loc1, choose axis which will move loc1 away
    pm.aimConstraint(loc1, grp2, offset=[0, 0, 0], weight=1, aimVector=[0, 0, 1], upVector=[0, 1, 0],
                     worldUpType="scene")
    pm.move(0, 0, -12, loc2, os=True, rpr=True)
    snapObject(loc2, elbow_ctrl_grp)

    pm.poleVectorConstraint(elbow_ctrl, ik_hdl[0], w=1)
    # _________________________________________________________________________
    pm.select(clear=1)

    fk_chain_grp_list = createFKSetup(fk_chain)
    pm.parent(fk_chain_grp_list[0], root_ctrl[0])
    # pm.parent(grp1,grp2,elbow_loc_grp,fk_chain_grp_list[0],setup_grp)
    # create switch and add attributes
    switch = createSwitch()

    colorCtr("YELLOW", switch)
    pm.rename(switch, 'l_arm_switch')

    snapObject(jnt_chain[2], switch)

    switch_offset_grup = createOffsetGrp(switch)
    pm.parent(switch_offset_grup, root_ctrl[0])

    # make control follow the arm
    pm.xform(switch_offset_grup, cp=1)
    snapObject(jnt_chain[2], switch_offset_grup)
    pm.move(0, 5, 0, switch, os=True, rpr=True)
    pm.parentConstraint(jnt_chain[2], switch_offset_grup, mo=1)

    # add attribute
    pm.addAttr(switch, ln='toggle', at="enum", en=":")
    pm.addAttr(switch, ln='FK_IK_switch', at='double', k=1, min=0, max=1, dv=0)

    # pm.parent(switch_offset_grup,setup_grp)

    # connect fk,ik and jnt chain

    for i in range(len(jnt_chain)):
        blndClr = pm.shadingNode('blendColors', asUtility=True, n=jnt_chain[i] + '_blndClr')

        pm.connectAttr(str(ik_chain[i]) + '.rotate', str(blndClr) + '.color1', f=1)

        pm.connectAttr(str(fk_chain[i]) + '.rotate', str(blndClr) + '.color2', f=1)

        pm.connectAttr(str(switch) + '.FK_IK_switch', str(blndClr) + '.blender', f=1)

        pm.connectAttr(str(blndClr) + '.output', str(jnt_chain[i]) + '.rotate', f=1)

        pm.connectAttr(ik_chain[i] + '.rotate', blndClr + '.color1', f=1)

        pm.connectAttr(fk_chain[i] + '.rotate', blndClr + '.color2', f=1)

        pm.connectAttr(str(switch) + '.FK_IK_switch', blndClr + '.blender', f=1)

        pm.connectAttr(blndClr + '.output', jnt_chain[i] + '.rotate', f=1)

    reverse_vis = pm.shadingNode('reverse', asUtility=True, n=fk_chain_grp_list[0] + '_reverse')

    # connect fk ik switch
    pm.connectAttr(str(switch) + '.FK_IK_switch', str(reverse_vis) + '.inputX', f=1)
    pm.connectAttr(str(reverse_vis) + '.outputX', fk_chain_grp_list[0] + '.visibility', f=1)
    pm.connectAttr(str(switch) + '.FK_IK_switch', str(ik_ctrl_grp) + '.visibility', f=1)
    pm.connectAttr(str(ik_ctrl_grp) + '.visibility', str(elbow_ctrl_grp) + '.visibility', f=1)

    # delete guides
    pm.delete(grp1)
    pm.delete(grp2)
    pm.delete(upper_loc)
    pm.delete(middle_loc)
    pm.delete(end_loc)

    # snapObject(jnt_chain[0],arm_ctrl[0])
    # switch_offset_grup(arm_ctrl[0])

    return jnt_chain, ik_ctrl, ik_hdl_grp, fk_chain_grp_list, switch_offset_grup, ik_chain, elbow_ctrl_grp, root_ctrl


def createIK_stretch(guideList, *args):
    # limbs
    Limb_chain, ik_ctrl, ik_hdl_grp, fk_chain_grp_list, switch_offset_grup, ik_chain, elbow_ctrl_grp, root_ctrl = createLimb_ArmSetup(
        guideList)

    deform_grup = "deform_grup"

    Limb_start = Limb_chain[0]

    Limb_middle = Limb_chain[1]

    Limb_end = Limb_chain[2]

    # pos of middle limb joint
    Limb_middle_pos = pm.getAttr(Limb_middle.translateY)

    # pos of end limb/wrist joint
    Limb_end_pos = pm.getAttr(Limb_end.translateY)

    # calculate length of arm
    limb_length_pma = pm.shadingNode("plusMinusAverage", asUtility=True, n="limb_length_pma")

    # calculate change in length by dividing current length by arm length
    change_length = pm.shadingNode("multiplyDivide", asUtility=True)

    # condition if current length is greater than length
    change_length_condition = pm.shadingNode("condition", asUtility=True)

    # multply change to translation Y of joint
    stretch_Limb_middle_md = pm.shadingNode("multiplyDivide", asUtility=True)

    ##making stretch scalable by multiplying it by global scale value
    global_scale_md = pm.shadingNode("multiplyDivide", asUtility=True)

    stretch_Limb_end_md = pm.shadingNode("multiplyDivide", asUtility=True)

    pm.select(cl=1)
    # dist = pm.distanceDimension(sp= Limb_middle_pos, ep= Limb_end_pos )

    dist = pm.distanceDimension(sp=(0, 0, 0), ep=(0, 0, 1))
    pm.setAttr(dist.visibility, 0)
    loc_start = pm.listConnections(dist)[0]
    loc_end = pm.listConnections(dist)[1]
    pm.setAttr(loc_start.visibility, 0)
    pm.setAttr(loc_end.visibility, 0)

    pm.parentConstraint(Limb_start, loc_start, mo=0)
    pm.parentConstraint(ik_ctrl, loc_end, mo=0)

    pm.setAttr(limb_length_pma.input1D[0], Limb_middle_pos)
    pm.setAttr(limb_length_pma.input1D[1], Limb_end_pos)

    pm.setAttr(change_length.operation, 2)
    pm.setAttr(change_length_condition.operation, 2)
    pm.setAttr(stretch_Limb_middle_md.input2X, Limb_middle_pos)
    pm.setAttr(stretch_Limb_end_md.input2X, Limb_end_pos)

    # compensate for scale
    pm.connectAttr(root_ctrl[0].scaleX, global_scale_md.input1X)
    pm.connectAttr(limb_length_pma.output1D, global_scale_md.input2X)

    # calucate change in length factor
    pm.connectAttr(dist.distance, change_length.input1X)
    pm.connectAttr(global_scale_md.outputX, change_length.input2X)

    # check if current distance is greater than arm length
    pm.connectAttr(dist.distance, change_length_condition.firstTerm)
    pm.connectAttr(global_scale_md.outputX, change_length_condition.secondTerm)
    pm.connectAttr(change_length.outputX, change_length_condition.colorIfTrueR)

    # multply change factor to tranlate y 0r primary axis of limb
    pm.connectAttr(change_length_condition.outColorR, stretch_Limb_middle_md.input1X)
    pm.connectAttr(change_length_condition.outColorR, stretch_Limb_end_md.input1X)
    pm.connectAttr(stretch_Limb_middle_md.outputX, Limb_middle.translateY)
    pm.connectAttr(stretch_Limb_end_md.outputX, Limb_end.translateY)

    pm.parent(loc_start, deform_grup)
    pm.parent(loc_end, deform_grup)
    pm.parent(dist, deform_grup)

    return Limb_chain, ik_ctrl, ik_hdl_grp, fk_chain_grp_list, switch_offset_grup, ik_chain, loc_end, loc_start, dist


# Launch the UI
'''This function will house all the commands to build the UI'''

win_name = 'BasicUI'
win_title = 'Basic Window'
win_width = 225
win_height = 75
# If the window already exists, delete it before creating a new one

if pm.window(win_name, exists=True):
    pm.deleteUI(win_name)

# Create the window and its contents
with pm.window(win_name, title= win_title ) as win:
    # Declare Controls Here
    with pm.frameLayout(cll =1, label = "Create Limbs"):
    # -----------------------------------------------------------------------
        with pm.columnLayout(nch=1, adjustableColumn=True):
            pm.separator(style='in')
            with pm.rowLayout(nc=2, adjustableColumn=True, cal=(1, 'left')):
                label = pm.text(label='Create guides')
                button = pm.button(label='Create', ekf= 1, w = win_width/2,command=createLimbGuide )

        with pm.columnLayout(nch=1, adjustableColumn=True):
            pm.separator(style='in')
            with pm.rowLayout(nc=2, adjustableColumn=True, cal=(1, 'left')):
                label = pm.text(label='Create limb setup')
                pm.button(label='Generate',ekf= 1,w = win_width/2,command=createIK_stretch)

# Show the window and edit its size
pm.showWindow(win_name)
pm.window(win_name, edit=True, widthHeight=(win_width, win_height),rtf=1)
