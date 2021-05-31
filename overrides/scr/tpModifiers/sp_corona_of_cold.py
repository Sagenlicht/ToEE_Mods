from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Corona of Cold"

def coronaOfColdSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    radiusCoronaOfCold = (10.0 + (attachee.radius / 12.0))
    coronaOfColdId = attachee.object_event_append(OLC_CRITTERS, radiusCoronaOfCold)
    args.set_arg(3, coronaOfColdId)
    spellPacket.update_registry()
    return 0

def coronaOfColdSpellOnEntered(attachee, args, evt_obj):
    print "Hook AoE"
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellTarget = evt_obj.target
    coronaOfColdId = args.get_arg(3)

    if coronaOfColdId != evt_obj.evt_id:
        print "ID Mismatch: Returned ID: {}, expected ID: {}".format(args.get_arg(3), evt_obj.evt_id)
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Corona of Cold Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3), 0)
    return 0

def coronaOfColdSpellFireResistance(attachee, args, evt_obj):
    evt_obj.damage_packet.add_damage_resistance(10, D20DT_FIRE, 1011) #Corona of Cold grants 10 Fire Resistance
    return 0

coronaOfColdSpell = PythonModifier("sp-Corona of Cold", 4) # spell_id, duration, spell_dc, eventID
coronaOfColdSpell.AddHook(ET_OnTakingDamage, EK_NONE, coronaOfColdSpellFireResistance, ())
coronaOfColdSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, coronaOfColdSpellOnEntered, ())
coronaOfColdSpell.AddHook(ET_OnConditionAdd, EK_NONE, coronaOfColdSpellOnConditionAdd,())
coronaOfColdSpell.AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addDimiss, ())
coronaOfColdSpell.AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, spell_utils.checkRemoveSpell, ())
coronaOfColdSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
coronaOfColdSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
coronaOfColdSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
coronaOfColdSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
coronaOfColdSpell.AddSpellDispelCheckStandard()
coronaOfColdSpell.AddSpellTeleportPrepareStandard()
coronaOfColdSpell.AddSpellTeleportReconnectStandard()
coronaOfColdSpell.AddSpellCountdownStandardHook()

### Start Corona of Cold Effect ###

def coronaOfColdEffectBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        game.create_history_freeform("{} is affected by ~Corona of Cold~[TAG_SPELLS_CORONA_OF_COLD]\n\n".format(attachee.description))
        #Saving Throw to negate damage
        if attachee.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): #success
            attachee.float_text_line("Corona of Cold saved")
            game.create_history_freeform("{} saves\n\n".format(attachee.description))
        else:
            attachee.float_text_line("Corona of Cold damage")
            spellDamageDice = dice_new('1d12')
            attachee.spell_damage(spellPacket.caster, D20DT_COLD, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
            if not args.get_arg(4): #if not already affected by shiver affect, activate it
                game.create_history_freeform("{} starts to shiver!\n\n".format(attachee.description))
                args.set_arg(4, 1)
    return 0

def coronaOfColdEffectAbilityPenalty(attachee, args, evt_obj):
    if args.get_arg(4):
        evt_obj.bonus_list.add(-2, 0,"~Corona of Cold~[TAG_SPELLS_CORONA_OF_COLD] Penalty") #Corona of Cold gives a -2 penalty to Strength and Dexterity on a failed save
    return 0

def coronaOfColdEffectMovementPenalty(attachee, args, evt_obj):
    if args.get_arg(4):
        moveSpeedBase = attachee.stat_level_get(stat_movement_speed)
        evt_obj.bonus_list.add(-(moveSpeedBase/2), 0 ,"~Corona of Cold~[TAG_SPELLS_CORONA_OF_COLD] Penalty") #Corona of Cold halfs movement speed on a failed save
        #newSpeed = evt_obj.bonus_list.get_sum()
        #if newSpeed < 5:
        #    speedToAdd = 5 - newSpeed
        #    evt_obj.bonus_list.add(speedToAdd, 0, "~Corona of Cold~[TAG_SPELLS_CORONA_OF_COLD] reduces to a minimum of 5 speed")
    return 0

def coronaOfColdEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Corona of Cold ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Corona of Cold ({} rounds)".format(args.get_arg(1)))
    return 0

def coronaOfColdEffectEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CORONA_OF_COLD"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CORONA_OF_COLD"), -2, " ({} rounds)".format(args.get_arg(1)))
    if args.get_arg(4):
        if args.get_arg(1) == 1:
            evt_obj.append(tpdp.hash("CORONA_OF_COLD_ABILITY"), -2, " ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append(tpdp.hash("CORONA_OF_COLD_ABILITY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def coronaOfColdEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def coronaOfColdEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    coronaOfColdId = args.get_arg(3)
    if coronaOfColdId != evt_obj.evt_id:
        print "ID Mismach Corona of Cold"
        return 0
    args.condition_remove()
    return 0

def coronaOfColdEffectDismissed(attachee, args, evt_obj):
    if evt_obj.data1 == args.get_arg(0):
        args.condition_remove()
    return 0


def coronaOfColdEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

coronaOfColdEffect = PythonModifier("Corona of Cold Effect", 5) #spell_id, duration, spell_dc, eventId, failedSave
coronaOfColdEffect.AddHook(ET_OnBeginRound, EK_NONE, coronaOfColdEffectBeginRound, ())
coronaOfColdEffect.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, coronaOfColdEffectAbilityPenalty,())
coronaOfColdEffect.AddHook(ET_OnAbilityScoreLevel, EK_STAT_STRENGTH, coronaOfColdEffectAbilityPenalty,())
coronaOfColdEffect.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, coronaOfColdEffectMovementPenalty,())
coronaOfColdEffect.AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, coronaOfColdEffectDismissed, ())
coronaOfColdEffect.AddHook(ET_OnGetTooltip, EK_NONE, coronaOfColdEffectTooltip, ())
coronaOfColdEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, coronaOfColdEffectEffectTooltip, ())
coronaOfColdEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, coronaOfColdEffectOnLeaveAoE, ())
coronaOfColdEffect.AddHook(ET_OnConditionRemove, EK_NONE, coronaOfColdEffectOnRemove, ())
