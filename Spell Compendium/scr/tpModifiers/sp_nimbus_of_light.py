from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Nimbus of Light"

def nimbusOfLightSpellBeginRound(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    roundsCharged = args.get_arg(2)
    if roundsCharged < spellPacket.caster_level:
        roundsCharged += 1
        args.set_arg(2, roundsCharged)
    return 0

def nimbusOfLightSpellRadialMenuEntry(attachee, args, evt_obj):
    radialMenuRayAttackId = 1701
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if args.get_arg(2) < spellPacket.caster_level:
        nimbusOfLightRadialId = tpdp.RadialMenuEntryPythonAction("Nimbus of Light (charged to: +{})".format(args.get_arg(2)), D20A_PYTHON_ACTION, radialMenuRayAttackId, 0, "TAG_SPELLS_NIMBUS_OF_LIGHT")
    else:
        nimbusOfLightRadialId = tpdp.RadialMenuEntryPythonAction("Nimbus of Light (charged to: MAX)", D20A_PYTHON_ACTION, radialMenuRayAttackId, 0, "TAG_SPELLS_NIMBUS_OF_LIGHT")
    nimbusOfLightRadialId.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Offense)
    return 0

def nimbusOfLightSpellTouchAttackSignal(attachee, args, evt_obj):
    print "Hook from D20 Signal"
    return 0

def nimbusOfLightSpellTouchAttackPerform(attachee, args, evt_obj):
    args.set_arg(3, 0) #set attack_hit_status
    spellTarget = evt_obj.d20a.target
    distanceToTarget = spellTarget.distance_to(attachee)
    #print "Distance to target: {}".format(distanceToTarget)
    if spellTarget.distance_to(attachee) > 30: #Nimbus of Light has a 30 ft. range
        spellTarget.float_text_line("Out of Range")
        game.particles('Fizzle', attachee)
        #reduce the cost to 0 when out of range?
        return AEC_TARGET_OUT_OF_RANGE

    evt_obj.d20a.flags |= D20CAF_RANGED
    evt_obj.d20a.flags |= D20CAF_TOUCH_ATTACK
    evt_obj.d20a.to_hit_processing()
    
    game.create_history_from_id(evt_obj.d20a.roll_id_1)
    game.create_history_from_id(evt_obj.d20a.roll_id_2)
    game.create_history_from_id(evt_obj.d20a.roll_id_0)
    
    if evt_obj.d20a.flags & D20CAF_HIT:
        args.set_arg(3, 1)
    if evt_obj.d20a.flags & D20CAF_CRITICAL:
        args.set_arg(3, 2)
        isCriticalHit = 1
    else:
        isCriticalHit = 0

    if attachee.anim_goal_push_attack(spellTarget, game.random_range(0,2), isCriticalHit ,0):
        new_anim_id = attachee.anim_goal_get_new_id()
        evt_obj.d20a.flags |= D20CAF_NEED_ANIM_COMPLETED
        evt_obj.d20a.anim_id = new_anim_id
    return 0

def nimbusOfLightSpellTouchAttackFrame(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellTarget = evt_obj.d20a.target
    spellDamageDice = dice_new('1d8')
    spellDamageDice.bonus = args.get_arg(2)
    if args.get_arg(3) == 2:
        spellDamageDice.number = 2
        spellDamageDice.bonus *= 2

    spellProjectile = evt_obj.d20a.create_projectile_and_throw(3000, spellTarget) #protoID 3000 = invisible projectile
    spellProjectile.obj_set_int(obj_f_projectile_part_sys_id, game.particles('sp-Ray of Frost', spellProjectile))
    spellProjectile.obj_set_float(obj_f_offset_z, 60.0)
    ammunition = OBJ_HANDLE_NULL
    if evt_obj.d20a.projectile_append(spellProjectile, ammunition):
        attachee.apply_projectile_particles(spellProjectile, evt_obj.d20a.flags)
        evt_obj.d20a.flags |= D20CAF_NEED_PROJECTILE_HIT

    if args.get_arg(3):
        spellTarget.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0)) #there is no DT_LIGHT
    else:
        spellTarget.float_mesfile_line('mes\\spell.mes', 30007)
        game.particles('Fizzle', spellTarget)
    
    #spell ends, when ray is fired
    args.remove_spell()
    args.remove_spell_mod()
    return 0

#######   Weapon Focus Ray Fix   #######
def nimbusOfLightSpellWfRayFix(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_flags() & D20CAF_TOUCH_ATTACK:
        return 0
    if not evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        return 
    #add_from_feat does not allow freetext
    if attachee.has_feat(feat_greater_weapon_focus_ray):
        evt_obj.bonus_list.add(2, 0, "Feat: ~Greater Weapon Foucs (Ray)~[TAG_WEAPON_FOCUS]")
    elif attachee.has_feat(feat_weapon_focus_ray):
        evt_obj.bonus_list.add(1, 0, "Feat: ~Weapon Foucs (Ray)~[TAG_WEAPON_FOCUS]")
    return 0
####### Weapon Focus Ray Fix END #######

def nimbusOfLightSpellTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if args.get_arg(1) == 1:
        evt_obj.append("Nimbus of Light ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Nimbus of Light ({} rounds)".format(args.get_arg(1)))
    if args.get_arg(2) < spellPacket.caster_level:
        evt_obj.append("Nimbus of Light charged to: {})".format(args.get_arg(2)))
    else:
        evt_obj.append("Nimbus of Light charged to: MAX)")
    return 0

def nimbusOfLightSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("NIMBUS_OF_LIGHT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("NIMBUS_OF_LIGHT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def nimbusOfLightSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def nimbusOfLightSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def nimbusOfLightSpellSpellEnd(attachee, args, evt_obj):
    print "Nimbus of Light SpellEnd"
    return 0

nimbusOfLightSpell = PythonModifier("sp-Nimbus of Light", 4) # spell_id, duration, roundsCharged, attack_hit_status
nimbusOfLightSpell.AddHook(ET_OnBeginRound, EK_NONE, nimbusOfLightSpellBeginRound, ())
nimbusOfLightSpell.AddHook(ET_OnD20PythonActionPerform, EK_NONE, nimbusOfLightSpellTouchAttackPerform, ())
nimbusOfLightSpell.AddHook(ET_OnD20PythonActionFrame, EK_NONE, nimbusOfLightSpellTouchAttackFrame, ())
nimbusOfLightSpell.AddHook(ET_OnToHitBonus2, EK_NONE, nimbusOfLightSpellWfRayFix, ())
nimbusOfLightSpell.AddHook(ET_OnBuildRadialMenuEntry, EK_NONE, nimbusOfLightSpellRadialMenuEntry, ())
nimbusOfLightSpell.AddHook(ET_OnGetTooltip, EK_NONE, nimbusOfLightSpellTooltip, ())
nimbusOfLightSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, nimbusOfLightSpellEffectTooltip, ())
nimbusOfLightSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, nimbusOfLightSpellSpellEnd, ())
nimbusOfLightSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, nimbusOfLightSpellHasSpellActive, ())
nimbusOfLightSpell.AddHook(ET_OnD20Signal, EK_S_Killed, nimbusOfLightSpellKilled, ())
nimbusOfLightSpell.AddSpellDispelCheckStandard()
nimbusOfLightSpell.AddSpellTeleportPrepareStandard()
nimbusOfLightSpell.AddSpellTeleportReconnectStandard()
nimbusOfLightSpell.AddSpellCountdownStandardHook()

