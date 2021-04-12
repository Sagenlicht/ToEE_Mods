from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Shield of Warding"

def shieldOfWardingSpellChainToShield(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    wornShield = attachee.item_worn_at(item_wear_shield)

    wornShield.d20_status_init()
    spellPacket.add_target(wornShield, 0)
    spellPacket.update_registry()
    return 0

def shieldOfWardingSpellBonus(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == attachee.item_worn_at(item_wear_shield):
        #Shield of Warding grants a bonus to AC and Reflex save; value(arg2) is passed by spell
        evt_obj.bonus_list.add(args.get_arg(2), 153, "~Shield of Warding~[TAG_SPELLS_SHIELD_OF_WARDING] ~Sacred~[TAG_MODIFIER_SACRED] Bonus")

def shieldOfWardingSpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    wornShieldInRegistry = spellPacket.get_target(0)
    if not wornShieldInRegistry == OBJ_HANDLE_NULL:
        spellPacket.remove_target(wornShieldInRegistry)
        spellPacket.update_registry()
        args.remove_spell()
    return 0

def shieldOfWardingSpellTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    wornShield = attachee.item_worn_at(item_wear_shield)
    if not spellPacket.get_target(1) == wornShield:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append("Shield of Warding ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Shield of Warding ({} rounds)".format(args.get_arg(1)))
    return 0

def shieldOfWardingSpellEffectTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    wornShield = attachee.item_worn_at(item_wear_shield)
    if not spellPacket.get_target(1) == wornShield:
        return 0
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SHIELD_OF_WARDING"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("SHIELD_OF_WARDING"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def shieldOfWardingSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def shieldOfWardingSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def shieldOfWardingSpellSpellEnd(attachee, args, evt_obj):
    print "Shield of Warding SpellEnd"
    return 0

shieldOfWardingSpell = PythonModifier("sp-Shield of Warding", 3) # spell_id, duration, shieldBonus
shieldOfWardingSpell.AddHook(ET_OnConditionAdd, EK_NONE, shieldOfWardingSpellChainToShield,())
shieldOfWardingSpell.AddHook(ET_OnGetAC, EK_NONE, shieldOfWardingSpellBonus,())
shieldOfWardingSpell.AddHook(ET_OnSaveThrowLevel, EK_SAVE_REFLEX, shieldOfWardingSpellBonus,())
shieldOfWardingSpell.AddHook(ET_OnConditionRemove, EK_NONE, shieldOfWardingSpellConditionRemove, ())
shieldOfWardingSpell.AddHook(ET_OnGetTooltip, EK_NONE, shieldOfWardingSpellTooltip, ())
shieldOfWardingSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, shieldOfWardingSpellEffectTooltip, ())
shieldOfWardingSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, shieldOfWardingSpellSpellEnd, ())
shieldOfWardingSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, shieldOfWardingSpellHasSpellActive, ())
shieldOfWardingSpell.AddHook(ET_OnD20Signal, EK_S_Killed, shieldOfWardingSpellKilled, ())
shieldOfWardingSpell.AddSpellDispelCheckStandard()
shieldOfWardingSpell.AddSpellTeleportPrepareStandard()
shieldOfWardingSpell.AddSpellTeleportReconnectStandard()
shieldOfWardingSpell.AddSpellCountdownStandardHook()
