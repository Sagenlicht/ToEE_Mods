from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Lawful Sword"

def lawfulSwordSpellChainToWeapon(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)

    mainhandWeapon.d20_status_init()
    spellPacket.add_target(mainhandWeapon, 0)
    spellPacket.update_registry()
    return 0

def lawfulSwordSpellBonusToHit(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    target = evt_obj.attack_packet.target
    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        evt_obj.bonus_list.add(5, 12, "~Lawful Sword~[TAG_SPELLS_LAWFUL_SWORD] ~Enhancement~[TAG_ENHANCEMENT_BONUS] Bonus") #Lawful Sword changes enhancement bonus +5
    return 0

def lawfulSwordSpellOnDamage(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    target = evt_obj.attack_packet.target
    targetAlignment = target.critter_get_alignment()

    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        enchantedWeaponUsed = True
        evt_obj.damage_packet.attack_power |= D20DAP_LAW #Lawful Sword adds axiomatic property
        evt_obj.damage_packet.bonus_list.add(5, 12, "~Lawful Sword~[TAG_SPELLS_LAWFUL_SWORD] ~Enhancement~[TAG_ENHANCEMENT_BONUS] Bonus") #Lawful Sword changes enhancement bonus +5
    else:
        enchantedWeaponUsed = False
    if targetAlignment & ALIGNMENT_CHAOTIC:
        targetIsChaotic = True
    else:
        targetIsChaotic = False

    if enchantedWeaponUsed and targetIsChaotic:
        bonusDice = dice_new('1d6') #Lawful Sword axiomatic Bonus Damage
        bonusDice.number = 2
        evt_obj.damage_packet.add_dice(bonusDice, D20DT_UNSPECIFIED, 3007) #ID 3007 added in damage.mes;
    return 0

def lawfulSwordSpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    removeWeaponFromSpellRegistry = spellPacket.get_target(0)
    spellPacket.remove_target(removeWeaponFromSpellRegistry)
    spellPacket.update_registry()
    args.remove_spell()
    return 0

def lawfulSwordSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Lawful Sword ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Lawful Sword ({} rounds)".format(args.get_arg(1)))
    return 0

def lawfulSwordSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("LAWFUL_SWORD"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("LAWFUL_SWORD"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def lawfulSwordSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def lawfulSwordSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def lawfulSwordSpellSpellEnd(attachee, args, evt_obj):
    print "Lawful Sword SpellEnd"
    return 0

lawfulSwordSpell = PythonModifier("sp-Lawful Sword", 2) # spell_id, duration
lawfulSwordSpell.AddHook(ET_OnToHitBonus2, EK_NONE, lawfulSwordSpellBonusToHit, ())
lawfulSwordSpell.AddHook(ET_OnDealingDamage, EK_NONE, lawfulSwordSpellOnDamage, ())
lawfulSwordSpell.AddHook(ET_OnConditionAdd, EK_NONE, lawfulSwordSpellChainToWeapon,())
lawfulSwordSpell.AddHook(ET_OnConditionRemove, EK_NONE, lawfulSwordSpellConditionRemove, ())
lawfulSwordSpell.AddHook(ET_OnGetTooltip, EK_NONE, lawfulSwordSpellTooltip, ())
lawfulSwordSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, lawfulSwordSpellEffectTooltip, ())
lawfulSwordSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, lawfulSwordSpellSpellEnd, ())
lawfulSwordSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, lawfulSwordSpellHasSpellActive, ())
lawfulSwordSpell.AddHook(ET_OnD20Signal, EK_S_Killed, lawfulSwordSpellKilled, ())
lawfulSwordSpell.AddSpellDispelCheckStandard()
lawfulSwordSpell.AddSpellTeleportPrepareStandard()
lawfulSwordSpell.AddSpellTeleportReconnectStandard()
lawfulSwordSpell.AddSpellCountdownStandardHook()
