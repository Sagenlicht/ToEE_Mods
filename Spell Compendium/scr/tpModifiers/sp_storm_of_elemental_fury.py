from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Storm of Elemental Fury"

def stormOfElementalFurySpellOnConditionAdd(attachee, args, evt_obj):
    print "On Condition Add"
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    stormOfElementalFuryPartsysId = game.particles('sp-Storm of Elemental Fury Wind', attachee)
    args.set_arg(4, stormOfElementalFuryPartsysId)
    spellPacket.add_spell_object(attachee, 0)
    radiusStorm = 40.0
    stormOfElementalFuryEventId = attachee.object_event_append(OLC_CRITTERS, radiusStorm)
    args.set_arg(3, stormOfElementalFuryEventId)
    spellPacket.update_registry()
    return 0

def stormOfElementalFurySpellOnEnteredAoe(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    stormOfElementalFuryEventId = args.get_arg(3)

    if stormOfElementalFuryEventId != evt_obj.evt_id:
        print "Id Mismatch !!"
        return 0

    if spellPacket.add_target(spellTarget, 0):
       spellTarget.condition_add_with_args('Storm of Elemental Fury Wind', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    return 0

def stormOfElementalFurySpellOnBeginRound(attachee, args, evt_obj):
    print "Storm object begin round #: {}".format(args.get_arg(1))
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellParticles = args.get_arg(4)
    if args.get_arg(1) == 2:
        game.particles_kill(spellParticles)
        spellParticles = game.particles('sp-Storm of Elemental Fury Earth', attachee)
        args.set_arg(4, spellParticles)
    elif args.get_arg(1) == 1:
        game.particles_kill(spellParticles)
    elif args.get_arg(1) == 0:
        pass
    spellPacket.update_registry()
    print "End Begin Round"
    return 0

def stormOfElementalFurySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def stormOfElementalFurySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def stormOfElementalFurySpellSpellEnd(attachee, args, evt_obj):
    print "Storm of Elemental Fury SpellEnd"
    return 0

stormOfElementalFurySpell = PythonModifier("sp-Storm of Elemental Fury", 5) # spell_id, duration, spellDc, eventId, partsysId
stormOfElementalFurySpell.AddHook(ET_OnConditionAdd, EK_NONE, stormOfElementalFurySpellOnConditionAdd, ())
stormOfElementalFurySpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, stormOfElementalFurySpellOnEnteredAoe, ())
stormOfElementalFurySpell.AddHook(ET_OnBeginRound, EK_NONE, stormOfElementalFurySpellOnBeginRound, ())
stormOfElementalFurySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, stormOfElementalFurySpellSpellEnd, ())
stormOfElementalFurySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, stormOfElementalFurySpellHasSpellActive, ())
stormOfElementalFurySpell.AddHook(ET_OnD20Signal, EK_S_Killed, stormOfElementalFurySpellKilled, ())
stormOfElementalFurySpell.AddSpellDispelCheckStandard()
stormOfElementalFurySpell.AddSpellTeleportPrepareStandard()
stormOfElementalFurySpell.AddSpellTeleportReconnectStandard()
stormOfElementalFurySpell.AddSpellCountdownStandardHook()
stormOfElementalFurySpell.AddAoESpellEndStandardHook()


### Begin Storm of Elemental Fury Wind ###

def stormOfElementalFuryWindOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    size = attachee.get_size
    if size < 6:
        if attachee.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)):
            attachee.float_mesfile_line('mes\\spell.mes', 30001)
        else:
            attachee.float_mesfile_line('mes\\spell.mes', 30002)
            attachee.fall_down()
            attachee.condition_add("Prone")
    return 0

def stormOfElementalFuryWindOnBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    return 0

def stormOfElementalFuryWindSkillPenalty(attachee, args, evt_obj):
     evt_obj.bonus_list.add(-4, 160, "~Storm of Elemental Fury~[TAG_SPELLS_AXIOMATIC_STORM] Penalty") #Storm of Elemental Fury gives a -4 penalty on Listen, Search and Spot Checks
     return 0

def stormOfElementalFuryWindAttackPenalty(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(-4, 160, "~Storm of Elemental Fury~[TAG_SPELLS_AXIOMATIC_STORM] Penalty") #Storm of Elemental Fury gives a -4 penalty on ranged attacks made in, into, or out of the storm
    return 0

def stormOfElementalFuryWindTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Storm of Elemental Fury ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Storm of Elemental Fury ({} rounds)".format(args.get_arg(1)))
    return 0

def stormOfElementalFuryWindEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("STORM_OF_ELEMENTAL_FURY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("STORM_OF_ELEMENTAL_FURY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def stormOfElementalFuryWindOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    axiomaticStormEventId = args.get_arg(3)
    if axiomaticStormEventId != evt_obj.evt_id:
        print "ID Mismach"
        return 0
    args.condition_remove()
    return 0

def stormOfElementalFuryWindOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def stormOfElementalFuryWindSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def stormOfElementalFuryWindHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

stormOfElementalFuryWind = PythonModifier("Storm of Elemental Fury Wind", 4) #spell_id, duration, spellDc, eventId
stormOfElementalFuryWind.AddHook(ET_OnBeginRound, EK_NONE, stormOfElementalFuryWindOnConditionAdd, ())
stormOfElementalFuryWind.AddHook(ET_OnBeginRound, EK_NONE, stormOfElementalFuryWindOnBeginRound, ())
stormOfElementalFuryWind.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, stormOfElementalFuryWindSkillPenalty, ())
stormOfElementalFuryWind.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, stormOfElementalFuryWindSkillPenalty, ())
stormOfElementalFuryWind.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, stormOfElementalFuryWindSkillPenalty, ())
stormOfElementalFuryWind.AddHook(ET_OnToHitBonus2, EK_NONE, stormOfElementalFuryWindAttackPenalty, ())
stormOfElementalFuryWind.AddHook(ET_OnToHitBonusFromDefenderCondition, EK_NONE, stormOfElementalFuryWindAttackPenalty, ())
stormOfElementalFuryWind.AddHook(ET_OnGetTooltip, EK_NONE, stormOfElementalFuryWindTooltip, ())
stormOfElementalFuryWind.AddHook(ET_OnGetEffectTooltip, EK_NONE, stormOfElementalFuryWindEffectTooltip, ())
stormOfElementalFuryWind.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, stormOfElementalFuryWindOnLeaveAoE, ())
stormOfElementalFuryWind.AddHook(ET_OnConditionRemove, EK_NONE, stormOfElementalFuryWindOnRemove, ())
stormOfElementalFuryWind.AddHook(ET_OnD20Signal, EK_S_Killed, stormOfElementalFuryWindSpellKilled, ())