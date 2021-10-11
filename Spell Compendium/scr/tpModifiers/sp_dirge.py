from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Dirge"

def dirgeSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    dirgePartsysId = game.particles('sp-Dirge', attachee)
    spellPacket.add_spell_object(attachee, dirgePartsysId) # store the spell obj and the particle sys
    radiusDirge = 50.0
    dirgeEventId = attachee.object_event_append(OLC_CRITTERS, radiusDirge)
    args.set_arg(3, dirgeEventId)
    spellPacket.update_registry()
    return 0

def dirgeSpellOnEntered(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellCaster = spellPacket.caster
    spellTarget = evt_obj.target
    dirgeEventId = args.get_arg(3)
    print "Dirge enter: ",  spellTarget

    if dirgeEventId != evt_obj.evt_id:
        return 0

    if spellTarget.is_friendly(spellCaster):
        return 0

    if spellPacket.check_spell_resistance(spellTarget):
        print "Spell Resistance"
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Dirge Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    return 0


def dirgeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def dirgeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def dirgeSpellSpellEnd(attachee, args, evt_obj):
    print "Dirge SpellEnd"
    #spellPacket = tpdp.SpellPacket(args.get_arg(0))
    #spellPacket.end_target_particles(attachee) <--- does not work
    #args.remove_spell_mod() #remove_spell crashes the game
    #attachee.destroy()
    return 0

dirgeSpell = PythonModifier("sp-Dirge", 4) # spell_id, duration, spellDc, eventId
dirgeSpell.AddHook(ET_OnConditionAdd, EK_NONE, dirgeSpellOnConditionAdd,())
dirgeSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, dirgeSpellOnEntered, ())
dirgeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, dirgeSpellSpellEnd, ())
dirgeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, dirgeSpellHasSpellActive, ())
dirgeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, dirgeSpellKilled, ())
dirgeSpell.AddSpellDispelCheckStandard()
dirgeSpell.AddSpellTeleportPrepareStandard()
dirgeSpell.AddSpellTeleportReconnectStandard()
dirgeSpell.AddSpellCountdownStandardHook()
dirgeSpell.AddAoESpellEndStandardHook()

### Start Dirge Effect ###

def dirgeConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellCaster = spellPacket.caster

        attachee.float_text_line("Dirge", tf_red)
        game.create_history_freeform("Save versus ~Dirge~[TAG_SPELLS_Dirge]:\n\n")
        if attachee.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)):
            attachee.float_mesfile_line('mes\\spell.mes', 30001)
        else:
            attachee.float_mesfile_line('mes\\spell.mes', 30002)
            attacheePartsysId = game.particles('sp-Poison', attachee)
            attachee.condition_add_with_args('Temp_Ability_Loss', stat_strength, 2)
            attachee.condition_add_with_args('Temp_Ability_Loss', stat_dexterity, 2)
            game.create_history_freeform("{} Abilities damaged\n\n".format(attachee.description))
    return 0

def dirgeConditionTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Dirge ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Dirge ({} rounds)".format(args.get_arg(1)))
    return 0

def dirgeConditionEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DIRGE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DIRGE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def dirgeConditionSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def dirgeConditionOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    dirgeEventId = args.get_arg(3)
    if dirgeEventId != evt_obj.evt_id:
        print "ID Mismach Dirge"
        return 0
    args.condition_remove()
    return 0

def dirgeConditionOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

dirgeCondition = PythonModifier("Dirge Effect", 4) #spell_id, duration, spellDc, eventId
dirgeCondition.AddHook(ET_OnBeginRound, EK_NONE, dirgeConditionBeginRound, ())
dirgeCondition.AddHook(ET_OnGetTooltip, EK_NONE, dirgeConditionTooltip, ())
dirgeCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, dirgeConditionEffectTooltip, ())
dirgeCondition.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, dirgeConditionOnLeaveAoE, ())
dirgeCondition.AddHook(ET_OnConditionRemove, EK_NONE, dirgeConditionOnRemove, ())
dirgeCondition.AddHook(ET_OnD20Signal, EK_S_Killed, dirgeConditionSpellKilled, ())

## End Dirge Effect ###
