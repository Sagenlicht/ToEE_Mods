from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Iron Silence"

def ironSilenceSpellChainToArmor(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    wornArmor.d20_status_init()
    wornArmor.condition_add_with_args('Iron Silence Condition', args.get_arg(1))
    return 0

def ironSilenceSpellNullifyArmorCheckPenalty(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    isEnchantedArmor = wornArmor.d20_query("Q_Has_Iron_Silence_Effect")
    if isEnchantedArmor:
        wornArmorCheckPenalty = wornArmor.obj_get_int(obj_f_armor_armor_check_penalty) # Get Armor Check Penalty
        evt_obj.bonus_list.add(abs(wornArmorCheckPenalty), 0, "~Iron Silence~[TAG_SPELLS_IRON_SILENCE] Bonus") #Generic stacking bonus to counteract the Armor Check Penalty
        #evt_obj.bonus_list.add_cap(0, 0, 6), this would cancel out the masterwork property but also everything else.
    return 0

def ironSilenceSpellTooltip(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    isEnchantedArmor = wornArmor.d20_query("Q_Has_Iron_Silence_Effect")
    if isEnchantedArmor:
        if args.get_arg(1) == 1:
            evt_obj.append("Iron Silence ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append("Iron Silence ({} rounds)".format(args.get_arg(1)))
    return 0

def ironSilenceSpellEffectTooltip(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    isEnchantedArmor = wornArmor.d20_query("Q_Has_Iron_Silence_Effect")
    if isEnchantedArmor:
        if args.get_arg(1) == 1:
            evt_obj.append(tpdp.hash("IRON_SILENCE"), -2, " ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append(tpdp.hash("IRON_SILENCE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def ironSilenceSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def ironSilenceSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def ironSilenceSpellSpellEnd(attachee, args, evt_obj):
    print "Iron SilenceSpellEnd"
    return 0

ironSilenceSpell = PythonModifier("sp-Iron Silence", 2) # spell_id, duration
ironSilenceSpell.AddHook(ET_OnConditionAdd, EK_NONE, ironSilenceSpellChainToArmor,())
ironSilenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_HIDE, ironSilenceSpellNullifyArmorCheckPenalty,())
ironSilenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_MOVE_SILENTLY, ironSilenceSpellNullifyArmorCheckPenalty,())
ironSilenceSpell.AddHook(ET_OnGetTooltip, EK_NONE, ironSilenceSpellTooltip, ())
ironSilenceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, ironSilenceSpellEffectTooltip, ())
ironSilenceSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, ironSilenceSpellSpellEnd, ())
ironSilenceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, ironSilenceSpellHasSpellActive, ())
ironSilenceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, ironSilenceSpellKilled, ())
ironSilenceSpell.AddSpellDispelCheckStandard()
ironSilenceSpell.AddSpellTeleportPrepareStandard()
ironSilenceSpell.AddSpellTeleportReconnectStandard()
ironSilenceSpell.AddSpellCountdownStandardHook()

###### Iron Silence Condition ######
def ironSilenceConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def ironSilenceConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

ironSilenceCondition = PythonModifier("Iron Silence Condition", 1) # duration
ironSilenceCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Iron_Silence_Effect", ironSilenceConditionEffectAnswerToQuery, ())
ironSilenceCondition.AddHook(ET_OnBeginRound , EK_NONE, ironSilenceConditionTickdown, ())