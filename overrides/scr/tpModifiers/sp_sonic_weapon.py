from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Sonic Weapon"

def sonicWeaponSpellChainToWeapon(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)

    mainhandWeapon.d20_status_init()
    spellPacket.add_target(mainhandWeapon, 0)
    spellPacket.update_registry()
    return 0

def sonicWeaponSpellBonusToDamage(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        bonusDice = dice_new('1d6') #Sonic Weapon Bonus Damage
        evt_obj.damage_packet.add_dice(bonusDice, D20DT_SONIC, 3001) #ID3001 added in damage.mes 
    return 0

def sonicWeaponSpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    removeWeaponFromSpellRegistry = spellPacket.get_target(0)
    spellPacket.remove_target(removeWeaponFromSpellRegistry)
    spellPacket.update_registry()
    args.remove_spell()
    return 0

def sonicWeaponSpellTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    if not spellPacket.get_target(1) == mainhandWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Sonic Weapon (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Sonic Weapon (" + str(args.get_arg(1)) + " rounds)")
    return 0

def sonicWeaponSpellEffectTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    if not spellPacket.get_target(1) == mainhandWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SONIC_WEAPON"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("SONIC_WEAPON"), -2, " (" + str(args.get_arg(1)) + " rounds)")
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
sonicWeaponSpell.AddHook(ET_OnConditionRemove, EK_NONE, sonicWeaponSpellConditionRemove, ())
sonicWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, sonicWeaponSpellTooltip, ())
sonicWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, sonicWeaponSpellEffectTooltip, ())
sonicWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, sonicWeaponSpellSpellEnd, ())
sonicWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, sonicWeaponSpellHasSpellActive, ())
sonicWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, sonicWeaponSpellKilled, ())
sonicWeaponSpell.AddSpellDispelCheckStandard()
sonicWeaponSpell.AddSpellTeleportPrepareStandard()
sonicWeaponSpell.AddSpellTeleportReconnectStandard()
sonicWeaponSpell.AddSpellCountdownStandardHook()
