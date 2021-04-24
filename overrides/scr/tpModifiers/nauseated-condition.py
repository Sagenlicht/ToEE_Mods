from templeplus.pymod import PythonModifier
from __main__ import game
from toee import *
import tpdp
print "Registering Nauseated Condition"

def nauseatedConditionAddPreActions(attachee, args, evt_obj):
    if evt_obj.is_modifier("Nauseated Condition"):
        duration = args.get_arg(0)
        duration += 1
        args.set_arg(0, duration)
        evt_obj.return_val = 0
    return 0

def nauseatedConditionAddActions(attachee, args, evt_obj):
    #check if immune to nauseated
    if attachee.is_category_type(mc_type_undead) or attachee.is_category_type(mc_type_construct):
        args.set_arg(1, 1)
        args.condition_remove()
        return 0
    attachee.float_text_line("Nauseated", tf_red)
    game.create_history_freeform(attachee.description + " is ~nauseated~[TAG_NAUSEATED]\n\n")
    game.particles('sp-Poison', attachee)
    if attachee.d20_query(Q_Critter_Is_Concentrating) == 1: #Nauseated breaks concentration
        attachee.d20_send_signal(S_Remove_Concentration)
    return 0

def nauseatedConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def nauseatedConditionTurnBasedStatusInit(attachee, args, evt_obj):
    if evt_obj.tb_status.hourglass_state > 1:
        evt_obj.tb_status.hourglass_state = 1 # Nauseated condition limits to a single Move Action only
    return 0

def nauseatedConditionAoOPossible(attachee, args, evt_obj): #Can't AoO under Nauseated condition
    evt_obj.return_val = 0
    return 0

def nauseatedConditionCannotCast(attachee, args, evt_obj): # Nauseated prohibits casting
    evt_obj.return_val = 1
    return 0

def nauseatedConditionAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def nauseatedConditionCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if heal spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemoveNauseated = [spell_heal, "Panacea", "Remove Nausea"] # Heal_enum=565; Panacea and Remove Nausea are currently not in the game
    if spellToCheck.spell_enum in spellsThatRemoveNauseated:
        args.condition_remove()
    return 0

def nauseatedConditionRemoveCondition(attachee, args, evt_obj):
    if args.get_arg(1):
        attachee.float_text_line("Unaffected due to Racial Immunity")
    else:
        if attachee.stat_level_get(stat_hp_current) > -10: # Is there really no better way to check if a critter is dead?
            attachee.float_text_line("No longer nauseated")
            game.create_history_freeform("{} is no longer ~nauseated~[TAG_NAUSEATED]\n\n".format(attachee.description))
    return 0

def nauseatedConditionGetTooltip(attachee, args, evt_obj):
    if args.get_arg(2):
        evt_obj.append("Nauseated")
        return 0
    if args.get_arg(0) == 1:
        evt_obj.append("Nauseated ({} round)".format(args.get_arg(0)))
    else:
        evt_obj.append("Nauseated ({} rounds)".format(args.get_arg(0)))

    return 0

def nauseatedConditionGetEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append(tpdp.hash("NAUSEATED"), -2, " ({} round)".format(args.get_arg(0)))
    else:
        evt_obj.append(tpdp.hash("NAUSEATED"), -2, " ({} rounds)".format(args.get_arg(0)))
    return 0

nauseatedCondition = PythonModifier("Nauseated Condition", 2, False) #duration, immunityFlag
nauseatedCondition.AddHook(ET_OnConditionAddPre, EK_NONE, nauseatedConditionAddPreActions, ())
nauseatedCondition.AddHook(ET_OnConditionAdd, EK_NONE, nauseatedConditionAddActions, ())
nauseatedCondition.AddHook(ET_OnTurnBasedStatusInit, EK_NONE, nauseatedConditionTurnBasedStatusInit, ())
nauseatedCondition.AddHook(ET_OnBeginRound, EK_NONE, nauseatedConditionBeginRound, ())
nauseatedCondition.AddHook(ET_OnD20Query, EK_Q_CannotCast, nauseatedConditionCannotCast, ())
nauseatedCondition.AddHook(ET_OnD20Query, EK_Q_AOOPossible, nauseatedConditionAoOPossible, ())
nauseatedCondition.AddHook(ET_OnD20PythonQuery, "Nauseated Condition", nauseatedConditionAnswerToQuery, ())
nauseatedCondition.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, nauseatedConditionCheckRemoveBySpell, ())
nauseatedCondition.AddHook(ET_OnConditionRemove, EK_NONE, nauseatedConditionRemoveCondition, ())
nauseatedCondition.AddHook(ET_OnGetTooltip, EK_NONE, nauseatedConditionGetTooltip, ())
nauseatedCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, nauseatedConditionGetEffectTooltip, ())
