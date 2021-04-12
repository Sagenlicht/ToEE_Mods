from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Iron Silence"

def ironSilenceSpellChainToArmor(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    armorWorn = attachee.item_worn_at(item_wear_armor)

    armorWorn.d20_status_init()
    spellPacket.add_target(armorWorn, 0)
    spellPacket.update_registry()
    return 0

def ironSilenceSpellNullifyArmorCheckPenalty(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == attachee.item_worn_at(item_wear_armor):
        wornShieldArmorCheckPenalty = attachee.item_worn_at(5).obj_get_int(224) # Get Armor Check Penalty
        evt_obj.bonus_list.add(abs(wornShieldArmorCheckPenalty), 0, "~Iron Silence~[TAG_SPELLS_IRON_SILENCE] Bonus") #Generic stacking bonus to counteract the Armor Check Penalty
        #evt_obj.bonus_list.add_cap(0, 0, 6), this would cancel out the masterwork property but also everything else.
    return 0

def ironSilenceSpellConditionRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    removeArmorFromSpellRegistry = spellPacket.get_target(0)
    spellPacket.remove_target(removeArmorFromSpellRegistry)
    spellPacket.update_registry()
    args.remove_spell()
    return 0

def ironSilenceSpellTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == attachee.item_worn_at(item_wear_armor):
        if args.get_arg(1) == 1:
            evt_obj.append("Iron Silence (" + str(args.get_arg(1)) + " round)")
        else:
            evt_obj.append("Iron Silence (" + str(args.get_arg(1)) + " rounds)")
    return 0

def ironSilenceSpellEffectTooltip(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == attachee.item_worn_at(item_wear_armor):
        if args.get_arg(1) == 1:
            evt_obj.append(tpdp.hash("IRON_SILENCE"), -2, " (" + str(args.get_arg(1)) + " round)")
        else:
            evt_obj.append(tpdp.hash("IRON_SILENCE"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def ironSilenceSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def ironSilenceSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def ironSilenceSpellSpellEnd(attachee, args, evt_obj):
    print "Iron SilenceSpellEnd"
    return 0

ironSilenceSpell = PythonModifier("sp-Iron Silence", 2) # spell_id, duration
ironSilenceSpell.AddHook(ET_OnConditionAdd, EK_NONE, ironSilenceSpellChainToArmor,())
ironSilenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_HIDE, ironSilenceSpellNullifyArmorCheckPenalty,())
ironSilenceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_MOVE_SILENTLY, ironSilenceSpellNullifyArmorCheckPenalty,())
ironSilenceSpell.AddHook(ET_OnConditionRemove, EK_NONE, ironSilenceSpellConditionRemove, ())
ironSilenceSpell.AddHook(ET_OnGetTooltip, EK_NONE, ironSilenceSpellTooltip, ())
ironSilenceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, ironSilenceSpellEffectTooltip, ())
ironSilenceSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, ironSilenceSpellSpellEnd, ())
ironSilenceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, ironSilenceSpellHasSpellActive, ())
ironSilenceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, ironSilenceSpellKilled, ())
ironSilenceSpell.AddSpellDispelCheckStandard()
ironSilenceSpell.AddSpellTeleportPrepareStandard()
ironSilenceSpell.AddSpellTeleportReconnectStandard()
ironSilenceSpell.AddSpellCountdownStandardHook()
