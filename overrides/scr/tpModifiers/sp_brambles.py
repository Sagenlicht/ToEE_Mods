from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Brambles"

def bramblesSpellAddWeaponCondition(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.item_condition_add_with_args('Weapon Brambles', args.get_arg(1), args.get_arg(2), 0)
    return 0

def bramblesSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    if mainhandWeapon.item_has_condition('Weapon Brambles'):
        name = spell_utils.spellName(args.get_arg(0))
        duration = spell_utils.spellTime(args.get_arg(1))
        evt_obj.append("{} ({})".format(name, duration))
    return 0

def bramblesSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    if mainhandWeapon.item_has_condition('Weapon Brambles'):
        key = spell_utils.spellKey(args.get_arg(0))
        duration = spell_utils.spellTime(args.get_arg(1))
        evt_obj.append(key, -2, " ({})".format(duration))
    return 0

bramblesSpell = PythonModifier("sp-Brambles", 4) # spell_id, duration, bonusDamage, empty
bramblesSpell.AddHook(ET_OnConditionAdd, EK_NONE, bramblesSpellAddWeaponCondition,())
bramblesSpell.AddHook(ET_OnGetTooltip, EK_NONE, bramblesSpellTooltip, ())
bramblesSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, bramblesSpellEffectTooltip, ())
bramblesSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
bramblesSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
bramblesSpell.AddSpellDispelCheckStandard()
bramblesSpell.AddSpellTeleportPrepareStandard()
bramblesSpell.AddSpellTeleportReconnectStandard()
bramblesSpell.AddSpellCountdownStandardHook()

###### Brambles Weapon Condition ######

def bramblesWeaponConditionToHitBonus(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_weapon_used().item_has_condition('Weapon Brambles'):
        return 0
    evt_obj.bonus_list.add(1, 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Brambles~[TAG_SPELLS_BRAMBLES]")
    return 0

def bramblesWeaponConditionBonusToDamage(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_weapon_used().item_has_condition('Weapon Brambles'):
        return 0
    weaponDamageType = attachee.obj_get_int(obj_f_weapon_attacktype)
    if not weaponDamageType == D20DT_BLUDGEONING_AND_PIERCING:
        if not weaponDamageType == D20DT_BLUDGEONING:
            evt_obj.damage_packet.attack_power |= D20DAP_BLUDGEONING
        if not weaponDamageType == D20DT_PIERCING:
            evt_obj.damage_packet.attack_power |= D20DAP_PIERCING
    if not evt_obj.damage_packet.attack_power & D20DAP_MAGIC:
        evt_obj.damage_packet.attack_power |= D20DAP_MAGIC
    evt_obj.damage_packet.bonus_list.add(args.get_arg(1), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Brambles~[TAG_SPELLS_BRAMBLES]")
    return 0

def bramblesWeaponConditionGlowEffect(attachee, args, evt_obj):
    if evt_obj.get_obj_from_args().item_has_condition('Weapon Brambles'):
        if not evt_obj.return_val:
            evt_obj.return_val = 3
    return 0

def bramblesWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

weaponBrambles = PythonModifier("Weapon Brambles", 3) # duration, bonusDamage, empty
weaponBrambles.AddHook(ET_OnToHitBonus2, EK_NONE, bramblesWeaponConditionToHitBonus, ())
weaponBrambles.AddHook(ET_OnDealingDamage, EK_NONE, bramblesWeaponConditionBonusToDamage,())
weaponBrambles.AddHook(ET_OnWeaponGlowType, EK_NONE, bramblesWeaponConditionGlowEffect, ())
weaponBrambles.AddHook(ET_OnBeginRound , EK_NONE, bramblesWeaponConditionTickdown, ())