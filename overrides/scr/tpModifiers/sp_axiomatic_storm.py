from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Axiomatic Storm"

def axiomaticStormSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    axiomaticStormPartsysId = game.particles('sp-Axiomatic Storm', attachee)
    spellPacket.add_spell_object(attachee, axiomaticStormPartsysId) # store the spell obj and the particle sys
    radiusAxiomaticStorm = 20.0
    axiomaticStormEventId = attachee.object_event_append(OLC_CRITTERS, radiusAxiomaticStorm)
    args.set_arg(3, axiomaticStormEventId)
    spellPacket.update_registry()
    return 0

def axiomaticStormSpellOnEnteredAoe(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    axiomaticStormEventId = args.get_arg(3)
    print "Axiomatic Storm enter: ", spellTarget

    if axiomaticStormEventId != evt_obj.evt_id:
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Axiomatic Storm Effect', args.get_arg(0), args.get_arg(1), 0, args.get_arg(3))
    return 0

def axiomaticStormSpellOnBeginRound(attachee, args, evt_obj):
    crittersInAoe = game.obj_list_cone(attachee, OLC_CRITTERS, 20, 0, 360)
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    neededAlignment = [ALIGNMENT_CHAOTIC_GOOD, ALIGNMENT_CHAOTIC_NEUTRAL, ALIGNMENT_CHAOTIC_EVIL]
    chaoticOutsiderInAoe = []
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 5
    
    for target in crittersInAoe:
        targetIsDead = target.d20_query(Q_Dead)
        if target.stat_level_get(stat_alignment) in neededAlignment:
            hasChaoticAlignment = True
        else:
            hasChaoticAlignment = False
        if target.is_category_type(mc_type_outsider):
            isOutsider = True
        else:
            isOutsider = False
        if not targetIsDead and hasChaoticAlignment and isOutsider:
            chaoticOutsiderInAoe.append(target)
    
    if not chaoticOutsiderInAoe:
        return 0
    
    numberOfTargets = len(chaoticOutsiderInAoe)
    randomDice = dice_new('1d{}'.format(numberOfTargets))
    selectTarget = randomDice.roll() - 1
    spellTarget = chaoticOutsiderInAoe[selectTarget]
    game.particles('sp-Axiomatic Storm-hit', spellTarget)
    game.create_history_freeform("{} is affected by ~Axiomatic Storm~[TAG_SPELLS_AXIOMATIC_STORM] burst\n\n".format(spellTarget.description))
    spellTarget.float_text_line("Axiomatic Storm burst", tf_red)
    spellTarget.spell_damage(spellPacket.caster, D20DT_ACID, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def axiomaticStormSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def axiomaticStormSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def axiomaticStormSpellSpellEnd(attachee, args, evt_obj):
    print "Axiomatic Storm SpellEnd"
    return 0

axiomaticStormSpell = PythonModifier("sp-Axiomatic Storm", 4) # spell_id, duration, empty, eventId
axiomaticStormSpell.AddHook(ET_OnConditionAdd, EK_NONE, axiomaticStormSpellOnConditionAdd, ())
axiomaticStormSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, axiomaticStormSpellOnEnteredAoe, ())
axiomaticStormSpell.AddHook(ET_OnBeginRound, EK_NONE, axiomaticStormSpellOnBeginRound, ())
axiomaticStormSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, axiomaticStormSpellSpellEnd, ())
axiomaticStormSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, axiomaticStormSpellHasSpellActive, ())
axiomaticStormSpell.AddHook(ET_OnD20Signal, EK_S_Killed, axiomaticStormSpellKilled, ())
axiomaticStormSpell.AddSpellDispelCheckStandard()
axiomaticStormSpell.AddSpellTeleportPrepareStandard()
axiomaticStormSpell.AddSpellTeleportReconnectStandard()
axiomaticStormSpell.AddSpellCountdownStandardHook()
axiomaticStormSpell.AddAoESpellEndStandardHook()

### Begin Axiomatic Storm Effect ###

def axiomaticStormEffectOnBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellTarget = attachee
        neededAlignment = [ALIGNMENT_CHAOTIC_GOOD, ALIGNMENT_CHAOTIC_NEUTRAL, ALIGNMENT_CHAOTIC_EVIL]
        spellDamageDice = dice_new('1d6')
        
        if not spellTarget.stat_level_get(stat_alignment) in neededAlignment:
            return 0
        elif spellTarget.is_category_type(mc_type_outsider):
            spellDamageDice.number = 4
        else:
            spellDamageDice.number = 2
        game.create_history_freeform("{} is affected by ~Axiomatic Storm~[TAG_SPELLS_AXIOMATIC_STORM]\n\n".format(spellTarget.description))
        spellTarget.float_text_line("Axiomatic Storm", tf_red)
        spellTarget.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def axiomaticStormEffectSkillPenalty(attachee, args, evt_obj):
     evt_obj.bonus_list.add(-4, 160, "~Axiomatic Storm~[TAG_SPELLS_AXIOMATIC_STORM] Penalty") #Axiomatic Storm gives a -4 penalty on Listen, Search and Spot Checks
     return 0

def axiomaticStormEffectAttackPenalty(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(-4, 160, "~Axiomatic Storm~[TAG_SPELLS_AXIOMATIC_STORM] Penalty") #Axiomatic Storm gives a -4 penalty on ranged attacks made in, into, or out of the storm
    return 0

def axiomaticStormEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Axiomatic Storm ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Axiomatic Storm ({} rounds)".format(args.get_arg(1)))
    return 0

def axiomaticStormEffectEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("AXIOMATIC_STORM"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("AXIOMATIC_STORM"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def axiomaticStormEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    axiomaticStormEventId = args.get_arg(3)
    if axiomaticStormEventId != evt_obj.evt_id:
        print "ID Mismach"
        return 0
    args.condition_remove()
    return 0

def axiomaticStormEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def axiomaticStormEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def axiomaticStormEffectHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

axiomaticStormEffect = PythonModifier("Axiomatic Storm Effect", 4) #spell_id, duration, empty, eventId
axiomaticStormEffect.AddHook(ET_OnBeginRound, EK_NONE, axiomaticStormEffectOnBeginRound, ())
axiomaticStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, axiomaticStormEffectSkillPenalty, ())
axiomaticStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, axiomaticStormEffectSkillPenalty, ())
axiomaticStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, axiomaticStormEffectSkillPenalty, ())
axiomaticStormEffect.AddHook(ET_OnToHitBonus2, EK_NONE, axiomaticStormEffectAttackPenalty, ())
axiomaticStormEffect.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, axiomaticStormEffectAttackPenalty, ())
axiomaticStormEffect.AddHook(ET_OnGetTooltip, EK_NONE, axiomaticStormEffectTooltip, ())
axiomaticStormEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, axiomaticStormEffectEffectTooltip, ())
axiomaticStormEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, axiomaticStormEffectOnLeaveAoE, ())
axiomaticStormEffect.AddHook(ET_OnConditionRemove, EK_NONE, axiomaticStormEffectOnRemove, ())
axiomaticStormEffect.AddHook(ET_OnD20Signal, EK_S_Killed, axiomaticStormEffectSpellKilled, ())