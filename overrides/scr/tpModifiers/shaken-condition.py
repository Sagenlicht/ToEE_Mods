from templeplus.pymod import PythonModifier
from __main__ import game
from toee import *
import tpdp
print "Registering Shaken Condition"

def shakenConditionAddActions(attachee, args, evt_obj):
    #check if immune to Shaken
    attacheeRacialImmunity = False
    immunityList = [mc_type_construct, mc_type_ooze, mc_type_plant, mc_type_undead, mc_type_vermin]
    for critterType in immunityList:
        if attachee.is_category_type(critterType):
            attacheeRacialImmunity = True

    if attacheeRacialImmunity:
        args.set_arg(3, 1)
        args.condition_remove()
        return 0
        
    attachee.float_text_line("Shaken", tf_red)
    game.create_history_freeform(attachee.description + " is ~Shaken~[TAG_Shaken]\n\n")
    return 0

def shakenConditionBeginRound(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def shakenConditionPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-2,0,"~Shaken~[TAG_SHAKEN] Penalty") #Shaken is a -2 penalty to attack and weapon damage rolls, saving throws and skill and ability checks.
    return 0

# weapon damage penalty missing

def shakenConditionAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def shakenConditionCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if heal spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemoveShaken = [spell_remove_fear, "Lionheart", "Aura of Glory", "Panacea"] #Lionheart, Panacea and Aura of Glory are currently not in the game yet
    if spellToCheck.spell_enum in spellsThatRemoveShaken:
        args.condition_remove()
    return 0

#def shakenConditionOnLeaveAoE(attachee, args, evt_obj):
#    aoeEventId = args.get_arg(2)
#    if aoeEventId != evt_obj.evt_id:
#        return 0
#    
#    ShakenDurationDice = dice_new('1d4+1')
#    diceResult = ShakenDurationDice.roll()
#    args.set_arg(0, diceResult)
#    args.set_arg(2, 0)
#    return 0

def shakenConditionGetTooltip(attachee, args, evt_obj):
    if args.get_arg(2):
        evt_obj.append("Shaken")
        return 0
    if args.get_arg(0) == 1:
        evt_obj.append("Shaken ({} round)".format(args.get_arg(0)))
    else:
        evt_obj.append("Shaken ({} rounds)".format(args.get_arg(0)))

    return 0

def shakenConditionGetEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(0) == 1:
        evt_obj.append(tpdp.hash("SHAKEN_CONDITION"), -2, " ({} round)".format(args.get_arg(0)))
    else:
        evt_obj.append(tpdp.hash("SHAKEN_CONDITION"), -2, " ({} rounds)".format(args.get_arg(0)))
    return 0

def shakenConditionRemoveCondition(attachee, args, evt_obj):
    if args.get_arg(3):
        attachee.float_text_line("Unaffected due to Racial Immunity")
    else:
        if attachee.stat_level_get(stat_hp_current) > -10:
            attachee.float_text_line("No longer Shaken")
            game.create_history_freeform(attachee.description + " is no longer ~Shaken~[TAG_Shaken]\n\n")
    return 0

shakenCondition = PythonModifier("Shaken Condition", 4) #duration, passedSpellID, aoeFlagId, racialImmunity
shakenCondition.AddHook(ET_OnConditionAdd, EK_NONE, shakenConditionAddActions, ())
shakenCondition.AddHook(ET_OnBeginRound, EK_NONE, shakenConditionBeginRound, ())
shakenCondition.AddHook(ET_OnToHitBonus2, EK_NONE, shakenConditionPenalty,())
shakenCondition.AddHook(ET_OnGetSkillLevel, EK_NONE, shakenConditionPenalty,())
shakenCondition.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, shakenConditionPenalty,())
shakenCondition.AddHook(ET_OnSaveThrowLevel, EK_NONE, shakenConditionPenalty,())
shakenCondition.AddHook(ET_OnD20PythonQuery, "Shaken Condition", shakenConditionAnswerToQuery, ())
shakenCondition.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, shakenConditionCheckRemoveBySpell, ())
#shakenCondition.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, shakenConditionOnLeaveAoE, ())
shakenCondition.AddHook(ET_OnConditionRemove, EK_NONE, shakenConditionRemoveCondition, ())
shakenCondition.AddHook(ET_OnGetTooltip, EK_NONE, shakenConditionGetTooltip, ())
shakenCondition.AddHook(ET_OnGetEffectTooltip, EK_NONE, shakenConditionGetEffectTooltip, ())
