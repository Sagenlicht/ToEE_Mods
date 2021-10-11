from templeplus.pymod import PythonModifier
from __main__ import game
from toee import *
import tpdp
print "Registering Panicked Condition"

def panickedConditionAddActions(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(1))

    attacheeRacialImmunity = False
    immunityList = [mc_type_construct, mc_type_ooze, mc_type_plant, mc_type_undead, mc_type_vermin]
    for critterType in immunityList:
        if attachee.is_category_type(critterType):
            attacheeRacialImmunity = True

    if attacheeRacialImmunity:
        args.set_arg(3, 1)
        args.condition_remove()
        return 0

    attachee.float_text_line("Panicked", tf_red)
    game.create_history_freeform(attachee.description + " is ~panicked~[TAG_panicked]\n\n")
    game.particles('sp-fear', attachee) #attachee.obj.partsys_id
    if attachee.critter_flags_get() & OCF_NO_FLEE:
        attachee.critter_flag_unset(OCF_NO_FLEE)
        args.set_arg(2, 1)
    attachee.ai_flee_add(spellPacket.caster)
    
    if attachee.d20_query(Q_Critter_Is_Concentrating) == 1: #Panicked breaks concentration
        panickedConditionBreakConcentration(attachee)
    return 0

def panickedConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def panickedConditionPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-2,0,"~Panicked~[TAG_PANICKED] Penalty") #While Panicked target has a -2 penalty on saves and ability and skill checks
    return 0

def panickedConditionAoOPossible(attachee, args, evt_obj): #Can't AoO under Panicked condition
    evt_obj.return_val = 0
    return 0

def panickedConditionBreakConcentration(attachee):
    #tested this with Calm Emotions and Detect Magic. 
    #Calm Emtions is stopped being concentrated on and expires, but it breaks; no removal of particles and radial menu :(
    #Detect Magic has presumably no concentration flag but it should. Nothing happened to the spell when panicked condition kicked in.
    #Not sure if the hook is worth keeping due to this.
    attachee.d20_send_signal(S_Concentration_Broken) #Try if Remove_Concentration is better signal
    return 0

def panickedConditionAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def panickedConditionCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemovePanicked = [spell_heal, "Panacea", "Remove Nausea"] # Heal_enum=565; Panacea and Remove Nausea are currently not in the game
    if spellToCheck.spell_enum in spellsThatRemovePanicked:
        args.condition_remove()
    return 0

def panickedConditionGetTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append("Panicked (" + str(args.get_arg(0)) + " round)")
    else:
        evt_obj.append("Panicked (" + str(args.get_arg(0)) + " rounds)")

    return 0

def panickedConditionGetEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append(tpdp.hash("PANICKED"), -2, "(" + str(args.get_arg(0)) + " round)")
    else:
        evt_obj.append(tpdp.hash("PANICKED"), -2, "(" + str(args.get_arg(0)) + " rounds)")
    return 0

def panickedConditionRemoveCondition(attachee, args, evt_obj):
    if args.get_arg(3):
        attachee.float_text_line("Unaffected due to Racial Immunity")
    else:
        if args.get_arg(2):
            attachee.critter_flag_set(OCF_NO_FLEE)
        attachee.critter_flag_unset(OCF_FLEEING)
        game.create_history_freeform(attachee.description + " is no longer ~panicked~[TAG_panicked]\n\n")
    return 0

panickedCondition = PythonModifier("Panicked Condition", 4) #duration, passedSpellID, noFleeFlag, racialImmunity
panickedCondition.AddHook(ET_OnConditionAdd, EK_NONE, panickedConditionAddActions, ())
panickedCondition.AddHook(ET_OnBeginRound, EK_NONE, panickedConditionBeginRound, ())
panickedCondition.AddHook(ET_OnGetSkillLevel, EK_NONE, panickedConditionPenalty,())
panickedCondition.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, panickedConditionPenalty,())
panickedCondition.AddHook(ET_OnSaveThrowLevel, EK_NONE, panickedConditionPenalty,())
panickedCondition.AddHook(ET_OnD20Query, EK_Q_AOOPossible, panickedConditionAoOPossible, ())
panickedCondition.AddHook(ET_OnD20PythonQuery, "Panicked", panickedConditionAnswerToQuery, ()) #not tested
panickedCondition.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, panickedConditionCheckRemoveBySpell, ())
panickedCondition.AddHook(ET_OnConditionRemove, EK_NONE, panickedConditionRemoveCondition, ())
panickedCondition.AddHook(ET_OnGetTooltip, EK_NONE, panickedConditionGetTooltip, ())
panickedCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, panickedConditionGetEffectTooltip, ())
