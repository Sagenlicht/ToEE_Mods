from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Sonic Weapon"

def sonicWeaponSpellAddWeaponCondition(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.item_condition_add_with_args('Weapon Sonic', args.get_arg(1), 0)
    ####   Workaround to activate weapon enchantment   ####
    #attachee.item_worn_unwield(item_wear_weapon_primary)
    #attachee.item_wield(mainhandWeapon, item_wear_weapon_primary)
    #### Workaround to activate weapon enchantment end ####

def sonicWeaponSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    offhandWeapon = attachee.item_worn_at(item_wear_weapon_secondary)
    if mainhandWeapon.item_has_condition('Weapon Sonic') or offhandWeapon.item_has_condition('Weapon Sonic'):
        name = spell_utils.spellName(args.get_arg(0))
        duration = spell_utils.spellTime(args.get_arg(1))
        evt_obj.append("{} ({})".format(name, duration))
    return 0

def sonicWeaponSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    offhandWeapon = attachee.item_worn_at(item_wear_weapon_secondary)
    if mainhandWeapon.item_has_condition('Weapon Sonic') or offhandWeapon.item_has_condition('Weapon Sonic'):
        key = spell_utils.spellKey(args.get_arg(0))
        duration = spell_utils.spellTime(args.get_arg(1))
        evt_obj.append(key, -2, "({})".format(duration))
    return 0

sonicWeaponSpell = PythonModifier("sp-Sonic Weapon", 3) # spell_id, duration, empty
sonicWeaponSpell.AddHook(ET_OnConditionAdd, EK_NONE, sonicWeaponSpellAddWeaponCondition,())
sonicWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, sonicWeaponSpellTooltip, ())
sonicWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, sonicWeaponSpellEffectTooltip, ())
sonicWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
sonicWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
sonicWeaponSpell.AddSpellDispelCheckStandard()
sonicWeaponSpell.AddSpellTeleportPrepareStandard()
sonicWeaponSpell.AddSpellTeleportReconnectStandard()
sonicWeaponSpell.AddSpellCountdownStandardHook()

#### Weapon Sonic Condition ####

def weaponSonicOnDealingDamage(attachee, args, evt_obj):
    if not evt_obj.attack_packet.get_weapon_used().item_has_condition('Weapon Sonic'):
        return 0
    damageDice = dice_new('1d6') #Sonic Weapon Bonus Damage
    damageType = D20DT_SONIC
    damageMesId = 3001 #ID 3001 added in damage.mes
    evt_obj.damage_packet.add_dice(damageDice, damageType, damageMesId)
    return 0

def weaponSonicGlowType(attachee, args, evt_obj):
    if evt_obj.get_obj_from_args().item_has_condition('Weapon Sonic'):
        if not evt_obj.return_val:
            evt_obj.return_val = 7 #there is no sonic Weapon Glow in the game I think using holy for now
    return 0

def weaponSonicTickDown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

weaponSonic = PythonModifier("Weapon Sonic", 2) # duration, empty
weaponSonic.AddHook(ET_OnDealingDamage, EK_NONE, weaponSonicOnDealingDamage, ())
weaponSonic.AddHook(ET_OnWeaponGlowType, EK_NONE, weaponSonicGlowType, ())
weaponSonic.AddHook(ET_OnBeginRound, EK_NONE, weaponSonicTickDown, ())
