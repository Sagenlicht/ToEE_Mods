from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Holy Storm"

def holyStormSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    holyStormPartsysId = game.particles('sp-Holy Storm', attachee)
    spellPacket.add_spell_object(attachee, holyStormPartsysId) # store the spell obj and the particle sys
    radiusHolyStorm = 20.0
    holyStormEventId = attachee.object_event_append(OLC_CRITTERS, radiusHolyStorm)
    args.set_arg(3, holyStormEventId)
    spellPacket.update_registry()
    return 0

def holyStormSpellOnEnteredAoe(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    holyStormEventId = args.get_arg(3)
    print "Holy Storm enter: ", spellTarget

    if holyStormEventId != evt_obj.evt_id:
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Holy Storm Effect', args.get_arg(0), args.get_arg(1), 0, args.get_arg(3))
    return 0

def holyStormSpellOnBeginRound(attachee, args, evt_obj):
    crittersInAoe = game.obj_list_cone(attachee, OLC_CRITTERS, 20, 0, 360)
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    neededAlignment = [ALIGNMENT_LAWFUL_EVIL, ALIGNMENT_NEUTRAL_EVIL, ALIGNMENT_CHAOTIC_EVIL]
    evilOutsiderInAoe = []
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 5
    
    for target in crittersInAoe:
        targetIsDead = target.d20_query(Q_Dead)
        if target.stat_level_get(stat_alignment) in neededAlignment:
            hasEvilAlignment = True
        else:
            hasEvilAlignment = False
        if target.is_category_type(mc_type_outsider):
            isOutsider = True
        else:
            isOutsider = False
        if not targetIsDead and hasEvilAlignment and isOutsider:
            evilOutsiderInAoe.append(target)
    
    if not evilOutsiderInAoe:
        return 0
    
    numberOfTargets = len(evilOutsiderInAoe)
    randomDice = dice_new('1d{}'.format(numberOfTargets))
    selectTarget = randomDice.roll() - 1 #first element in list is 0 not 1
    spellTarget = evilOutsiderInAoe[selectTarget]
    game.particles('sp-Holy Storm-hit', spellTarget)
    game.create_history_freeform("{} is affected by ~Holy Storm~[TAG_SPELLS_HOLY_STORM] burst\n\n".format(spellTarget.description))
    spellTarget.float_text_line("Holy Storm burst", tf_red)
    spellTarget.spell_damage(spellPacket.caster, D20DT_COLD, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def holyStormSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def holyStormSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def holyStormSpellSpellEnd(attachee, args, evt_obj):
    print "Holy Storm SpellEnd"
    return 0

holyStormSpell = PythonModifier("sp-Holy Storm", 4) # spell_id, duration, empty, eventId
holyStormSpell.AddHook(ET_OnConditionAdd, EK_NONE, holyStormSpellOnConditionAdd, ())
holyStormSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, holyStormSpellOnEnteredAoe, ())
#holyStormSpell.AddHook(ET_OnBeginRound, EK_NONE, holyStormSpellOnBeginRound, ())
holyStormSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, holyStormSpellSpellEnd, ())
holyStormSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, holyStormSpellHasSpellActive, ())
holyStormSpell.AddHook(ET_OnD20Signal, EK_S_Killed, holyStormSpellKilled, ())
holyStormSpell.AddSpellDispelCheckStandard()
holyStormSpell.AddSpellTeleportPrepareStandard()
holyStormSpell.AddSpellTeleportReconnectStandard()
holyStormSpell.AddSpellCountdownStandardHook()
holyStormSpell.AddAoESpellEndStandardHook()

### Begin Holy Storm Effect ###

def holyStormEffectOnBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellTarget = attachee
        neededAlignment = [ALIGNMENT_LAWFUL_EVIL, ALIGNMENT_NEUTRAL_EVIL, ALIGNMENT_CHAOTIC_EVIL]
        spellDamageDice = dice_new('1d6')
        
        if not spellTarget.stat_level_get(stat_alignment) in neededAlignment:
            return 0
        elif spellTarget.is_category_type(mc_type_outsider):
            spellDamageDice.number = 4
        else:
            spellDamageDice.number = 2
        game.create_history_freeform("{} is affected by ~Holy Storm~[TAG_SPELLS_HOLY_STORM]\n\n".format(spellTarget.description))
        spellTarget.float_text_line("Holy Storm", tf_red)
        spellTarget.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def holyStormEffectSkillPenalty(attachee, args, evt_obj):
     evt_obj.bonus_list.add(-4, 160, "~Holy Storm~[TAG_SPELLS_HOLY_STORM] Penalty") #Holy Storm gives a -4 penalty on Listen, Search and Spot Checks
     return 0

def holyStormEffectAttackPenalty(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(-4, 160, "~Holy Storm~[TAG_SPELLS_HOLY_STORM] Penalty") #Holy Storm gives a -4 penalty on ranged attacks made in, into, or out of the storm
    return 0

def holyStormEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Holy Storm ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Holy Storm ({} rounds)".format(args.get_arg(1)))
    return 0

def holyStormEffectEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("HOLY_STORM"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("HOLY_STORM"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def holyStormEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    holyStormEventId = args.get_arg(3)
    if holyStormEventId != evt_obj.evt_id:
        print "ID Mismach"
        return 0
    args.condition_remove()
    return 0

def holyStormEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def holyStormEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def holyStormEffectHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

holyStormEffect = PythonModifier("Holy Storm Effect", 4) #spell_id, duration, empty, eventId
holyStormEffect.AddHook(ET_OnBeginRound, EK_NONE, holyStormEffectOnBeginRound, ())
holyStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, holyStormEffectSkillPenalty, ())
holyStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, holyStormEffectSkillPenalty, ())
holyStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, holyStormEffectSkillPenalty, ())
holyStormEffect.AddHook(ET_OnToHitBonus2, EK_NONE, holyStormEffectAttackPenalty, ())
holyStormEffect.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, holyStormEffectAttackPenalty, ())
holyStormEffect.AddHook(ET_OnGetTooltip, EK_NONE, holyStormEffectTooltip, ())
holyStormEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, holyStormEffectEffectTooltip, ())
holyStormEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, holyStormEffectOnLeaveAoE, ())
holyStormEffect.AddHook(ET_OnConditionRemove, EK_NONE, holyStormEffectOnRemove, ())
holyStormEffect.AddHook(ET_OnD20Signal, EK_S_Killed, holyStormEffectSpellKilled, ())