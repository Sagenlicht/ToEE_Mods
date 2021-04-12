from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Undead Bane Weapon"

def undeadBaneWeaponSpellChainToWeapon(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)

    mainhandWeapon.d20_status_init()
    spellPacket.add_target(mainhandWeapon, 0)
    spellPacket.update_registry()
    return 0

def undeadBaneWeaponSpellBonusToHit(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    target = evt_obj.attack_packet.target
    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        if target.is_category_type(mc_type_undead):
            evt_obj.bonus_list.add(2,0,"~Undead Bane Weapon~[TAG_SPELLS_UNDEAD_BANE_WEAPON] Bonus") #Undead Bane Weapon adds a +2 Bonus to Attack Rolls against undead
    return 0

def undeadBaneWeaponSpellOnDamage(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    target = evt_obj.attack_packet.target

    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        enchantedWeaponUsed = True
        evt_obj.damage_packet.attack_power |= D20DAP_HOLY #Undead Bane Weapon adds good property
    else:
        enchantedWeaponUsed = False
    if target.is_category_type(mc_type_undead):
        targetIsUndead = True
    else:
        targetIsUndead = False
    if enchantedWeaponUsed and targetIsUndead:
        bonusDice = dice_new('1d6') #Undead Weapon Bonus Damage
        bonusDice.number = 2
        evt_obj.damage_packet.add_dice(bonusDice, D20DT_UNSPECIFIED, 3006) #ID3006 added in damage.mes; Undead Bane adds 2d6 extra damage
    return 0

def undeadBaneWeaponSpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    removeWeaponFromSpellRegistry = spellPacket.get_target(0)
    spellPacket.remove_target(removeWeaponFromSpellRegistry)
    spellPacket.update_registry()
    args.remove_spell()
    return 0

def undeadBaneWeaponSpellTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if not spellPacket.get_target(1) == attachee.item_worn_at(item_wear_weapon_primary):
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append("Undead Bane Weapon ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Undead Bane Weapon ({} rounds)".format(args.get_arg(1)))
    return 0

def undeadBaneWeaponSpellEffectTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if not spellPacket.get_target(1) == attachee.item_worn_at(item_wear_weapon_primary):
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("UNDEAD_BANE_WEAPON"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("UNDEAD_BANE_WEAPON"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def undeadBaneWeaponSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def undeadBaneWeaponSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def undeadBaneWeaponSpellSpellEnd(attachee, args, evt_obj):
    print "Undead Bane Weapon SpellEnd"
    return 0

undeadBaneWeaponSpell = PythonModifier("sp-Undead Bane Weapon", 2) # spell_id, duration
undeadBaneWeaponSpell.AddHook(ET_OnToHitBonus2, EK_NONE, undeadBaneWeaponSpellBonusToHit, ())
undeadBaneWeaponSpell.AddHook(ET_OnDealingDamage, EK_NONE, undeadBaneWeaponSpellOnDamage, ())
undeadBaneWeaponSpell.AddHook(ET_OnConditionAdd, EK_NONE, undeadBaneWeaponSpellChainToWeapon,())
undeadBaneWeaponSpell.AddHook(ET_OnConditionRemove, EK_NONE, undeadBaneWeaponSpellConditionRemove, ())
undeadBaneWeaponSpell.AddHook(ET_OnGetTooltip, EK_NONE, undeadBaneWeaponSpellTooltip, ())
undeadBaneWeaponSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, undeadBaneWeaponSpellEffectTooltip, ())
undeadBaneWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, undeadBaneWeaponSpellSpellEnd, ())
undeadBaneWeaponSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, undeadBaneWeaponSpellHasSpellActive, ())
undeadBaneWeaponSpell.AddHook(ET_OnD20Signal, EK_S_Killed, undeadBaneWeaponSpellKilled, ())
undeadBaneWeaponSpell.AddSpellDispelCheckStandard()
undeadBaneWeaponSpell.AddSpellTeleportPrepareStandard()
undeadBaneWeaponSpell.AddSpellTeleportReconnectStandard()
undeadBaneWeaponSpell.AddSpellCountdownStandardHook()
