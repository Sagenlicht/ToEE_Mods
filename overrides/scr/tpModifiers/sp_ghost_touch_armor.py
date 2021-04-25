from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Ghost Touch Armor"

def ghostTouchArmorSpellOnConditionAdd(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    wornArmor.d20_status_init()
    wornArmor.condition_add_with_args('Ghost Touch Armor Condition', args.get_arg(1))
    
    acValue = wornArmor.item_d20_query(Q_Armor_Get_AC_Bonus)
    args.set_arg(2, acValue)
    return 0

def ghostTouchArmorSpellOnGetAc(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    isEnchantedArmor = wornArmor.d20_query("Q_Ghost_Touch_Armor_Effect")
    if not isEnchantedArmor:
        return 0
    armorBonusToAc = args.get_arg(2)
    if armorBonusToAc:
        if evt_obj.attack_packet.attacker.is_category_subtype(mc_subtype_incorporeal):
            evt_obj.bonus_list.add(armorBonusToAc, 161, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Ghost Touch Armor~[TAG_SPELLS_GHOST_TOUCH_ARMOR]")
    return 0

def ghostTouchArmorSpellTooltip(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    isEnchantedArmor = wornArmor.d20_query("Q_Ghost_Touch_Armor_Effect")
    if not isEnchantedArmor:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Ghost Touch Armor ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Ghost Touch Armor ({} rounds)".format(args.get_arg(1)))
    return 0

def ghostTouchArmorSpellEffectTooltip(attachee, args, evt_obj):
    wornArmor = attachee.item_worn_at(item_wear_armor)
    isEnchantedArmor = wornArmor.d20_query("Q_Ghost_Touch_Armor_Effect")
    if not isEnchantedArmor:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("GHOST_TOUCH_ARMOR"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("GHOST_TOUCH_ARMOR"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def ghostTouchArmorSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def ghostTouchArmorSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def ghostTouchArmorSpellSpellEnd(attachee, args, evt_obj):
    print "Ghost Touch Armor SpellEnd"
    return 0

ghostTouchArmorSpell = PythonModifier("sp-Ghost Touch Armor", 3) # spell_id, duration, armorBonusToAc
ghostTouchArmorSpell.AddHook(ET_OnConditionAdd, EK_NONE, ghostTouchArmorSpellOnConditionAdd, ())
ghostTouchArmorSpell.AddHook(ET_OnGetAC, EK_NONE, ghostTouchArmorSpellOnGetAc, ())
ghostTouchArmorSpell.AddHook(ET_OnGetTooltip, EK_NONE, ghostTouchArmorSpellTooltip, ())
ghostTouchArmorSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, ghostTouchArmorSpellEffectTooltip, ())
ghostTouchArmorSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, ghostTouchArmorSpellSpellEnd, ())
ghostTouchArmorSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, ghostTouchArmorSpellHasSpellActive, ())
ghostTouchArmorSpell.AddHook(ET_OnD20Signal, EK_S_Killed, ghostTouchArmorSpellKilled, ())
ghostTouchArmorSpell.AddSpellDispelCheckStandard()
ghostTouchArmorSpell.AddSpellTeleportPrepareStandard()
ghostTouchArmorSpell.AddSpellTeleportReconnectStandard()
ghostTouchArmorSpell.AddSpellCountdownStandardHook()

###### Ghost Touch Armor Condition ######
def diamondsteelConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def diamondsteelConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

diamondsteelCondition = PythonModifier("Ghost Touch Armor Condition", 1) # duration
diamondsteelCondition.AddHook(ET_OnD20PythonQuery, "Q_Ghost_Touch_Armor_Effect", diamondsteelConditionEffectAnswerToQuery, ())
diamondsteelCondition.AddHook(ET_OnBeginRound , EK_NONE, diamondsteelConditionTickdown, ())