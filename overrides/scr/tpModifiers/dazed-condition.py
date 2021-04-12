from templeplus.pymod import PythonModifier
from __main__ import game
from toee import *
import tpdp
print "Registering Dazed Condition"

def dazedConditionAddActions(attachee, args, evt_obj):
    attachee.float_text_line("Dazed", tf_red)
    game.create_history_freeform(attachee.description + " is ~Dazed~[TAG_DAZED]\n\n")
    dazedPartsysId = game.particles('sp-Daze', attachee) #attachee.obj.partsys_id
    args.set_arg(1, dazedPartsysId)
    if attachee.d20_query(Q_Critter_Is_Concentrating) == 1: #Dazed breaks concentration
        dazedConditionBreakConcentration(attachee)
    return 0

def dazedConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def dazedConditionTurnBasedStatusInit(attachee, args, evt_obj):
    if evt_obj.tb_status.hourglass_state > 0:
        evt_obj.tb_status.hourglass_state = 0 # Dazed target can't act.
    return 0

def dazedConditionAoOPossible(attachee, args, evt_obj): #Can't AoO under Dazed Condition
    evt_obj.return_val = 0
    return 0

def dazedConditionCannotCast(attachee, args, evt_obj): # Dazed prohibits casting
    evt_obj.return_val = 1
    return 0

def dazedConditionBreakConcentration(attachee):
    #tested this with Calm Emotions and Detect Magic. 
    #Calm Emtions is stopped being concentrated on and expires, but it breaks; no removal of particles and radial menu :(
    #Detect Magic has presumably no concentration flag but it should. Nothing happened to the spell when Dazed Condition kicked in.
    #Not sure if the hook is worth keeping due to this.
    attachee.d20_send_signal(S_Concentration_Broken) #Try if Remove_Concentration is better signal
    return 0

def dazedConditionAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def dazedConditionCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if heal spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemoveDazed = [565, "Panacea", "Remove Nausea"] # Heal_enum=565; Panacea and Remove Nausea are currently not in the game
    if spellToCheck.spell_enum in spellsThatRemoveDazed:
        args.condition_remove()
    return 0

def dazedConditionGetTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append("Dazed (" + str(args.get_arg(0)) + " round)")
    else:
        evt_obj.append("Dazed (" + str(args.get_arg(0)) + " rounds)")

    return 0

def dazedConditionGetEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append(tpdp.hash("DAZED_CONDITION"), -2, "(" + str(args.get_arg(0)) + " round)")
    else:
        evt_obj.append(tpdp.hash("DAZED_CONDITION"), -2, "(" + str(args.get_arg(0)) + " rounds)")
    return 0

def dazedConditionRemoveCondition(attachee, args, evt_obj):
    game.particles_end(args.get_arg(1))
    if attachee.stat_level_get(stat_hp_current) > -10:
        attachee.float_text_line("No longer Dazed")
        game.create_history_freeform(attachee.description + " is no longer ~Dazed~[TAG_DAZED]\n\n")
    return 0

dazedCondition = PythonModifier("Dazed Condition", 2) #duration, partsys_id
dazedCondition.AddHook(ET_OnConditionAdd, EK_NONE, dazedConditionAddActions, ())
dazedCondition.AddHook(ET_OnTurnBasedStatusInit, EK_NONE, dazedConditionTurnBasedStatusInit, ())
dazedCondition.AddHook(ET_OnBeginRound, EK_NONE, dazedConditionBeginRound, ())
dazedCondition.AddHook(ET_OnD20Query, EK_Q_CannotCast, dazedConditionCannotCast, ())
dazedCondition.AddHook(ET_OnD20Query, EK_Q_AOOPossible, dazedConditionAoOPossible, ())
dazedCondition.AddHook(ET_OnD20PythonQuery, "Dazed", dazedConditionAnswerToQuery, ()) #not tested
dazedCondition.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, dazedConditionCheckRemoveBySpell, ())
dazedCondition.AddHook(ET_OnConditionRemove, EK_NONE, dazedConditionRemoveCondition, ())
dazedCondition.AddHook(ET_OnGetTooltip, EK_NONE, dazedConditionGetTooltip, ())
dazedCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, dazedConditionGetEffectTooltip, ())
