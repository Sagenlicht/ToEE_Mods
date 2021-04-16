from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Align Weapon"

def alignWeaponSpellOnConditionAdd(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Align Weapon Condition', args.get_arg(1), args.get_arg(2))
    return 0

def alignWeaponSpellOnDamage(attachee, args, evt_obj):
    alignType = args.get_arg(2)
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Align_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if alignType == 1:
        if not evt_obj.damage_packet.attack_power & D20DAP_HOLY:
            evt_obj.damage_packet.attack_power |= D20DAP_HOLY
    elif alignType == 2:
        if not evt_obj.damage_packet.attack_power & D20DAP_UNHOLY:
            evt_obj.damage_packet.attack_power |= D20DAP_UNHOLY
    elif alignType == 3:
        if not evt_obj.damage_packet.attack_power & D20DAP_LAW:
            evt_obj.damage_packet.attack_power |= D20DAP_LAW
    elif alignType == 4:
        if not evt_obj.damage_packet.attack_power & D20DAP_CHAOS:
            evt_obj.damage_packet.attack_power |= D20DAP_CHAOS
    return 0

def alignTpyeTooltipDict(getAlignType):
    alignTypeDict={
    1: "Good",
    2: "Evil",
    3: "Lawful",
    4: "Chaotic"
    }
    return alignTypeDict.get(getAlignType)

def alignWeaponSpellTooltip(attachee, args, evt_obj):
    alignType = alignTpyeTooltipDict(args.get_arg(2))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Align_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append("Align Weapon ({}) ({} round)".format(alignType, args.get_arg(1)))
    else:
        evt_obj.append("Align Weapon ({}) ({} rounds)".format(alignType, args.get_arg(1)))
    return 0

def alignWeaponSpellEffectTooltip(attachee, args, evt_obj):
    alignType = alignTpyeTooltipDict(args.get_arg(2))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Align_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("ALIGN_WEAPON"), -2, "({}) ({} round)".format(alignType, args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("ALIGN_WEAPON"), -2, "({}) ({} rounds)".format(alignType, args.get_arg(1)))
    return 0

def alignWeaponSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def alignWeaponSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def alignWeaponSpellSpellEnd(attachee, args, evt_obj):
    print "Align Weapon SpellEnd"
    return 0

alignWeaponSpell = PythonModifier("sp-Align Weapon", 3) # spell_id, duration, alignType
alignWeaponSpell.AddHook(ET_OnConditionAdd, EK_NONE, alignWeaponSpellOnConditionAdd,())
alignWeaponSpell.AddHook(ET_OnDealingDamage, EK_NONE, alignWeaponSpellOnDamage,())
alignWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, alignWeaponSpellTooltip, ())
alignWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, alignWeaponSpellEffectTooltip, ())
alignWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, alignWeaponSpellSpellEnd, ())
alignWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, alignWeaponSpellHasSpellActive, ())
alignWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, alignWeaponSpellKilled, ())
alignWeaponSpell.AddSpellDispelCheckStandard()
alignWeaponSpell.AddSpellTeleportPrepareStandard()
alignWeaponSpell.AddSpellTeleportReconnectStandard()
alignWeaponSpell.AddSpellCountdownStandardHook()

###### Align Weapon Condition ######
def alignWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 1

def alignWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def alignWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

alignWeaponCondition = PythonModifier("Align Weapon Condition", 2) # duration, alignType
alignWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, alignWeaponConditionGlowEffect, ())
alignWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Align_Weapon_Effect", alignWeaponConditionEffectAnswerToQuery, ()) #not tested
alignWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, alignWeaponConditionTickdown, ())