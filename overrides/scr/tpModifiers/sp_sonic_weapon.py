from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Sonic Weapon"

def sonicWeaponSpellChainToWeapon(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Sonic Weapon Condition', args.get_arg(1))
    return 0

def sonicWeaponSpellBonusToDamage(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Sonic_Weapon_Effect")
    if isEnchantedWeapon:
        bonusDice = dice_new('1d6') #Sonic Weapon Bonus Damage
        evt_obj.damage_packet.add_dice(bonusDice, D20DT_SONIC, 3001) #ID3001 added in damage.mes 
    return 0

def sonicWeaponSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Sonic_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Sonic Weapon ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Sonic Weapon ({} rounds)".format(args.get_arg(1)))
    return 0

def sonicWeaponSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Sonic_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SONIC_WEAPON"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("SONIC_WEAPON"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def sonicWeaponSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def sonicWeaponSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def sonicWeaponSpellSpellEnd(attachee, args, evt_obj):
    print "Sonic Weapon SpellEnd"
    return 0

sonicWeaponSpell = PythonModifier("sp-Sonic Weapon", 2) # spell_id, duration
sonicWeaponSpell.AddHook(ET_OnConditionAdd, EK_NONE, sonicWeaponSpellChainToWeapon,())
sonicWeaponSpell.AddHook(ET_OnDealingDamage, EK_NONE, sonicWeaponSpellBonusToDamage,())
sonicWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, sonicWeaponSpellTooltip, ())
sonicWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, sonicWeaponSpellEffectTooltip, ())
sonicWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, sonicWeaponSpellSpellEnd, ())
sonicWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, sonicWeaponSpellHasSpellActive, ())
sonicWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, sonicWeaponSpellKilled, ())
sonicWeaponSpell.AddSpellDispelCheckStandard()
sonicWeaponSpell.AddSpellTeleportPrepareStandard()
sonicWeaponSpell.AddSpellTeleportReconnectStandard()
sonicWeaponSpell.AddSpellCountdownStandardHook()

###### Sonic Weapon Condition ######
def sonicWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 1

def sonicWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def sonicWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

sonicWeaponCondition = PythonModifier("Sonic Weapon Condition", 1) # duration
sonicWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, sonicWeaponConditionGlowEffect, ())
sonicWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Sonic_Weapon_Effect", sonicWeaponConditionEffectAnswerToQuery, ())
sonicWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, sonicWeaponConditionTickdown, ())
