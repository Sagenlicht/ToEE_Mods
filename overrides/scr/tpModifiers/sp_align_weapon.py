from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Align Weapon"

def alignTpyeTooltipDict(getAlignType):
    alignTypeDict={
    1: "Good",
    2: "Evil",
    3: "Lawful",
    4: "Chaotic"
    }
    return alignTypeDict.get(getAlignType)

def alignWeaponSpellOnConditionAdd(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.item_condition_add_with_args('Weapon Align', args.get_arg(1), args.get_arg(2), 0)
    return 0

def alignWeaponSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    offhandWeapon = attachee.item_worn_at(item_wear_weapon_secondary)
    if mainhandWeapon.item_has_condition('Weapon Align') or offhandWeapon.item_has_condition('Weapon Align'):
        alignType = alignTpyeTooltipDict(args.get_arg(2))
        name = "Align Weapon"
        duration = spell_utils.spellTime(args.get_arg(1))
        evt_obj.append("{} ({}) ({})".format(name, alignType, duration))
    return 0

def alignWeaponSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    offhandWeapon = attachee.item_worn_at(item_wear_weapon_secondary)
    if mainhandWeapon.item_has_condition('Weapon Align') or offhandWeapon.item_has_condition('Weapon Align'):
        alignType = alignTpyeTooltipDict(args.get_arg(2))
        key = tpdp.hash("ALIGN_WEAPON")
        duration = spell_utils.spellTime(args.get_arg(1))
        evt_obj.append(key, -2, "({}) ({})".format(alignType, duration))
    return 0

alignWeaponSpell = PythonModifier("sp-Align Weapon", 4) # spell_id, duration, alignType, empty
alignWeaponSpell.AddHook(ET_OnConditionAdd, EK_NONE, alignWeaponSpellOnConditionAdd,())
alignWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, alignWeaponSpellTooltip, ())
alignWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, alignWeaponSpellEffectTooltip, ())
alignWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
alignWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
alignWeaponSpell.AddSpellDispelCheckStandard()
alignWeaponSpell.AddSpellTeleportPrepareStandard()
alignWeaponSpell.AddSpellTeleportReconnectStandard()
alignWeaponSpell.AddSpellCountdownStandardHook()


###### Align Weapon Condition ######

def weaponAlignOnDamage(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_weapon_used().item_has_condition('Weapon Align'):
        return 0

    #Check if weapn is already aligned
    if evt_obj.damage_packet.attack_power & D20DAP_HOLY:
        return 0
    elif evt_obj.damage_packet.attack_power & D20DAP_UNHOLY:
        return 0
    elif evt_obj.damage_packet.attack_power & D20DAP_LAW:
        return 0
    elif evt_obj.damage_packet.attack_power & D20DAP_CHAOS:
        return 0

    alignType = args.get_arg(1)

    if alignType == 1:
        evt_obj.damage_packet.attack_power |= D20DAP_HOLY
        game.particles('hit-HOLY-medium', evt_obj.attack_packet.target)
    elif alignType == 2:
        evt_obj.damage_packet.attack_power |= D20DAP_UNHOLY
        game.particles('hit-UNHOLY-medium', evt_obj.attack_packet.target)
    elif alignType == 3:
        evt_obj.damage_packet.attack_power |= D20DAP_LAW
        game.particles('hit-LAW-medium', evt_obj.attack_packet.target)
    elif alignType == 4:
        evt_obj.damage_packet.attack_power |= D20DAP_CHAOS
        game.particles('hit-CHAOTIC-medium', evt_obj.attack_packet.target)
    return 0

def weaponAlignGlowEffect(attachee, args, evt_obj):
    if not evt_obj.get_obj_from_args().item_has_condition('Weapon Align'):
        return 0

    alignType = args.get_arg(1)
    if alignType == 1:
        evt_obj.return_val = 7
    elif alignType == 2:
        evt_obj.return_val = 10
    elif alignType == 3:
        evt_obj.return_val = 8
    elif alignType == 4:
        evt_obj.return_val = 4
    return 0

def weaponAlignTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

weaponAlign = PythonModifier("Weapon Align", 3) # duration, alignType, empty
weaponAlign.AddHook(ET_OnDealingDamage, EK_NONE, weaponAlignOnDamage,())
weaponAlign.AddHook(ET_OnWeaponGlowType, EK_NONE, weaponAlignGlowEffect, ())
weaponAlign.AddHook(ET_OnBeginRound , EK_NONE, weaponAlignTickdown, ())