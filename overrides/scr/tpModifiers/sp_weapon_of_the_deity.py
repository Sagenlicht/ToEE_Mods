from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Weapon of the Deity"

def weaponOfTheDeitySpellChainToWeapon(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)

    mainhandWeapon.d20_status_init()
    spellPacket.add_target(mainhandWeapon, 0)
    spellPacket.update_registry()
    return 0

def weaponOfTheDeitySpellBonusToHit(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        #evt_obj.bonus_list.add_cap(37, 0, 2, "~Weapon of the Deity~[TAG_SPELLS_WEAPON_OF_THE_DEITY]") # does not negate the -4 non proficient penalty, but it should
        evt_obj.bonus_list.modify(4, 37, 138) # using modify now to negate, works
        evt_obj.bonus_list.add(args.get_arg(2), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Weapon of the Deity~[TAG_SPELLS_WEAPON_OF_THE_DEITY]") #Weapon of the Deity adds a Bonus to Attack Rolls (bonus passed by spell)
    return 0

def weaponOfTheDeitySpellOnDamage(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        evt_obj.damage_packet.bonus_list.add(args.get_arg(2), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Weapon of the Deity~[TAG_SPELLS_WEAPON_OF_THE_DEITY]")
    return 0

def weaponOfTheDeitySpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    removeWeaponFromSpellRegistry = spellPacket.get_target(0)
    spellPacket.remove_target(removeWeaponFromSpellRegistry)
    spellPacket.update_registry()
    args.remove_spell()
    return 0

def weaponOfTheDeitySpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Weapon of the Deity ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Weapon of the Deity ({} rounds)".format(args.get_arg(1)))
    return 0

def weaponOfTheDeitySpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("WEAPON_OF_THE_DEITY"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("WEAPON_OF_THE_DEITY"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def weaponOfTheDeitySpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def weaponOfTheDeitySpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def weaponOfTheDeitySpellSpellEnd(attachee, args, evt_obj):
    print "Weapon of the Deity SpellEnd"
    return 0

weaponOfTheDeitySpell = PythonModifier("sp-Weapon of the Deity", 4) # spell_id, duration, weaponToHitBonus, spellCasterDeity
weaponOfTheDeitySpell.AddHook(ET_OnToHitBonus2, EK_NONE, weaponOfTheDeitySpellBonusToHit, ())
weaponOfTheDeitySpell.AddHook(ET_OnDealingDamage, EK_NONE, weaponOfTheDeitySpellOnDamage, ())
weaponOfTheDeitySpell.AddHook(ET_OnConditionAdd, EK_NONE, weaponOfTheDeitySpellChainToWeapon,())
weaponOfTheDeitySpell.AddHook(ET_OnConditionRemove, EK_NONE, weaponOfTheDeitySpellConditionRemove, ())
weaponOfTheDeitySpell.AddHook(ET_OnGetTooltip, EK_NONE, weaponOfTheDeitySpellTooltip, ())
weaponOfTheDeitySpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, weaponOfTheDeitySpellEffectTooltip, ())
weaponOfTheDeitySpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, weaponOfTheDeitySpellSpellEnd, ())
weaponOfTheDeitySpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, weaponOfTheDeitySpellHasSpellActive, ())
weaponOfTheDeitySpell.AddHook(ET_OnD20Signal, EK_S_Killed, weaponOfTheDeitySpellKilled, ())
weaponOfTheDeitySpell.AddSpellDispelCheckStandard()
weaponOfTheDeitySpell.AddSpellTeleportPrepareStandard()
weaponOfTheDeitySpell.AddSpellTeleportReconnectStandard()
weaponOfTheDeitySpell.AddSpellCountdownStandardHook()
