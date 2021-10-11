from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Fugue"

def fugueSpellOnConditionAdd(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    fuguePartsysId = game.particles( 'sp-Fugue', attachee)
    spellPacket.add_spell_object(attachee, fuguePartsysId) # store the spell obj and the particle sys
    radiusFugue = 30.0
    fugueEventId = attachee.object_event_append(OLC_CRITTERS, radiusFugue)
    args.set_arg(3, fugueEventId)
    spellPacket.update_registry()
    spellPacket.caster.condition_add_with_args('sp-Concentrating', args.get_arg(0))
    return 0

def fugueSpellOnEntered(attachee, args, evt_obj):
    print "Fugue enter"
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellTarget = evt_obj.target
    fugueEventId = args.get_arg(3)

    if fugueEventId != evt_obj.evt_id:
        print"Mismach ID Fugue"
        return 0

    if spellTarget == spellPacket.caster:
        return 0

    if spellPacket.check_spell_resistance(spellTarget):
        print "Spell Resistance"
        return 0

    if spellPacket.add_target(spellTarget, 0):
        if spellTarget.saving_throw_spell(args.get_arg(2), D20_Save_Fortitude, D20STD_F_NONE, spellPacket.caster, args.get_arg(0)): # save to be only disorientated condition
            spellTarget.float_mesfile_line('mes\\spell.mes', 30001)
            spellTarget.condition_add_with_args('Fugue Disoriented', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
        else:
            spellTarget.float_mesfile_line('mes\\spell.mes', 30002)
            spellTarget.condition_add_with_args('Fugue Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    return 0

def fugueSpellConcentrationBroken(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.spell_enum == 0:
        return 0
    attachee.d20_send_signal(S_Spell_End, args.get_arg(0))
    return 0

def fugueSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def fugueSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def fugueSpellSpellEnd(attachee, args, evt_obj):
    print "Fugue SpellEnd"
    return 0

fugueSpell = PythonModifier("sp-Fugue", 4) # spell_id, duration, spellDc, eventId
fugueSpell.AddHook(ET_OnConditionAdd, EK_NONE, fugueSpellOnConditionAdd,())
fugueSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, fugueSpellOnEntered, ())
fugueSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, fugueSpellConcentrationBroken, ())
fugueSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, fugueSpellSpellEnd, ())
fugueSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, fugueSpellHasSpellActive, ())
fugueSpell.AddHook(ET_OnD20Signal, EK_S_Killed, fugueSpellKilled, ())
fugueSpell.AddSpellDispelCheckStandard()
fugueSpell.AddSpellTeleportPrepareStandard()
fugueSpell.AddSpellTeleportReconnectStandard()
fugueSpell.AddSpellCountdownStandardHook()
fugueSpell.AddAoESpellEndStandardHook()

### Start Fugue Effect ###

def fugueConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    else:
        spellPacket = tpdp.SpellPacket(args.get_arg(0))
        spellCaster = spellPacket.caster
        spellCasterPerformSkill = spellCaster.skill_level_get(skill_perform)
        skillDice = dice_new('1d20')
        skillDiceRoll = skillDice.roll()
        skillRollResult = skillDiceRoll + spellCasterPerformSkill
        print "Perform Check Result", skillRollResult

        game.create_history_freeform("~Fugue~[TAG_SPELLS_FUGUE] effect:\n\n")
        if skillRollResult < 15:
            attachee.float_text_line("Fugue nothing happened")
            game.create_history_freeform("Nothing happened")
        elif skillRollResult in range(15, 20):
            spellDamageDice = dice_new('1d6')
            spellDamageDice.number = 3
            attachee.spell_damage(spellCaster, D20DT_SUBDUAL, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
        elif skillRollResult in range(20, 25):
            spellDamageDice = dice_new('1d6')
            spellDamageDice.number = 3
            attachee.spell_damage(spellCaster, D20DT_SONIC, spellDamageDice, D20DAP_UNSPECIFIED, D20A_CAST_SPELL, args.get_arg(0))
        elif skillRollResult in range(25, 30):
            attachee.fall_down()
            attachee.condition_add("Prone")
            attachee.float_mesfile_line('mes\\combat.mes', 18, 1) #ID18: Knockdown message
            game.create_history_freeform("{} is knocked ~prone~[TAG_PRONE]\n\n".format(attachee.description))
        elif skillRollResult in range(30, 35):
            queryForNausea = attachee.d20_query("Nauseated Condition")
            if queryForNausea:
                attachee.float_text_line("Nauseated", tf_red)
                game.create_history_freeform("{} is ~nauseated~[TAG_NAUSEATED]\n\n".format(attachee.description))
            attachee.condition_add_with_args('Nauseated Condition', 1, 0, 0)
        #elif skillRollResult in range(35, 40):
        else:
            attachee.float_text_line("Stunned", tf_red)
            attachee.condition_add_with_args('Stunned', 1, 0)
            attacheePartsysId = game.particles('sp-Daze2', attachee)
            game.create_history_freeform("{} is ~stunned~[TAG_STUNNED]\n\n".format(attachee.description))
        #else:
        #    threateningTargets = game.obj_list_cone(attachee, OLC_CRITTERS, 5, 0, 360)
        #    print "Targets 1: ", threateningTargets
        #    if len(threateningTargets) == 0:
        #        noTargetsToAttack = True
        #   else:
        #        possibleTargets = []
        #        for target in threateningTargets:
        #            if target.is_friendly(attachee):
        #                if not target == attachee:
        #                    print "Target to add: ", target
        #                    possibleTargets.append(target)
        #                    print "target added"
        #    print "Targets 2: ", possibleTargets
        #    if len(possibleTargets) == 0:
        #        noTargetsToAttack = True
        #    else:
        #        noTargetsToAttack = False
        #    
        #    if noTargetsToAttack:
        #        attachee.float_text_line("Stunned", tf_red)
        #        attachee.condition_add_with_args('Stunned', 1, 0)
        #        attacheePartsysId = game.particles('sp-Daze2', attachee)
        #        game.create_history_freeform(attachee.description + " is ~stunned~[TAG_STUNNED]\n\n")
        #    else:
        #        print "lets Attack"
        #        targetToAttack = possibleTargets[0]
        #        print "target To Attack: ", targetToAttack
        #        attachee.attack(targetToAttack, )
    return 0

def fugueConditionAnswerToQueries(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def fugueConditionTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Fugue ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Fugue ({} rounds)".format(args.get_arg(1)))
    return 0

def fugueConditionEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FUGUE_EFFECT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FUGUE_EFFECT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def fugueConditionSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def fugueConditionOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    fugueEventId = args.get_arg(3)
    if fugueEventId != evt_obj.evt_id:
        return 0
    args.condition_remove()
    return 0

def fugueConditionOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def fugueConditionEnd(attachee, args, evt_obj):
    print "Deafening Condition SpellEnd"
    spellId = args.get_arg(0)
    if evt_obj.data1 == spellId:
        #args.remove_spell_mod() # does a .condition_remove() with some safety checks
        args.condition_remove()
    return 0


fugueCondition = PythonModifier("Fugue Effect", 4) #spell_id, duration, spellDc, eventId
fugueCondition.AddHook(ET_OnBeginRound, EK_NONE, fugueConditionBeginRound, ())
fugueCondition.AddHook(ET_OnGetTooltip, EK_NONE, fugueConditionTooltip, ())
fugueCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, fugueConditionEffectTooltip, ())
fugueCondition.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, fugueConditionOnLeaveAoE, ())
fugueCondition.AddHook(ET_OnConditionRemove, EK_NONE, fugueConditionOnRemove, ())
fugueCondition.AddHook(ET_OnD20Signal, EK_S_Killed, fugueConditionSpellKilled, ())
fugueCondition.AddHook(ET_OnD20Signal, EK_S_Spell_End, fugueConditionEnd, ())
fugueCondition.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, fugueConditionEnd, ())

### End Fugue Effect ###

### Start Fugue Disoriented ###

def fugueDisorientedBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    return 0

def fugueDisorientedPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-2 , 0,"~Fugue~[TAG_SPELLS_FUGUE] Disorientation Penalty")
    return 0

def fugueDisorientedTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Disoriented ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Disoriented ({} rounds)".format(args.get_arg(1)))
    return 0

def fugueDisorientedEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FUGUE_DISORIENTED"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FUGUE_DISORIENTED"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def fugueDisorientedSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def fugueDisorientedOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    fugueEventId = args.get_arg(3)
    if fugueEventId != evt_obj.evt_id:
        return 0
    args.condition_remove()
    return 0

def fugueDisorientedOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

def fugueDisorientedEnd(attachee, args, evt_obj):
    print "Deafening Condition SpellEnd"
    spellId = args.get_arg(0)
    if evt_obj.data1 == spellId:
        #args.remove_spell_mod() # does a .condition_remove() with some safety checks
        args.condition_remove()
    return 0

fugueDisoriented = PythonModifier("Fugue Disoriented", 4) #spell_id, duration, spellDc, eventId
fugueDisoriented.AddHook(ET_OnBeginRound, EK_NONE, fugueDisorientedBeginRound, ())
fugueDisoriented.AddHook(ET_OnToHitBonus2, EK_NONE, fugueDisorientedPenalty,())
fugueDisoriented.AddHook(ET_OnGetSkillLevel, EK_NONE, fugueDisorientedPenalty,())
fugueDisoriented.AddHook(ET_OnGetTooltip, EK_NONE, fugueDisorientedTooltip, ())
fugueDisoriented.AddHook(ET_OnGetEffectTooltip, EK_NONE, fugueDisorientedEffectTooltip, ())
fugueDisoriented.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, fugueDisorientedOnLeaveAoE, ())
fugueDisoriented.AddHook(ET_OnConditionRemove, EK_NONE, fugueDisorientedOnRemove, ())
fugueDisoriented.AddHook(ET_OnD20Signal, EK_S_Killed, fugueDisorientedSpellKilled, ())
fugueDisoriented.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, fugueDisorientedEnd, ())
