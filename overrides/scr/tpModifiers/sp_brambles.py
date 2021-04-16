from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Brambles"

def bramblesSpellChainToWeapon(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Brambles Weapon Condition', args.get_arg(1))
    return 0

def bramblesSpellToHitBonus(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Brambles_Weapon_Effect")
    if isEnchantedWeapon:
        evt_obj.bonus_list.add(1, 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Brambles~[TAG_SPELLS_BRAMBLES]")
    return 0

def bramblesSpellBonusToDamage(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Brambles_Weapon_Effect")
    if isEnchantedWeapon:
        usedWeaponDamageType = usedWeapon.obj_get_int(obj_f_weapon_attacktype)
        if not usedWeaponDamageType == D20DT_BLUDGEONING_AND_PIERCING:
            if not usedWeaponDamageType == D20DT_BLUDGEONING:
                evt_obj.damage_packet.attack_power |= D20DAP_BLUDGEONING
            if not usedWeaponDamageType == D20DT_PIERCING:
                evt_obj.damage_packet.attack_power |= D20DAP_PIERCING
        if not evt_obj.damage_packet.attack_power & D20DAP_MAGIC:
            evt_obj.damage_packet.attack_power |= D20DAP_MAGIC
        evt_obj.damage_packet.bonus_list.add(args.get_arg(2), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Brambles~[TAG_SPELLS_BRAMBLES]")
    return 0

def bramblesSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Brambles_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Brambles ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Brambles ({} rounds)".format(args.get_arg(1)))
    return 0

def bramblesSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Brambles_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("BRAMBLES"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("BRAMBLES"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def bramblesSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def bramblesSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def bramblesSpellSpellEnd(attachee, args, evt_obj):
    print "Brambles SpellEnd"
    return 0

bramblesSpell = PythonModifier("sp-Brambles", 3) # spell_id, duration, bonusDamage
bramblesSpell.AddHook(ET_OnConditionAdd, EK_NONE, bramblesSpellChainToWeapon,())
bramblesSpell.AddHook(ET_OnToHitBonus2, EK_NONE, bramblesSpellToHitBonus, ())
bramblesSpell.AddHook(ET_OnDealingDamage, EK_NONE, bramblesSpellBonusToDamage,())
bramblesSpell.AddHook(ET_OnGetTooltip, EK_NONE, bramblesSpellTooltip, ())
bramblesSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, bramblesSpellEffectTooltip, ())
bramblesSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, bramblesSpellSpellEnd, ())
bramblesSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, bramblesSpellHasSpellActive, ())
bramblesSpell.AddHook(ET_OnD20Signal, EK_S_Killed, bramblesSpellKilled, ())
bramblesSpell.AddSpellDispelCheckStandard()
bramblesSpell.AddSpellTeleportPrepareStandard()
bramblesSpell.AddSpellTeleportReconnectStandard()
bramblesSpell.AddSpellCountdownStandardHook()

###### Brambles Weapon Condition ######
def bramblesWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def bramblesWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def bramblesWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

bramblesWeaponCondition = PythonModifier("Brambles Weapon Condition", 1) # duration
bramblesWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, bramblesWeaponConditionGlowEffect, ())
bramblesWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Brambles_Weapon_Effect", bramblesWeaponConditionEffectAnswerToQuery, ()) #not tested
bramblesWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, bramblesWeaponConditionTickdown, ())