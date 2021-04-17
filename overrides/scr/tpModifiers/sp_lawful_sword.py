from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Lawful Sword"

def lawfulSwordSpellChainToWeapon(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Lawful Sword Weapon Condition', args.get_arg(1))
    return 0

def lawfulSwordSpellBonusToHit(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Lawful_Sword_Weapon_Effect")
    if isEnchantedWeapon:
        evt_obj.bonus_list.add(5, 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Lawful Sword~[TAG_SPELLS_LAWFUL_SWORD]") #Lawful Sword changes enhancement bonus +5
    return 0

def lawfulSwordSpellOnDamage(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    target = evt_obj.attack_packet.target
    targetAlignment = target.critter_get_alignment()
    usedWeapon = evt_obj.attack_packet.get_weapon_used()

    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Lawful_Sword_Weapon_Effect")
    if isEnchantedWeapon:
        evt_obj.damage_packet.bonus_list.add(5, 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Lawful Sword~[TAG_SPELLS_LAWFUL_SWORD]") #Lawful Sword changes enhancement bonus to +5
        if not evt_obj.damage_packet.attack_power & D20DAP_MAGIC: #Lawful Sword adds magic property
            evt_obj.damage_packet.attack_power |= D20DAP_MAGIC
        if not evt_obj.damage_packet.attack_power & D20DAP_LAW: #Lawful Sword adds axiomatic property, which makes weapon lawful aligned
            evt_obj.damage_packet.attack_power |= D20DAP_LAW
        if targetAlignment & ALIGNMENT_CHAOTIC:
            bonusDice = dice_new('1d6')
            bonusDice.number = 2
            evt_obj.damage_packet.add_dice(bonusDice, D20DT_UNSPECIFIED, 3007) #ID 3007 added in damage.mes;
    return 0

def lawfulSwordSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Lawful_Sword_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append("Lawful Sword ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Lawful Sword ({} rounds)".format(args.get_arg(1)))
    return 0

def lawfulSwordSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Lawful_Sword_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

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
lawfulSwordSpell.AddHook(ET_OnGetTooltip, EK_NONE, lawfulSwordSpellTooltip, ())
lawfulSwordSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, lawfulSwordSpellEffectTooltip, ())
lawfulSwordSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, lawfulSwordSpellSpellEnd, ())
lawfulSwordSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, lawfulSwordSpellHasSpellActive, ())
lawfulSwordSpell.AddHook(ET_OnD20Signal, EK_S_Killed, lawfulSwordSpellKilled, ())
lawfulSwordSpell.AddSpellDispelCheckStandard()
lawfulSwordSpell.AddSpellTeleportPrepareStandard()
lawfulSwordSpell.AddSpellTeleportReconnectStandard()
lawfulSwordSpell.AddSpellCountdownStandardHook()

###### Lawful Sword Weapon Condition ######
def lawfulSwordWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 1

def lawfulSwordWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def lawfulSwordWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

lawfulSwordWeaponCondition = PythonModifier("Lawful Sword Weapon Condition", 2) # duration, alignType
lawfulSwordWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, lawfulSwordWeaponConditionGlowEffect, ())
lawfulSwordWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Lawful_Sword_Weapon_Effect", lawfulSwordWeaponConditionEffectAnswerToQuery, ())
lawfulSwordWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, lawfulSwordWeaponConditionTickdown, ())