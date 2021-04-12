from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Unholy Storm"

def unholyStormSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    unholyStormPartsysId = game.particles('sp-Holy Storm', attachee)
    spellPacket.add_spell_object(attachee, unholyStormPartsysId) # store the spell obj and the particle sys
    radiusUnholyStorm = 20.0
    unholyStormEventId = attachee.object_event_append(OLC_CRITTERS, radiusUnholyStorm)
    args.set_arg(3, unholyStormEventId)
    spellPacket.update_registry()
    return 0

def unholyStormSpellOnEnteredAoe(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    unholyStormEventId = args.get_arg(3)
    print "Unholy Storm enter: ", spellTarget

    if unholyStormEventId != evt_obj.evt_id:
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Unholy Storm Effect', args.get_arg(0), args.get_arg(1), 0, args.get_arg(3))
    return 0

def unholyStormSpellOnBeginRound(attachee, args, evt_obj):
    crittersInAoe = game.obj_list_cone(attachee, OLC_CRITTERS, 20, 0, 360)
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    neededAlignment = [ALIGNMENT_LAWFUL_GOOD, ALIGNMENT_NEUTRAL_GOOD, ALIGNMENT_CHAOTIC_GOOD]
    goodOutsiderInAoe = []
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 5
    
    for target in crittersInAoe:
        targetIsDead = target.d20_query(Q_Dead)
        if target.stat_level_get(stat_alignment) in neededAlignment:
            hasGoodAlignment = True
        else:
            hasGoodAlignment = False
        if target.is_category_type(mc_type_outsider):
            isOutsider = True
        else:
            isOutsider = False
        if not targetIsDead and hasGoodAlignment and isOutsider:
            goodOutsiderInAoe.append(target)
    
    if not goodOutsiderInAoe:
        return 0
    
    numberOfTargets = len(goodOutsiderInAoe)
    randomDice = dice_new('1d{}'.format(numberOfTargets))
    selectTarget = randomDice.roll() - 1 #First List Element is 0 not 1
    spellTarget = goodOutsiderInAoe[selectTarget]
    game.particles('sp-Unholy Storm-hit', spellTarget)
    game.create_history_freeform("{} is affected by ~Unholy Storm~[TAG_SPELLS_UNHOLY_STORM] burst\n\n".format(spellTarget.description))
    spellTarget.float_text_line("Unholy Storm burst", tf_red)
    spellTarget.spell_damage(spellPacket.caster, D20DT_FIRE, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def unholyStormSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def unholyStormSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def unholyStormSpellSpellEnd(attachee, args, evt_obj):
    print "Unholy Storm SpellEnd"
    return 0

unholyStormSpell = PythonModifier("sp-Unholy Storm", 4) # spell_id, duration, empty, eventId
unholyStormSpell.AddHook(ET_OnConditionAdd, EK_NONE, unholyStormSpellOnConditionAdd, ())
unholyStormSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, unholyStormSpellOnEnteredAoe, ())
#unholyStormSpell.AddHook(ET_OnBeginRound, EK_NONE, unholyStormSpellOnBeginRound, ())
unholyStormSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, unholyStormSpellSpellEnd, ())
unholyStormSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, unholyStormSpellHasSpellActive, ())
unholyStormSpell.AddHook(ET_OnD20Signal, EK_S_Killed, unholyStormSpellKilled, ())
unholyStormSpell.AddSpellDispelCheckStandard()
unholyStormSpell.AddSpellTeleportPrepareStandard()
unholyStormSpell.AddSpellTeleportReconnectStandard()
unholyStormSpell.AddSpellCountdownStandardHook()
unholyStormSpell.AddAoESpellEndStandardHook()

### Begin Unholy Storm Effect ###

def unholyStormEffectOnBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellTarget = attachee
        neededAlignment = [ALIGNMENT_LAWFUL_GOOD, ALIGNMENT_NEUTRAL_GOOD, ALIGNMENT_CHAOTIC_GOOD]
        spellDamageDice = dice_new('1d6')
        
        if not spellTarget.stat_level_get(stat_alignment) in neededAlignment:
            return 0
        elif spellTarget.is_category_type(mc_type_outsider):
            spellDamageDice.number = 4
        else:
            spellDamageDice.number = 2
        game.create_history_freeform("{} is affected by ~Unholy Storm~[TAG_SPELLS_UNHOLY_STORM]\n\n".format(spellTarget.description))
        spellTarget.float_text_line("Unholy Storm", tf_red)
        spellTarget.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def unholyStormEffectSkillPenalty(attachee, args, evt_obj):
     evt_obj.bonus_list.add(-4, 160, "~Unholy Storm~[TAG_SPELLS_UNHOLY_STORM] Penalty") #Unholy Storm gives a -4 penalty on Listen, Search and Spot Checks
     return 0

def unholyStormEffectAttackPenalty(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(-4, 160, "~Unholy Storm~[TAG_SPELLS_UNHOLY_STORM] Penalty") #Unholy Storm gives a -4 penalty on ranged attacks made in, into, or out of the storm
    return 0

def unholyStormEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Unholy Storm ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Unholy Storm ({} rounds)".format(args.get_arg(1)))
    return 0

def unholyStormEffectEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("UNHOLY_STORM"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("UNHOLY_STORM"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def unholyStormEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    unholyStormEventId = args.get_arg(3)
    if unholyStormEventId != evt_obj.evt_id:
        print "ID Mismach"
        return 0
    args.condition_remove()
    return 0

def unholyStormEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def unholyStormEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def unholyStormEffectHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

unholyStormEffect = PythonModifier("Unholy Storm Effect", 4) #spell_id, duration, empty, eventId
unholyStormEffect.AddHook(ET_OnBeginRound, EK_NONE, unholyStormEffectOnBeginRound, ())
unholyStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, unholyStormEffectSkillPenalty, ())
unholyStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, unholyStormEffectSkillPenalty, ())
unholyStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, unholyStormEffectSkillPenalty, ())
unholyStormEffect.AddHook(ET_OnToHitBonus2, EK_NONE, unholyStormEffectAttackPenalty, ())
unholyStormEffect.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, unholyStormEffectAttackPenalty, ())
unholyStormEffect.AddHook(ET_OnGetTooltip, EK_NONE, unholyStormEffectTooltip, ())
unholyStormEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, unholyStormEffectEffectTooltip, ())
unholyStormEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, unholyStormEffectOnLeaveAoE, ())
unholyStormEffect.AddHook(ET_OnConditionRemove, EK_NONE, unholyStormEffectOnRemove, ())
unholyStormEffect.AddHook(ET_OnD20Signal, EK_S_Killed, unholyStormEffectSpellKilled, ())