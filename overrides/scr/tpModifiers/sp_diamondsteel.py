from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Diamondsteel"

def isEnchantedArmor(attachee):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    hasSpellEffect = wornArmor.d20_query("Q_Has_Diamondsteel_Effect")
    return hasSpellEffect

def diamondsteelSpellOnCondidtionAdd(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    wornArmor.d20_status_init()
    wornArmor.condition_add_with_args('Diamondsteel Condition', args.get_arg(1))

    acValue = wornArmor.item_d20_query(Q_Armor_Get_AC_Bonus)
    args.set_arg(2, acValue)
    return 0

def diamondsteelSpellGrantDr(attachee, args, evt_obj):
    if isEnchantedArmor(attachee):
        evt_obj.damage_packet.add_physical_damage_res(args.get_arg(2), D20DAP_ADAMANTIUM, 126) #Diamondsteel grants DR adamantine value depends on AC granted by the armor; ID126 in damage.mes is DR
    return 0

def diamondsteelSpellTooltip(attachee, args, evt_obj):
    if isEnchantedArmor(attachee):
        if args.get_arg(1) == 1:
            evt_obj.append("Diamondsteel ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append("Diamondsteel ({} rounds)".format(args.get_arg(1)))
    return 0

def diamondsteelSpellEffectTooltip(attachee, args, evt_obj):
    if not isEnchantedArmor(attachee):
        if args.get_arg(1) == 1:
            evt_obj.append(tpdp.hash("DIAMONDSTEEL"), -2, " ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append(tpdp.hash("DIAMONDSTEEL"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def diamondsteelSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def diamondsteelSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def diamondsteelSpellSpellEnd(attachee, args, evt_obj):
    print "Diamondsteel SpellEnd"
    return 0

diamondsteelSpell = PythonModifier("sp-Diamondsteel", 3) # spell_id, duration, acValue
diamondsteelSpell.AddHook(ET_OnConditionAdd , EK_NONE, diamondsteelSpellOnCondidtionAdd,())
diamondsteelSpell.AddHook(ET_OnTakingDamage , EK_NONE, diamondsteelSpellGrantDr,())
diamondsteelSpell.AddHook(ET_OnGetTooltip, EK_NONE, diamondsteelSpellTooltip, ())
diamondsteelSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, diamondsteelSpellEffectTooltip, ())
diamondsteelSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, diamondsteelSpellSpellEnd, ())
diamondsteelSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, diamondsteelSpellHasSpellActive, ())
diamondsteelSpell.AddHook(ET_OnD20Signal, EK_S_Killed, diamondsteelSpellKilled, ())
diamondsteelSpell.AddSpellDispelCheckStandard()
diamondsteelSpell.AddSpellTeleportPrepareStandard()
diamondsteelSpell.AddSpellTeleportReconnectStandard()
diamondsteelSpell.AddSpellCountdownStandardHook()

###### Diamondsteel Condition ######
def diamondsteelConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def diamondsteelConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

diamondsteelCondition = PythonModifier("Diamondsteel Condition", 1) # duration
diamondsteelCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Diamondsteel_Effect", diamondsteelConditionEffectAnswerToQuery, ())
diamondsteelCondition.AddHook(ET_OnBeginRound , EK_NONE, diamondsteelConditionTickdown, ())