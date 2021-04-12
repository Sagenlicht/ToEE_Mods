from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Dolorous Blow"

def dolorousBlowSpellChainToWeapon(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)

    mainhandWeapon.d20_status_init()
    spellPacket.add_target(mainhandWeapon, 0)
    spellPacket.update_registry()
    return 0

def dolorousBlowSpellModifyThreatRange(attachee, args, evt_obj):
    appliedKeenRange =  evt_obj.bonus_list.get_sum()
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    weaponUsed = evt_obj.attack_packet.get_weapon_used()

    if spellPacket.get_target(1) == weaponUsed:
        print "Range old ", appliedKeenRange
        getWeaponKeenRange = weaponUsed.obj_get_int(obj_f_weapon_crit_range)
        if appliedKeenRange == getWeaponKeenRange:
            evt_obj.bonus_list.add(getWeaponKeenRange, 0 , "~Dolorous Blow~[TAG_SPELLS_DOLORUS_BLOW] Bonus")
            print "Range new ", evt_obj.bonus_list.get_sum()
        else:
            print "Already keen"
    return 0

def dolorousBlowSpellAnswerToKeenQuery(attachee, args, evt_obj):
    if args.get_arg(1):
        evt_obj.return_val = 1
    return 0

def dolorousBlowSpellBonusToConfirmCrit(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == evt_obj.attack_packet.get_weapon_used():
        flags = evt_obj.attack_packet.get_flags()
        flags |= D20CAF_CRITICAL
        evt_obj.attack_packet.set_flags(flags)
    return 0

def dolorousBlowSpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    removeWeaponFromSpellRegistry = spellPacket.get_target(0)
    spellPacket.remove_target(removeWeaponFromSpellRegistry)
    spellPacket.update_registry()
    args.remove_spell()
    return 0

def dolorousBlowSpellTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    if not spellPacket.get_target(1) == mainhandWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Dolorous Blow ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Dolorous Blow ({} rounds)".format(args.get_arg(1)))

def dolorousBlowSpellEffectTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    if not spellPacket.get_target(1) == mainhandWeapon:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DOLOROUS_BLOW"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DOLOROUS_BLOW"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def dolorousBlowSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def dolorousBlowSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def dolorousBlowSpellSpellEnd(attachee, args, evt_obj):
    print "Dolorous BlowSpellEnd"
    return 0

dolorousBlowSpell = PythonModifier("sp-Dolorous Blow", 2) # spell_id, duration
dolorousBlowSpell.AddHook(ET_OnConditionAdd, EK_NONE, dolorousBlowSpellChainToWeapon,())
dolorousBlowSpell.AddHook(ET_OnConfirmCriticalBonus, EK_NONE, dolorousBlowSpellBonusToConfirmCrit,())
dolorousBlowSpell.AddHook(ET_OnGetCriticalHitRange, EK_NONE, dolorousBlowSpellModifyThreatRange,())
dolorousBlowSpell.AddHook(ET_OnConditionRemove, EK_NONE, dolorousBlowSpellConditionRemove, ())
dolorousBlowSpell.AddHook(ET_OnD20Query, EK_Q_Item_Has_Keen_Bonus, dolorousBlowSpellAnswerToKeenQuery, ())
#dolorousBlowSpell.AddHook(ET_OnD20Query, EK_Q_Weapon_Get_Keen_Bonus, dolorousBlowSpellAnswerToKeenQuery, ())
dolorousBlowSpell.AddHook(ET_OnGetTooltip, EK_NONE, dolorousBlowSpellTooltip, ())
dolorousBlowSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, dolorousBlowSpellEffectTooltip, ())
dolorousBlowSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, dolorousBlowSpellSpellEnd, ())
dolorousBlowSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, dolorousBlowSpellHasSpellActive, ())
dolorousBlowSpell.AddHook(ET_OnD20Signal, EK_S_Killed, dolorousBlowSpellKilled, ())
dolorousBlowSpell.AddSpellDispelCheckStandard()
dolorousBlowSpell.AddSpellTeleportPrepareStandard()
dolorousBlowSpell.AddSpellTeleportReconnectStandard()
dolorousBlowSpell.AddSpellCountdownStandardHook()
