from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Anarchic Storm"

def anarchicStormSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    anarchicStormPartsysId = game.particles('sp-Axiomatic Storm', attachee)
    spellPacket.add_spell_object(attachee, anarchicStormPartsysId) # store the spell obj and the particle sys
    radiusAxiomaticStorm = 20.0
    anarchicStormEventId = attachee.object_event_append(OLC_CRITTERS, radiusAxiomaticStorm)
    args.set_arg(3, anarchicStormEventId)
    spellPacket.update_registry()
    return 0

def anarchicStormSpellOnEnteredAoe(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    anarchicStormEventId = args.get_arg(3)
    print "Anarchic Storm enter: ", spellTarget

    if anarchicStormEventId != evt_obj.evt_id:
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Anarchic Storm Effect', args.get_arg(0), args.get_arg(1), 0, args.get_arg(3))
    return 0

def anarchicStormSpellOnBeginRound(attachee, args, evt_obj):
    crittersInAoe = game.obj_list_cone(attachee, OLC_CRITTERS, 20, 0, 360)
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    lawfulOutsiderInAoe = []
    spellDamageDice = dice_new('1d6')
    spellDamageDice.number = 5
    
    for target in crittersInAoe:
        targetIsDead = target.d20_query(Q_Dead)
        if target.critter_get_alignment() & ALIGNMENT_LAWFUL:
            hasLawfulAlignment = True
        else:
            hasLawfulAlignment = False
        if target.is_category_type(mc_type_outsider):
            isOutsider = True
        else:
            isOutsider = False
        if not targetIsDead and hasLawfulAlignment and isOutsider:
            lawfulOutsiderInAoe.append(target)
    
    if not lawfulOutsiderInAoe:
        return 0
    
    numberOfTargets = len(lawfulOutsiderInAoe)
    if numberOfTargets == 1:
        selectTarget = 0
    else:
        selectTarget = (game.random_range(0, numberOfTargets) -1)
    spellTarget = lawfulOutsiderInAoe[selectTarget]
    game.particles('sp-Axiomatic Storm-hit', spellTarget)
    game.create_history_freeform("{} is affected by ~Anarchic Storm~[TAG_SPELLS_ANARCHIC_STORM] burst\n\n".format(spellTarget.description))
    spellTarget.float_text_line("Anarchic Storm burst", tf_red)
    spellTarget.spell_damage(spellPacket.caster, D20DT_ELECTRICITY, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def anarchicStormSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def anarchicStormSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def anarchicStormSpellSpellEnd(attachee, args, evt_obj):
    print "Anarchic Storm SpellEnd"
    return 0

anarchicStormSpell = PythonModifier("sp-Anarchic Storm", 4) # spell_id, duration, empty, eventId
anarchicStormSpell.AddHook(ET_OnConditionAdd, EK_NONE, anarchicStormSpellOnConditionAdd, ())
anarchicStormSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, anarchicStormSpellOnEnteredAoe, ())
anarchicStormSpell.AddHook(ET_OnBeginRound, EK_NONE, anarchicStormSpellOnBeginRound, ())
anarchicStormSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, anarchicStormSpellSpellEnd, ())
anarchicStormSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, anarchicStormSpellHasSpellActive, ())
anarchicStormSpell.AddHook(ET_OnD20Signal, EK_S_Killed, anarchicStormSpellKilled, ())
anarchicStormSpell.AddSpellDispelCheckStandard()
anarchicStormSpell.AddSpellTeleportPrepareStandard()
anarchicStormSpell.AddSpellTeleportReconnectStandard()
anarchicStormSpell.AddSpellCountdownStandardHook()
anarchicStormSpell.AddAoESpellEndStandardHook()

### Begin Anarchic Storm Effect ###

def anarchicStormEffectOnBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellTarget = attachee
        spellDamageDice = dice_new('1d6')
        
        if not spellTarget.critter_get_alignment() & ALIGNMENT_LAWFUL:
            return 0
        elif spellTarget.is_category_type(mc_type_outsider):
            spellDamageDice.number = 4
        else:
            spellDamageDice.number = 2
        game.create_history_freeform("{} is affected by ~Anarchic Storm~[TAG_SPELLS_ANARCHIC_STORM]\n\n".format(spellTarget.description))
        spellTarget.float_text_line("Anarchic Storm", tf_red)
        spellTarget.spell_damage(spellPacket.caster, D20DT_MAGIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
    return 0

def anarchicStormEffectSkillPenalty(attachee, args, evt_obj):
     evt_obj.bonus_list.add(-4, 160, "~Anarchic Storm~[TAG_SPELLS_ANARCHIC_STORM] Penalty") #Anarchic Storm gives a -4 penalty on Listen, Search and Spot Checks
     return 0

def anarchicStormEffectAttackPenalty(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(-4, 160, "~Anarchic Storm~[TAG_SPELLS_ANARCHIC_STORM] Penalty") #Anarchic Storm gives a -4 penalty on ranged attacks made in, into, or out of the storm
    return 0

def anarchicStormEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Anarchic Storm ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Anarchic Storm ({} rounds)".format(args.get_arg(1)))
    return 0

def anarchicStormEffectEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("ANARCHIC_STORM"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("ANARCHIC_STORM"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def anarchicStormEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    anarchicStormEventId = args.get_arg(3)
    if anarchicStormEventId != evt_obj.evt_id:
        print "ID Mismach"
        return 0
    args.condition_remove()
    return 0

def anarchicStormEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def anarchicStormEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def anarchicStormEffectHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

anarchicStormEffect = PythonModifier("Anarchic Storm Effect", 4) #spell_id, duration, empty, eventId
anarchicStormEffect.AddHook(ET_OnBeginRound, EK_NONE, anarchicStormEffectOnBeginRound, ())
anarchicStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, anarchicStormEffectSkillPenalty, ())
anarchicStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, anarchicStormEffectSkillPenalty, ())
anarchicStormEffect.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, anarchicStormEffectSkillPenalty, ())
anarchicStormEffect.AddHook(ET_OnToHitBonus2, EK_NONE, anarchicStormEffectAttackPenalty, ())
anarchicStormEffect.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, anarchicStormEffectAttackPenalty, ())
anarchicStormEffect.AddHook(ET_OnGetTooltip, EK_NONE, anarchicStormEffectTooltip, ())
anarchicStormEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, anarchicStormEffectEffectTooltip, ())
anarchicStormEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, anarchicStormEffectOnLeaveAoE, ())
anarchicStormEffect.AddHook(ET_OnConditionRemove, EK_NONE, anarchicStormEffectOnRemove, ())
anarchicStormEffect.AddHook(ET_OnD20Signal, EK_S_Killed, anarchicStormEffectSpellKilled, ())