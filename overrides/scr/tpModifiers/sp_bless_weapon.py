from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Bless Weapon"

def blessWeaponSpellOnConditionAdd(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Bless Weapon Condition', args.get_arg(1))
    return 0

def blessWeaponSpellOnDamage(attachee, args, evt_obj):
    targetAlignment = evt_obj.attack_packet.target.critter_get_alignment()
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Bless_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if not evt_obj.damage_packet.attack_power & D20DAP_HOLY:
        evt_obj.damage_packet.attack_power |= D20DAP_HOLY
    if targetAlignment & ALIGNMENT_EVIL:
        if not evt_obj.damage_packet.attack_power & D20DAP_MAGIC:
            evt_obj.damage_packet.attack_power |= D20DAP_MAGIC
    return 0

def blessWeaponSpellCheckThreatRange(attachee, args, evt_obj):
    appliedKeenRange =  evt_obj.bonus_list.get_sum()
    weaponUsed = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = weaponUsed.d20_query("Q_Has_Bless_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    weaponKeenRange = weaponUsed.obj_get_int(obj_f_weapon_crit_range)
    if appliedKeenRange == weaponKeenRange:
        args.set_arg(2, 0)
    else:
        args.set_arg(2, 1)
    return 0

def blessWeaponSpellConfirmCrit(attachee, args, evt_obj):
    targetAlignment = evt_obj.attack_packet.target.critter_get_alignment()
    if not targetAlignment & ALIGNMENT_EVIL:
        return 0
    if args.get_arg(2):
        return 0
    weaponUsed = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = weaponUsed.d20_query("Q_Has_Bless_Weapon_Effect")
    if isEnchantedWeapon:
        flags = evt_obj.attack_packet.get_flags()
        flags |= D20CAF_CRITICAL
        evt_obj.attack_packet.set_flags(flags)
    return 0

def blessWeaponSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Bless_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Bless Weapon ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Bless Weapon ({} rounds)".format(args.get_arg(1)))
    return 0

def blessWeaponSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Bless_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BLESS_WEAPON"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BLESS_WEAPON"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def blessWeaponSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def blessWeaponSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def blessWeaponSpellSpellEnd(attachee, args, evt_obj):
    print "Bless Weapon SpellEnd"
    return 0

blessWeaponSpell = PythonModifier("sp-Bless Weapon", 3) # spell_id, duration, keenFlag
blessWeaponSpell.AddHook(ET_OnConditionAdd, EK_NONE, blessWeaponSpellOnConditionAdd,())
blessWeaponSpell.AddHook(ET_OnGetCriticalHitRange, EK_NONE, blessWeaponSpellCheckThreatRange,())
blessWeaponSpell.AddHook(ET_OnDealingDamage, EK_NONE, blessWeaponSpellOnDamage,())
blessWeaponSpell.AddHook(ET_OnConfirmCriticalBonus, EK_NONE, blessWeaponSpellConfirmCrit,())
blessWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, blessWeaponSpellTooltip, ())
blessWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, blessWeaponSpellEffectTooltip, ())
blessWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, blessWeaponSpellSpellEnd, ())
blessWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, blessWeaponSpellHasSpellActive, ())
blessWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, blessWeaponSpellKilled, ())
blessWeaponSpell.AddSpellDispelCheckStandard()
blessWeaponSpell.AddSpellTeleportPrepareStandard()
blessWeaponSpell.AddSpellTeleportReconnectStandard()
blessWeaponSpell.AddSpellCountdownStandardHook()

###### Bless Weapon Condition ######
def blessWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 1

def blessWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def blessWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

blessWeaponCondition = PythonModifier("Bless Weapon Condition", 1) # duration
blessWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, blessWeaponConditionGlowEffect, ())
blessWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Bless_Weapon_Effect", blessWeaponConditionEffectAnswerToQuery, ())
blessWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, blessWeaponConditionTickdown, ())
